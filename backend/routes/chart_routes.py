from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from databases.database_managers import ClientDatabaseManager
from databases.sql_executor import SQLExecutor
from databases.table_metadata_manager import TableMetadataManager
from llms.gpt import GPTLLM
from utils.nivo_assistant import NivoAssistant
from utils.utils import execute_select_query

import json
import os

chart_router = APIRouter()

class ChartConfigRequest(BaseModel):
    msg: str
    chart_config: dict

@chart_router.get("/charts/types/")
async def get_chart_types():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'chart_types.json')
    with open(config_path, 'r') as file:
        chart_types = json.load(file)
    return chart_types

@chart_router.post("/chart/config/")
async def create_chart_config(request: ChartConfigRequest):
    """Creates or updates a chart configuration using an LLM."""
    msg = request.msg
    chart_config = request.chart_config
    table_name = chart_config.get("table")
    chart_type = chart_config.get("type")
    existing_query= chart_config.get("query")  # If chart is already created updated  TODO
    table_metadata = get_table_metadata(table_name)

    # Generate a query
    gpt = GPTLLM(user_id=1)  # TODO: make sure user_id is dynamically fetched
    chart_config["query"] = gpt.generate_query_for_chart(msg, table_name, table_metadata, chart_type, existing_query)

    # Execute query
    results = execute_select_query(chart_config["query"])

    # Transform query data to specific chart
    formatter = NivoAssistant(chart_type)
    chart_config["nivoConfig"]["data"] = formatter.format_data(results)

    # Have GPT determine the settings and styling, ex. which column is the key, and which is the index
    chart_config["nivoConfig"] = gpt.generate_chart_config(msg, table_name, table_metadata, chart_type, chart_config["query"], \
                                                         chart_config["nivoConfig"])

    print('CHART CONFIG', json.dumps(chart_config))
    return json.dumps(chart_config)

def get_table_metadata(table_name: str):
    """Get table metadata"""
    with ClientDatabaseManager() as session:
        metadata_manager = TableMetadataManager(session)
        table_metadata_obj = metadata_manager.get_metadata(table_name)
        table_metadata = table_metadata_obj.to_dict() # Transforms Table_Metadata object to dict
    return table_metadata