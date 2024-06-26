import json
import os
from typing import Optional

from database.chart_manager import ChartManager
from database.database_manager import DatabaseManager
from database.table_metadata_manager import TableMetadataManager
from fastapi import APIRouter, Depends
from llms.gpt import GPTLLM
from models.chart import Chart, ChartCreate
from models.table_metadata import TableMetadata
from models.user import User
from pydantic import BaseModel
from security import get_current_user
from utils.nivo_assistant import NivoAssistant
from utils.utils import execute_select_query

chart_router = APIRouter()


class ChartConfigRequest(BaseModel):
    chat_id: Optional[int]
    msg: str
    chart_config: dict


@chart_router.get("/charts/types/")
async def get_chart_types(current_user: User = Depends(get_current_user)):
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "chart_types.json"
    )
    with open(config_path, "r") as file:
        chart_types = json.load(file)
    return chart_types


@chart_router.post("/chart/")
async def save_chart(
    chart: ChartCreate, current_user: User = Depends(get_current_user)
):
    with DatabaseManager() as session:
        manager = ChartManager(session)
        highest_order = manager.get_highest_order()
        order = highest_order + 1

        db_chart = Chart(
            dashboard_id=chart.dashboard_id, order=order, config=chart.config
        )

        manager.save_chart(db_chart)


@chart_router.post("/chart/config/")
async def create_chart_config(
    request: ChartConfigRequest, current_user: User = Depends(get_current_user)
):
    """Creates or updates a chart configuration using an LLM."""
    chat_id = request.chat_id
    msg = request.msg
    chart_config = request.chart_config
    table_name = chart_config.get("table", "")
    chart_type = chart_config.get("type")
    nivo_config = chart_config.get("nivoConfig")
    table_metadata = get_table_metadata(table_name)

    gpt = GPTLLM(chat_id, current_user)
    updated_chart_config = await gpt.generate_chart_config(
        msg, table_metadata, chart_type, nivo_config
    )

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


def get_table_metadata(
    table_name: str, current_user: User = Depends(get_current_user)
) -> TableMetadata:
    """Get table metadata"""
    with DatabaseManager() as session:
        metadata_manager = TableMetadataManager(session)
        table_metadata_obj = metadata_manager.get_metadata(table_name)
        table_metadata = (
            table_metadata_obj.to_dict()
        )  # Transforms Table_Metadata object to dict
    return table_metadata
