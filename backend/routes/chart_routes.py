from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from databases.chart_manager import ChartManager
from databases.database_managers import ClientDatabaseManager
from databases.table_metadata_manager import TableMetadataManager
from llms.gpt import GPTLLM
from models.app.user import User
from models.client.chart import Chart, ChartCreate
from security import get_current_user
from utils.nivo_assistant import NivoAssistant
from utils.utils import execute_select_query

import json
import os

chart_router = APIRouter()

class ChartConfigRequest(BaseModel):
    chat_id: Optional[int]
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
    nivo_config = chart_config.get("nivoConfig")
    table_metadata = get_table_metadata(table_name)

    gpt = GPTLLM(chat_id, user)
    updated_chart_config = await gpt.generate_chart_config_v2(msg, table_metadata, chart_type, nivo_config)

    # Make sure configuration holds data needed for specific chart type
    formatter = NivoAssistant(chart_type)
    updated_nivo_config = updated_chart_config.get("nivoConfig")
    formatted_nivo_config = formatter.format_config(updated_nivo_config)
    updated_chart_config["nivoConfig"] = formatted_nivo_config

    # Execute query
    results = execute_select_query(updated_chart_config["query"])

    # Transform query data to specific chart and add to configuration
    nivo_data = formatter.format_data(results)
    updated_chart_config["nivoConfig"]["data"] = nivo_data
    print(updated_chart_config)

    return updated_chart_config, gpt.chat_id

def get_table_metadata(table_name: str):
    """Get table metadata"""
    with ClientDatabaseManager() as session:
        metadata_manager = TableMetadataManager(session)
        table_metadata_obj = metadata_manager.get_metadata(table_name)
        table_metadata = table_metadata_obj.to_dict() # Transforms Table_Metadata object to dict
    return table_metadata
