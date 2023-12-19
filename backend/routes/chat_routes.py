from fastapi import APIRouter, Depends

from databases.chat_history_manager import ChatHistoryManager
from databases.database_manager import DatabaseManager
from llms.base import BaseLLM
from llms.gpt import GPTLLM
from llms.utils import ChatRequest, ChatResponse, get_llm_chat_object
from models.chat import AnalyticsRequest, AnalyticsResponse
from models.user import User
from security import get_current_user

chat_router = APIRouter()


@chat_router.post("/chat/")
async def chat_endpoint(
    request: ChatRequest,
    llm: BaseLLM = Depends(get_llm_chat_object),
    current_user: User = Depends(get_current_user),
):
    user_input = request.user_input
    llm_output = llm.generate_text(user_input)
    return ChatResponse(llm_output=llm_output)


@chat_router.post("/chat/analytics/")
async def chat_analytics_endpoint(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user),
):
    gpt = GPTLLM(chat_id=request.chat_id, user=current_user, store_history=True)
    response = gpt.generate_text(request.prompt)
    return AnalyticsResponse(chat_id=gpt.chat_id, response=response)


@chat_router.delete("/chat_history/")
async def delete_chat_history(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    with DatabaseManager() as session:
        chat_service = ChatHistoryManager(session)
        chat_service.delete_chat_history(user_id)

    return {"message": "Chat history deleted"}
