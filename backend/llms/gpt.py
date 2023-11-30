from .base import BaseLLM
from databases.chat_history_manager import ChatHistoryManager
from databases.database_managers import ClientDatabaseManager
from models.app_models import User
from settings import OPENAI_API_KEY
from utils.nivo_assistant import NivoAssistant

import json
import openai
import tiktoken

class GPTLLM(BaseLLM):
    """
    A class representing a GPT-based Language Learning Model (LLM) with chat history storage capabilities.

    This class encapsulates the functionality for initializing and managing a GPT model, including configuration for API key, model version, token limits, and optional storage of chat history in a specified database. 
    It is designed to be flexible for different users, requests, and chat session management.
    """
    def __init__(self, chat_id: int = None, user: User = None, store_history: bool = False, llm_type: str = "generic", database_type: str = "postgres"):
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
        self.store_history = store_history
        self.llm_type = llm_type
        self.database_type = database_type
        self.history = self._set_init_history()
    
    def _set_init_history(self):
        """Helper function to set the initial history for the instance."""
        if self.chat_id and self.store_history:
            with ClientDatabaseManager() as session:
                chat_manager = ChatHistoryManager(session)
                return chat_manager.get_history(self.chat_id)
        else:
            return []
    
    def _set_response_format(self, is_json: bool):
        if is_json:
            self.response_format = { "type": "json_object" }
        else:
            self.response_format = { "type": "" }
    
    async def _api_call(self, payload: dict) -> str:
        """Make an API call to get a response based on the conversation history."""
        completion = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=payload['messages'],
            response_format=self.response_format
        )
        return completion.choices[0].message.content

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        encoding = tiktoken.encoding_for_model(self.model) 
        token_count = len(encoding.encode(text))  # Use the .encode() method to tokenize and count the tokens
        return token_count
    
    def _total_tokens(self):
        """Calculate total tokens in the given history."""
        return sum(self._count_tokens(message["content"]) for message in self.history)
    
    def _truncate_history(self):
        """Truncate history to fit within token limits."""
        tokens = self._total_tokens()

        index_to_start = 1 if self.is_system_added else 0  # Skip the system message if it exists

        while tokens > self.max_tokens:
            removed_message = self.history.pop(index_to_start)
            tokens -= self._count_tokens(removed_message["content"])
    
    def _get_system_message_content(self, assistant_type: str = "generic") -> str:
        """Generate a system message based on the assistant type."""
        messages = {
            "sql_code": f"You are a {self.database_type} SQL statement assistant. Generate {self.database_type} SQL statements based on the given prompt. Return only the pure code.",
            "nivo_charts":f"""
                You are a nivo chart generator assistant.
                Nivo is a visualisation library for React that produces different types of charts.
                You will only be working with responsive charts. Ex. ResponsiveBar, ResponsiveLine, etc.
                You will be in charge of generating configurations, SQL queries, and titles.
                Style the charts clean and modernly.
                Do not add introductory statements, filler words, or extra formatting.
            """,
            "nivo_config_for_charts":f"""
                You are a JSON generator assistant.
                You will be creating a JSON that will hold the configuration needed for a nivo chart (react library).
                You will be given the user's request, the name and metadata of the table to be visualized, the type of chart, the query used on the table, and the current NIVO configuration.
                Generate the necessary nivo configuration in the form of a JSON. If the chart does not have any styling, add some, and make it look nice.
                Implement any styling the user asks for.
                Return only the pure JSON.
            """,
            "sql_code_for_charts": f"""
                You are a {self.database_type} SQL statement assistant. 
                Your query will be used to create a chart using the NIVO library. 
                You will be given the table name, information about the table, type of chart that will be used, the existing query (if there is one), along with what data the user wishes to visualise. 
                The user may not always use the correct names for the columns, it is your job to decide which column the user is referring to by using the information you have about the table.
                Generate {self.database_type} SQL statements based on the given prompt. Return only the pure code.
            """,
            "title_for_chart": f"""
                You are a chart title generator assistant.
                You will be naming a chart based on the given inputs.
                Return only the chart name.
            """,
            "sql_desc": "You are an SQL table description assistant. Generate concise, informative descriptions of SQL tables based on CREATE TABLE queries and sample data. \
                Your descriptions should help in categorizing new data and provide context for future queries, reports, and analytics.",
            "table_categorization": "You are a table categorization assistant. Your task is to analyze sample data and existing table metadata to identify the most suitable \
                table for appending the sample data. Return only the name of the table.",
            "generic": "You are a generic assistant."
        }
        return messages.get(assistant_type, "You are a generic assistant.")
    
    def _create_message(self, role: str, prompt: str):
        """Create either a user, system, or assistant message."""
        return {"role":f"{role}", "content": f"{prompt}"}
    
    def _add_system_message(self, assistant_type: str) -> None:
        """
        Adds a system message based on the given assistant type.
        Replaces the existing system message if one is present.
        """
        system_message_content = self._get_system_message_content(assistant_type)
        system_message  = self._create_message("system", system_message_content)

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
    
    async def _send_and_receive_message(self, prompt: str):
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
            self._save_messages()

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
        This method assumes an existing ClientDatabaseManager context for database operations.
        There's a TODO regarding freezing operations to prevent duplicate chat_id assignment.
        """

        # Serialize to JSON for storage:
        json_user_message = json.dumps(user_message)
        json_assistant_message = json.dumps(assistant_message)

        with ClientDatabaseManager() as session:
            chat_manager = ChatHistoryManager(session)
            if not self.chat_id:  # Generate a new chat id
                # TODO: Freeze operations here (not 100% sure but worried about other users getting the same chat id)
                self.chat_id = chat_manager.get_new_chat_id()

            chat_manager.save_message(chat_id=self.chat_id, user_id=self.user_id, organization_id=self.organization_id,
                                      llm_type=self.llm_type, message=json_user_message, is_user=True)  
            chat_manager.save_message(chat_id=self.chat_id, user_id=self.user_id, organization_id=self.organization_id, 
                                      llm_type=self.llm_type, message=json_assistant_message, is_user=False)
    
    async def generate_create_statement(self, sample_content: str, header: str, existing_table_names: str, extra_desc: str) -> str:
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

        prompt = f"Generate SQL CREATE TABLE statement for the following sample data:"
        if header:
            prompt += f"\n\nHeader:\n{header}"
        prompt += f"\n\nSample data:\n{sample_content}"
        if existing_table_names:
            prompt += f"\n\nDo not use the following table names as they are already in use: \n{existing_table_names}"
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: \n{extra_desc}"
        
        gpt_response = await self._send_and_receive_message(prompt)

        return gpt_response
    
    async def generate_table_desc(self, create_query: str, sample_content: str, extra_desc: str) -> str:
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

        prompt = f"""
            Generate a brief description for the table that will be created using the SQL CREATE TABLE query below. 
            This description should help in determining whether to categorize new data into this table 
            and should also provide the context needed to generate suggested queries for reports and analytics in the future.

            SQL CREATE TABLE Query:
            {create_query}

            Sample Data:
            {sample_content}

            Only generate the description, no formatting or title. Do not include any additional text, explanations, or filler words.
            """
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: {extra_desc}"

        gpt_response = await self._send_and_receive_message(prompt)

        return gpt_response
    
    async def generate_chart_config_v2(self, msg: str, table_name: str, table_metadata: str, chart_type: str, nivo_config: dict):
        """Generate the full chart configuration."""  # TODO: Make chart_type dynamic, LLM should pick
        self._add_system_message(assistant_type="nivo_charts")
        self._set_response_format(is_json=True)

        assistant = NivoAssistant(chart_type)
        nivo_config_preview = assistant.sample_data_for_llm(nivo_config)

        prompt = f"""
            Given all of the context, generate the requested data based on the following request:

            User request:
            {msg}
            Table name:
            {table_name}
            Table metadata:
            {table_metadata}
            Chart type:
            Responsive {chart_type}
            Current nivo configuration:
            {nivo_config_preview}

            Provide output in JSON format as follows:
            {{
                "title":"",
                "query":"",
                "nivoConfig":{{}}
            }}

            The data key in nivoConfig shows a preview of the data. Do not update it.
        """

        updated_config = await self._send_and_receive_message(prompt)  # Returns a JSON string

        # Parse the JSON string
        parsed_config = json.loads(updated_config)

        return parsed_config

    
    async def generate_query_for_chart(self, msg: str, table_name: str, table_metadata: str, chart_type: str, existing_query: str) -> str:
        """
        Generate an SQL query for a chart based on a prompt.
        """
        self._add_system_message(assistant_type="sql_code_for_charts")
        existing_query_section = f"Existing query:\n{existing_query}\n" if existing_query else ""
        existing_query_info = f"The request may be a pure styling request, with no need to change the existing query. \
            If that is the case, return the existing query." if existing_query else ""
        prompt = f"""
            Generate an SQL query for the following request:

            Table name: {table_name}
            Information about the table:
            {table_metadata}
            Chart that will be used:
            {chart_type}
            {existing_query_section}
            Request:
            {msg}

            Make sure to use only the columns specified in the table information (within the create query).
            {existing_query_info}
        """

        return await self._send_and_receive_message(prompt)
    
    async def generate_chart_config(self, msg: str, table_name: str, table_metadata: str, chart_type: str, query: str, nivo_config: dict):
        """
        Generate the nivo chart config for the given inputs.
        """
        self._add_system_message(assistant_type="nivo_config_for_charts")
        self._set_response_format(is_json=True)
        
        nivo_assistant = NivoAssistant(chart_type)
        available_chart_params = nivo_assistant.get_available_params()  # TODO: Decide if it's worth adding this much data for llm context
        prompt = f"""
            Generate the nivo configuration for the following request. Do not change the values in the data key of the nivo config. 
            Add styling in accordance with what the user requests. If there is no styling, add styling. Ensure the chart looks modern and is optimized for readibility. 

            Request:
            {msg}
            Table name:
            {table_name}
            Table metadata:
            {table_metadata}
            Chart type:
            {chart_type}
            Query:
            {query}
            Existing nivo configuration:
            {nivo_config}

            Return a JSON represenation of the nivo configuration. Do not add any filler words or introductions. Just the pure code.
        """

        updated_nivo_config = await self._send_and_receive_message(prompt)
        updated_nivo_config = updated_nivo_config.replace("\n", "").replace("\\","")  # Clean up the string
        print('RAW CONFIG\n', updated_nivo_config)

        # Convert the cleaned string to a Python dictionary
        try:
            updated_nivo_config = json.loads(updated_nivo_config)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        
        updated_nivo_config["data"] = nivo_config["data"]  # Ensures GPT does not overwrite the data

        return updated_nivo_config
    
    async def generate_title_for_chart(self, msg: str, table_name: str, table_metadata: str, chart_type: str, query: str, existing_chart_name: str):
        """
        Generate a title for a chart.
        """
        self._add_system_message(assistant_type="title_for_chart")

        existing_title_section = f"Existing title:\n{existing_chart_name}\n" if existing_chart_name else ""
        existing_title_info = f"If the existing title correctly represents the data, return the existing title.\
            If the chart configuration request seems to only be a styling request, return the existing title." if existing_chart_name else ""

        prompt = f"""
            Generate a title for the following request:

            Chart configuration request:
            {msg}
            Table name:
            {table_name}
            Table metadata:
            {table_metadata}
            Chart type:
            {chart_type}
            Query on table for the chart:
            {query}
            {existing_title_section}
            {existing_title_info}
        """

        title = await self._send_and_receive_message(prompt)
        title = title.replace('"','')

        return title

    def fetch_table_name_from_sample(self, sample_content: str, extra_desc: str, table_metadata: str):
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

        prompt = f"""
            Based on the sample data and existing table metadata, determine to which table the sample data should be appended. 

            Sample Data: 
            {sample_content}

            Existing Table Metadata:
            {table_metadata}

            Return only the name of the table.
            """
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: {extra_desc}"

        gpt_response = self._send_and_receive_message(prompt)

        return gpt_response

    def generate_text(self, input_text):
        self._add_system_message(assistant_type="generic")

        prompt = input_text

        assistant_message_content = self._send_and_receive_message(prompt)
        
        return assistant_message_content
