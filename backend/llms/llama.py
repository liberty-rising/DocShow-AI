from .base import BaseLLM

class LlamaLLM(BaseLLM):
    def __init__(self):
        self.api_key = "LLAMA_API_KEY"
        self.endpoint = "LLAMA_ENDPOINT"

    def generate_text(self, prompt: str) -> str:
        return f"Llama Generated Text for: {prompt}"