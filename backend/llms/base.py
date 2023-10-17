class BaseLLM:
    def __init__(self):
        pass

    def api_call(self, endpoint: str, payload: dict) -> str:
        raise NotImplementedError

    def generate_text(self, prompt: str) -> str:
        """
        Generate text based on the given prompt
        """
        raise NotImplementedError("This method should be overridden by subclass")
    
    def generate_create_table_statement():
        pass