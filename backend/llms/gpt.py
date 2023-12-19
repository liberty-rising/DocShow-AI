from openai import ChatCompletion
from typing import List, Optional

import json
import openai
import tiktoken

from .base import BaseLLM
from databases.chat_history_manager import ChatHistoryManager
from databases.database_manager import DatabaseManager
from llms.prompt_manager import PromptManager
from llms.system_message_manager import SystemMessageManager
from models.user import User
from settings import OPENAI_API_KEY
from utils.nivo_assistant import NivoAssistant


class GPTLLM(BaseLLM):
    """
    A class representing a GPT-based Language Learning Model (LLM) with chat history storage capabilities.

    This class encapsulates the functionality for initializing and managing a GPT model, including configuration for API key, model version, token limits, and optional storage of chat
    history in a specified database.
    It is designed to be flexible for different users, requests, and chat session management.
    """

    def __init__(
        self,
        chat_id: Optional[int],
        user: User = None,
        store_history: bool = False,
        llm_type: str = "generic",
        database_type: str = "postgres",
    ):
        """
        Initializes an instance of the GPT-based Language Model (LLM) with optional chat history storage.

        This constructor sets up the GPT model with necessary parameters and configurations, such as API key, model type, token limit, and chat history management.
        It also initializes the user and chat identifiers, and determines whether to store chat history based on the provided parameters.

        Parameters:
        chat_id (int, optional): Unique identifier for the chat session. Defaults to None.
        user (User, optional): The user object containing user-specific information like user_id and organization_id. Defaults to None.
        store_history (bool, optional): Flag indicating whether to store chat history in the database. Defaults to False.
        llm_type (str, optional): Specifies the type of the language model. Defaults to "generic".
        database_type (str, optional): Specifies the type of database being used, such as "postgres". Defaults to "postgres".

        Note:
        - The OPENAI_API_KEY is required and used to authenticate with the OpenAI API.
        - The model is set to "gpt-4-1106-preview" and the maximum token limit is set to 8192 as of October 2023.
        - If 'chat_id' is provided and 'store_history' is True, the chat history will be fetched from the database.
        - The history of the chat is maintained in a list, which is empty by default unless fetched from the database.
        """
        openai.api_key = OPENAI_API_KEY
        self.model = "gpt-4-1106-preview"
        self.response_format = {"type": ""}
        self.max_tokens = 8192  # As of Oct 2023
        self.is_system_added = False  # Flag to check if system message is added

        self.chat_id = chat_id
        self.user_id = user.id
        self.organization_id = user.organization_id
        self.prompt_manager = PromptManager()
        self.store_history = store_history
        self.system_message_manager = SystemMessageManager()
        self.llm_type = llm_type
        self.database_type = database_type
        self.history = self._set_init_history()

    def _set_init_history(self):
        """Helper function to set the initial history for the instance."""
        if self.chat_id and self.store_history:
            with DatabaseManager() as session:
                chat_manager = ChatHistoryManager(session)
                return chat_manager.get_history(self.chat_id)
        else:
            return []

    def _set_response_format(self, is_json: bool):
        if is_json:
            self.response_format = {"type": "json_object"}
        else:
            self.response_format = {"type": ""}

    async def _api_call(self, payload: dict) -> str:
        """Make an API call to get a response based on the conversation history."""
        completion: ChatCompletion = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=payload["messages"],
            response_format=self.response_format,
        )
        return str(
            completion.choices[0].message.content
        )  # TODO: Typecasting is not recommended for mypy

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        encoding = tiktoken.encoding_for_model(self.model)
        token_count = len(
            encoding.encode(text)
        )  # Use the .encode() method to tokenize and count the tokens
        return token_count

    def _total_tokens(self):
        """Calculate total tokens in the given history."""
        return sum(self._count_tokens(message["content"]) for message in self.history)

    def _truncate_history(self):
        """Truncate history to fit within token limits."""
        tokens = self._total_tokens()

        index_to_start = (
            1 if self.is_system_added else 0
        )  # Skip the system message if it exists

        while tokens > self.max_tokens:
            removed_message = self.history.pop(index_to_start)
            tokens -= self._count_tokens(removed_message["content"])

    def _get_system_message_content(self, assistant_type: str = "generic") -> str:
        """Generate a system message based on the assistant type."""
        system_message_content: str = (
            self.system_message_manager.get_system_message_content(assistant_type)
        )
        return system_message_content

    def _create_message(self, role: str, prompt: str):
        """Create either a user, system, or assistant message."""
        return {"role": f"{role}", "content": f"{prompt}"}

    def _add_system_message(self, assistant_type: str) -> None:
        """
        Adds a system message based on the given assistant type.
        Replaces the existing system message if one is present.
        """
        system_message_content = self._get_system_message_content(assistant_type)
        system_message = self._create_message("system", system_message_content)

        if self.is_system_added:
            # Replace the existing system message
            self.history[0] = system_message
        else:
            if len(self.history) > 0:
                # Shift existing history to make room for the new system message at the beginning
                self.history = [system_message] + self.history
            else:
                # If history is empty, simply add the system message
                self.history.append(system_message)

            self.is_system_added = True

        self.llm_type = assistant_type

    async def _send_and_receive_message(self, prompt: str) -> str:
        user_message = self._create_message("user", prompt)
        self.history.append(user_message)

        # Check token limit and truncate history if needed
        self._truncate_history()

        # Make API call
        assistant_message_content = await self._api_call({"messages": self.history})
        assistant_message = self._create_message("assistant", assistant_message_content)

        # Append assistant's reply to history
        self.history.append(assistant_message)

        if self.store_history:
            self._save_messages(user_message, assistant_message)

        return assistant_message_content

    def _save_messages(self, user_message, assistant_message):
        """
        Saves the user's message and the assistant's response to the database.

        This method serializes both the user and assistant messages into JSON format
        and then stores them in the database using the ChatHistoryManager. If a chat_id
        does not exist for the current session, it generates a new one. This ensures
        that each message is associated with the correct chat session and user.

        Parameters:
        user_message (dict): A dictionary representing the user's message.
        assistant_message (dict): A dictionary representing the assistant's response.

        Note:
        This method assumes an existing DatabaseManager context for database operations.
        There's a TODO regarding freezing operations to prevent duplicate chat_id assignment.
        """

        # Serialize to JSON for storage:
        json_user_message = json.dumps(user_message)
        json_assistant_message = json.dumps(assistant_message)

        with DatabaseManager() as session:
            chat_manager = ChatHistoryManager(session)
            if not self.chat_id:  # Generate a new chat id
                # TODO: Freeze operations here (not 100% sure but worried about other users getting the same chat id)
                self.chat_id = chat_manager.get_new_chat_id()

            chat_manager.save_message(
                chat_id=self.chat_id,
                user_id=self.user_id,
                organization_id=self.organization_id,
                llm_type=self.llm_type,
                message=json_user_message,
                is_user=True,
            )
            chat_manager.save_message(
                chat_id=self.chat_id,
                user_id=self.user_id,
                organization_id=self.organization_id,
                llm_type=self.llm_type,
                message=json_assistant_message,
                is_user=False,
            )

    async def generate_create_statement(
        self,
        sample_content: str,
        header: str,
        existing_table_names: str,
        extra_desc: str,
    ) -> str:
        """
        Generate an SQL CREATE TABLE statement based on sample data and additional constraints.

        Parameters:
            sample_content (str): Sample data that the SQL table will store.
            existing_table_names (str): Names of tables that already exist and should not be used.
            extra_desc (str): Additional information or context about the sample data.

        Returns:
            str: The generated SQL CREATE TABLE statement.
        """
        self._add_system_message(assistant_type="sql_code")

        prompt = self.prompt_manager.create_table_create_prompt(
            sample_content, header, existing_table_names, extra_desc
        )

        gpt_response: str = await self._send_and_receive_message(prompt)

        return gpt_response

    async def generate_table_desc(
        self, create_query: str, sample_content: str, extra_desc: str
    ) -> str:
        """
        Generate a concise description for a SQL table based on its CREATE TABLE query and sample data.

        Parameters:
            create_query (str): The SQL CREATE TABLE query that defines the table.
            sample_content (str): A sample of the data that will be stored in the table.
            extra_desc (str): Additional context or information about the sample data.

        Returns:
            str: A brief, focused description of the SQL table without any additional formatting, titles, or filler text.
        """

        self._add_system_message(assistant_type="sql_desc")

        prompt = self.prompt_manager.create_table_desc_prompt(
            create_query, sample_content, extra_desc
        )

        gpt_response = await self._send_and_receive_message(prompt)

        return gpt_response

    async def generate_chart_config(
        self, msg: str, table_metadata: str, chart_type: str, nivo_config: dict
    ):
        """Generate the full chart configuration."""  # TODO: Make chart_type dynamic, LLM should pick
        self._add_system_message(assistant_type="nivo_charts")
        self._set_response_format(is_json=True)

        assistant = NivoAssistant(chart_type)
        nivo_config_preview = assistant.sample_data_for_llm(nivo_config)

        # TODO: minValue and maxValue should always be set to auto
        # TODO: keys, indexBy is not a valid key for all charts, should be dynamically added.

        prompt = self.prompt_manager.create_chart_config_prompt(
            msg, table_metadata, chart_type, nivo_config_preview
        )

        updated_config = await self._send_and_receive_message(
            prompt
        )  # Returns a JSON string

        # Parse the JSON string
        parsed_config = json.loads(updated_config)

        print("raw data", parsed_config)

        return parsed_config

    def fetch_table_name_from_sample(
        self, sample_content: str, extra_desc: str, table_metadata: str
    ):
        """
        Determine the most appropriate existing table to which the sample data should be appended.

        Parameters:
            sample_content (str): The sample data that needs to be categorized into an existing table.
            extra_desc (str): Additional context or instructions regarding the sample data.
            table_metadata (str): Metadata of existing tables.

        Returns:
            str: The name of the existing table to which the sample data should be appended.
        """

        self._add_system_message(assistant_type="table_categorization")

        prompt = self.prompt_manager.create_get_table_name_from_sample_prompt(
            sample_content, extra_desc, table_metadata
        )

        gpt_response = self._send_and_receive_message(prompt)

        return gpt_response

    def generate_text(self, input_text):
        self._add_system_message(assistant_type="generic")

        prompt = input_text

        assistant_message_content = self._send_and_receive_message(prompt)

        return assistant_message_content

    def generate_analytics_text(self, input_text: str, table_names: List[str]):
        self._add_system_message(assistant_type="analytics_chat")
