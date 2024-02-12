import json
from typing import Dict, List, Optional

import openai
import tiktoken
from database.chat_history_manager import ChatHistoryManager
from database.database_manager import DatabaseManager
from llms.prompt_manager import PromptManager
from llms.system_message_manager import SystemMessageManager
from models.data_profile import DataProfile
from models.user import User
from openai import ChatCompletion
from settings import OPENAI_API_KEY
from utils.file_manager import FileManager
from utils.nivo_assistant import NivoAssistant

from .base import BaseLLM


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

        # User and chat identifiers
        self.chat_id = chat_id
        self.user_id = user.id
        self.organization_id = user.organization_id

        openai.api_key = OPENAI_API_KEY
        self.database_type = database_type
        self.llm_type = llm_type
        self.model = "gpt-4-1106-preview"
        self.max_tokens = 8192  # As of Oct 2023
        self.is_system_added = False  # Flag to check if system message is added
        self.response_format = {"type": ""}
        self.store_history = store_history
        self.history = self._set_init_history()

        # Vision settings
        self.image_detail = "high"

        # Managers
        self.file_manager = FileManager()
        self.prompt_manager = PromptManager()
        self.system_message_manager = SystemMessageManager()

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

    def _set_model(self, model_type: str):
        if model_type == "img":
            self.model = "gpt-4-vision-preview"
        else:
            self.model = "gpt-4-1106-preview"

    async def _api_call(self, payload: dict) -> str:
        """Make an API call to get a response based on the conversation history."""
        params = {
            "model": self.model,
            "messages": payload["messages"],
            "max_tokens": 1000,
        }
        if self.response_format["type"]:
            params["response_format"] = self.response_format

        completion: ChatCompletion = await openai.ChatCompletion.acreate(**params)
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

    def _count_image_tokens(self, width: int, height: int) -> int:
        """Count the number of tokens in the given image."""
        if max(width, height) > 2048:
            aspect_ratio = width / height
            if width > height:
                width = 2048
                height = int(width / aspect_ratio)
            else:
                height = 2048
                width = int(height * aspect_ratio)

        # Scale down such that the shortest side is 768px long
        aspect_ratio = width / height
        if width < height:
            width = 768
            height = int(width / aspect_ratio)
        else:
            height = 768
            width = int(height * aspect_ratio)

        # Count how many 512px squares the image consists of
        num_squares = (width // 512) * (height // 512)

        # Each square costs 170 tokens, and 85 tokens are always added to the final total
        token_cost = 170 * num_squares + 85

        return token_cost

    def _total_tokens(self) -> int:
        """Calculate total tokens in the given history."""
        total_tokens = 0
        for message in self.history:
            content = message["content"]
            if isinstance(content, str):
                total_tokens += self._count_tokens(content)
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and "image_url" in item:
                        total_tokens += self._count_image_tokens(
                            1024, 1024
                        )  # Adjust these values based on your image's actual dimensions
        return total_tokens

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

    def _create_message(
        self, role: str, prompt: str, jpg_presigned_urls: List[str] = []
    ):
        """Create either a user, system, or assistant message."""
        content: List[Dict] = [{"type": "text", "text": prompt}]
        for url in jpg_presigned_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": url, "detail": self.image_detail},
                }
            )

        return {"role": role, "content": content}

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

    async def _send_and_receive_message(
        self, prompt: str, jpg_presigned_urls: List[str] = []
    ) -> str:
        user_message = self._create_message("user", prompt, jpg_presigned_urls)
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

    async def generate_suggested_column_metadata(self, column_names: list, data: dict):
        """Generate suggested column types for the given data."""
        self._add_system_message(assistant_type="column_metadata_suggestion")
        self._set_response_format(is_json=True)

        prompt = self.prompt_manager.create_column_metadata_suggestion_prompt(
            column_names, data
        )

        gpt_response = await self._send_and_receive_message(prompt)

        suggested_column_types = json.loads(gpt_response)

        return suggested_column_types

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

    async def extract_data_from_jpgs(
        self, data_profile: DataProfile, jpg_presigned_urls: List[str]
    ):
        self._add_system_message(assistant_type="jpg_data_extraction")
        self._set_model(model_type="img")

        instructions = data_profile.extract_instructions
        prompt = self.prompt_manager.jpg_data_extraction_prompt(instructions)

        assistant_message_content = await self._send_and_receive_message(
            prompt, jpg_presigned_urls
        )
        json_string = assistant_message_content.replace("```json\n", "").replace(
            "\n```", ""
        )
        data = json.loads(json_string)

        # If data is a dictionary, wrap it in a list
        if isinstance(data, dict):
            data = [data]
        print(data)
        return data
