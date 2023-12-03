from fastapi import APIRouter, Depends
from security import get_current_user

from databases.database_manager import DatabaseManager
from databases.sql_executor import SQLExecutor
from databases.table_manager import TableManager
from databases.table_metadata_manager import TableMetadataManager
from models.user import User

table_router = APIRouter()


@table_router.get("/table/columns/")
async def get_table_columns(
    table_name: str, current_user: User = Depends(get_current_user)
):
    manager = TableManager()
    columns = manager.get_table_columns(table_name)
    return columns


@table_router.get("/table/metadata/")
async def get_table_metadata(
    table_name: str, current_user: User = Depends(get_current_user)
):
    with DatabaseManager() as session:
        manager = TableMetadataManager(session)
        metadata = manager.get_metadata(table_name)
    return metadata


@table_router.get("/tables/")
async def get_tables(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        executor = SQLExecutor(session)
        tables = executor.get_all_table_names_as_list()
    return tables


@table_router.get("/tables/metadata/")
async def get_all_table_metadata(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        manager = TableMetadataManager(session)
        metadata = manager.get_all_metadata()
    return metadata


@table_router.delete("/table/")
async def drop_table(table_name: str, current_user: User = Depends(get_current_user)):
    manager = TableManager()
    manager.drop_table(table_name)
    return {"message": f"Dropped table {table_name}"}
