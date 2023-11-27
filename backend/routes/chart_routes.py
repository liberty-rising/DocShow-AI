from fastapi import APIRouter, Depends
from pydantic import BaseModel

from databases.chart_manager import ChartManager
from databases.database_managers import ClientDatabaseManager
from databases.table_metadata_manager import TableMetadataManager
from llms.gpt import GPTLLM
from models.app_models import User
from models.client_models import Chart, ChartCreate
from security import get_current_user
from utils.nivo_assistant import NivoAssistant
from utils.utils import execute_select_query

import json
import os

chart_router = APIRouter()

class ChartConfigRequest(BaseModel):
    chat_id: int
    msg: str
    chart_config: dict

@chart_router.get("/charts/types/")
async def get_chart_types():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'chart_types.json')
    with open(config_path, 'r') as file:
        chart_types = json.load(file)
    return chart_types

@chart_router.post("/chart/")
async def save_chart(chart: ChartCreate):

    with ClientDatabaseManager() as session:
        manager = ChartManager(session)
        highest_order = manager.get_highest_order()
        order = highest_order + 1

        db_chart = Chart(
            dashboard_id = chart.dashboardId,
            order = order,
            config = chart.conf
        )

        manager.save_chart(db_chart)

@chart_router.post("/chart/config/")
async def create_chart_config(request: ChartConfigRequest, user: User = Depends(get_current_user)):
    """Creates or updates a chart configuration using an LLM."""
    chat_id = request.chat_id
    msg = request.msg
    chart_config = request.chart_config
    table_name = chart_config.get("table")
    chart_type = chart_config.get("type")
    existing_query = chart_config.get("query")
    existing_title = chart_config.get("title")
    table_metadata = get_table_metadata(table_name)

    # Generate a query
    gpt = GPTLLM(chat_id, user)
    chart_config["query"] = await gpt.generate_query_for_chart(msg, table_name, table_metadata, chart_type, existing_query)

    # Execute query
    results = execute_select_query(chart_config["query"])

    # Transform query data to specific chart
    formatter = NivoAssistant(chart_type)
    chart_config["nivoConfig"]["data"] = formatter.format_data(results)

    # Generate a title for the chart
    chart_config["title"] = await gpt.generate_title_for_chart(msg, table_name, table_metadata, chart_type, chart_config["query"], existing_title)

    # Have GPT determine the settings and styling, ex. which column is the key, and which is the index
    chart_config["nivoConfig"] = await gpt.generate_chart_config(msg, table_name, table_metadata, chart_type, chart_config["query"], \
                                                         chart_config["nivoConfig"])

    return chart_config

def get_table_metadata(table_name: str):
    """Get table metadata"""
    with ClientDatabaseManager() as session:
        metadata_manager = TableMetadataManager(session)
        table_metadata_obj = metadata_manager.get_metadata(table_name)
        table_metadata = table_metadata_obj.to_dict() # Transforms Table_Metadata object to dict
    return table_metadata
