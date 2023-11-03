from pydantic import BaseModel

from llms.gpt import GPTLLM

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    llm_output: str

def get_llm_sql_object():
    global user_id  

    # Initialize LLM object
    llm = GPTLLM(user_id, store_history=False, llm_type="sql")
    return llm

def get_llm_chat_object():
    global user_id

    # Initialize LLM object
    llm = GPTLLM(user_id, store_history=True, llm_type="chat")
    return llm