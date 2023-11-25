from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from databases.database_managers import ClientDatabaseManager
from databases.table_metadata_manager import TableMetadataManager
from llms.gpt import GPTLLM

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
    msg = request.msg
    table_name = request.chart_config.get("table")
    chart_type = request.chart_config.get("type")
    existing_query= request.chart_config.get("query")  # If chart is being updated  TODO

    with ClientDatabaseManager() as session:
        metadata_manager = TableMetadataManager(session)
        table_metadata_obj = metadata_manager.get_metadata(table_name)
        table_metadata = table_metadata_obj.to_dict() # Transforms Table_Metadata object to dict

    gpt = GPTLLM(user_id=1)  # TODO: make sure user_id is dynamically fetched
    query = gpt.generate_query_for_chart(msg=msg, table_name=table_name, table_metadata=table_metadata, chart_type=chart_type)

    # Execute query

    # Transform query data to specific chart

    # Have GPT do basic styling of the chart

    # Figure out how not to regenerate a query if all that's needed is styling

    return 'new_chart_config'  # chart config should include query
