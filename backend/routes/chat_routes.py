from fastapi import APIRouter, Depends

from database.chat_history_manager import ChatHistoryManager
from database.database_manager import DatabaseManager
from database.table_map_manager import TableMapManager
from llms.base import BaseLLM
from llms.gpt_lang import GPTLangSQL
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


@chat_router.post("/chat/analytics/", response_model=AnalyticsResponse)
async def chat_analytics_endpoint(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user),
):
    with DatabaseManager() as session:
        table_map_manager = TableMapManager(session)
        org_tables = table_map_manager.get_org_tables(current_user.organization_id)

    gpt = GPTLangSQL(tables=org_tables)
    response = gpt.generate(request.prompt)
    return AnalyticsResponse(chat_id=1, response=response)


@chat_router.delete("/chat_history/")
async def delete_chat_history(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    with DatabaseManager() as session:
        chat_service = ChatHistoryManager(session)
        chat_service.delete_chat_history(user_id)

    return {"message": "Chat history deleted"}
