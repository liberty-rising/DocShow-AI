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

    def generate_create_statement(
        self, sample_content: str, existing_table_names: str, extra_desc: str
    ) -> str:
        raise NotImplementedError

    def generate_table_desc(
        self, create_query: str, sample_content: str, extra_desc: str
    ) -> str:
        raise NotImplementedError

    def fetch_table_name_from_sample(
        self, sample_content: str, extra_desc: str, table_metadata: str
    ):
        raise NotImplementedError
