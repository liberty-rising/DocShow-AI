from .base import BaseLLM

from tiktoken import Tokenizer

import openai
import os

class GPTLLM(BaseLLM):
    def __init__(self, history: list = []):
        """Initialize API key, model, token limit, and conversation history."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not set in environment variables")
        openai.api_key = api_key
        self.model = "gpt-4"
        self.model_info = openai.Model.retrieve(self.model)
        self.max_tokens = self.model_info['max_tokens']
        self.history = history
        self.is_system_added = False  # Flag to check if system message is added
    
    def api_call(self, payload: dict) -> str:
        """Make an API call to get a response based on the conversation history."""
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=payload['messages']
        )
        return completion.choices[0].message['content']

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        tokenizer = Tokenizer()
        token_count = sum(1 for _ in tokenizer.tokenize(text))
        return token_count
    
    def total_tokens(self, history):
        """Calculate total tokens in the given history."""
        return sum(self.count_tokens(message["content"]) for message in history)
    
    def truncate_history(self, history):
        """Truncate history to fit within token limits."""
        tokens = self.total_tokens(history)

        index_to_start = 1 if self.is_system_added else 0  # Skip the system message if it exists

        while tokens > self.max_tokens:
            removed_message = history.pop(index_to_start)
            tokens -= self.count_tokens(removed_message["content"])
        return history
    
    def get_system_message_content(self, assistant_type: str = "generic") -> str:
        """Generate a system message based on the assistant type."""
        messages = {
            "sql_code": "You are an SQL statement assistant. Generate SQL statements based on the given prompt. Return only the pure code.",
            "sql_desc": "You are an SQL table description assistant. Generate concise, informative descriptions of SQL tables based on CREATE TABLE queries and sample data. \
                Your descriptions should help in categorizing new data and provide context for future queries, reports, and analytics.",
            "table_categorization": "You are a table categorization assistant. Your task is to analyze sample data and existing table metadata to identify the most suitable \
                table for appending the sample data. Return only the name of the table.",
            "generic": "You are a generic assistant."
        }
        return messages.get(assistant_type, "You are a generic assistant.")
    
    def create_message(self, role: str, prompt: str):
        """Create either a user, system, or assistant message."""
        return {"role":f"{role}", "content": f"{prompt}"}
    
    def add_system_message(self, assistant_type: str) -> None:
        """
        Adds a system message based on the given assistant type.
        Replaces the existing system message if one is present.
        """
        system_message_content = self.get_system_message_content(assistant_type)
        system_message  = self.create_message("system", system_message_content)

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
    
    def generate_create_statement(self, sample_content: str, existing_table_names: str, extra_desc: str) -> str:
        """
        Generate an SQL CREATE TABLE statement based on sample data and additional constraints.
        
        Parameters:
            sample_content (str): Sample data that the SQL table will store.
            existing_table_names (str): Names of tables that already exist and should not be used.
            extra_desc (str): Additional information or context about the sample data.
            
        Returns:
            str: The generated SQL CREATE TABLE statement.
        """
        self.add_system_message(assistant_type="sql_code")

        prompt = f"Generate SQL CREATE TABLE statement for the following sample data: \n{sample_content}"
        if existing_table_names:
            prompt += f"\n\nDo not use the following table names as they are already in use: \n{existing_table_names}"
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: \n{extra_desc}"
        user_message = self.create_message("user", prompt)
        self.history.append(user_message)

        # Check token limit and truncate history if needed
        self.truncate_history(self.history)

        # Make API call
        assistant_message_content = self.api_call({"messages": self.history})
        assistant_message = self.create_message("assistant", assistant_message_content)

        # Append assistant's reply to history
        self.history.append(assistant_message)

        return assistant_message
    
    def generate_table_desc(self, create_query: str, sample_content: str, extra_desc: str) -> str:
        """
        Generate a concise description for a SQL table based on its CREATE TABLE query and sample data.
    
        Parameters:
            create_query (str): The SQL CREATE TABLE query that defines the table.
            sample_content (str): A sample of the data that will be stored in the table.
            extra_desc (str): Additional context or information about the sample data.
            
        Returns:
            str: A brief, focused description of the SQL table without any additional formatting, titles, or filler text.
        """
        
        self.add_system_message(assistant_type="sql_desc")

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

        user_message = self.create_message("user", prompt)
        self.history.append(user_message)

        # Check token limit and truncate history if needed
        self.truncate_history(self.history)

        # Make API call
        assistant_message_content = self.api_call({"messages": self.history})
        assistant_message = self.create_message("assistant", assistant_message_content)

        # Append assistant's reply to history
        self.history.append(assistant_message)

        return assistant_message
    
    def fetch_table_from_sample(self, sample_content: str, extra_desc: str, table_metadata: str):
        """
        Determine the most appropriate existing table to which the sample data should be appended.
        
        Parameters:
            sample_content (str): The sample data that needs to be categorized into an existing table.
            extra_desc (str): Additional context or instructions regarding the sample data.
            table_metadata (str): Metadata of existing tables.
            
        Returns:
            str: The name of the existing table to which the sample data should be appended.
        """

        self.add_system_message(assistant_type="table_categorization")

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

        user_message = self.create_message("user", prompt)
        self.history.append(user_message)

        # Check token limit and truncate history if needed
        self.truncate_history(self.history)

        # Make API call
        assistant_message_content = self.api_call({"messages": self.history})
        assistant_message = self.create_message("assistant", assistant_message_content)

        # Append assistant's reply to history
        self.history.append(assistant_message)

        return assistant_message

