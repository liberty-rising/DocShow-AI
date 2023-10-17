from .base import BaseLLM

from tiktoken import Tokenizer

import openai
import os

class GPTLLM(BaseLLM):
    def __init__(self):
        """Initialize API key, model, token limit, and conversation history."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not set in environment variables")
        openai.api_key = api_key
        self.model = "gpt-4"
        self.model_info = openai.Model.retrieve(self.model)
        self.max_tokens = self.model_info['max_tokens']
        self.history = []
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
            "sql": "You are an SQL statement assistant. Generate SQL statements based on the given prompt. Return only the pure code.",
            "poetic": "You are a poetic assistant, skilled in generating beautiful poems.",
            "generic": "You are a generic assistant."
        }
        return messages.get(assistant_type, "You are a generic assistant.")
    
    def add_system_message(self, assistant_type: str) -> None:
        """
        Adds a system message based on the given assistant type.
        Replaces the existing system message if one is present.
        """
        system_message  = {"role": "system", "content": self.get_system_message_content(assistant_type)}

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
        
    
    def generate_create_statement(self, sample_content: str, existing_table_names: str, desc: str) -> str:
        """Generate an SQL CREATE statement based on the given sample content and constraints."""
        self.add_system_message("sql")

        prompt = f"Generate SQL CREATE TABLE statement for the following sample data: \n{sample_content}"
        if existing_table_names:
            prompt += f"\nDo not use the following table names as they are already in use: {existing_table_names}"
        if desc:
            prompt += f"\nAdditional information about the sample data: {desc}"
        user_message = {"role": "user", "content": prompt}
        self.history.append(user_message)

        # Check token limit and truncate history if needed
        self.truncate_history(self.history)

        # Make API call
        assistant_message = self.api_call({"messages": self.history})

        # Append assistant's reply to history
        self.history.append({"role": "assistant", "content": assistant_message})

        return assistant_message
    
    def generate_table_desc(self, create_query: str, sample_content: str, desc: str) -> str:
        # TODO Determine whether to use the generic assistant
        self.add_system_message()

    

