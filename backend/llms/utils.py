from fastapi import Depends
from llms.gpt import GPTLLM
from models.user import User
from pydantic import BaseModel
from security import get_current_user


class ChatRequest(BaseModel):
    user_input: str


class ChatResponse(BaseModel):
    llm_output: str


def get_llm_sql_object(current_user: User = Depends(get_current_user)):
    # Initialize LLM object
    user_id = current_user.id
    llm = GPTLLM(user_id, store_history=False, llm_type="sql")
    return llm


def get_llm_chat_object(current_user: User = Depends(get_current_user)):
    # Initialize LLM object
    user_id = current_user.id
    llm = GPTLLM(user_id, store_history=True, llm_type="chat")
    return llm
