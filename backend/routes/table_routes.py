from fastapi import APIRouter

from databases.database_managers import ClientDatabaseManager
from databases.sql_executor import SQLExecutor
from databases.table_manager import TableManager

table_router = APIRouter()

@table_router.get("/table/columns/")
async def get_table_columns(table_name: str):
    return ['test1','test2','test3']

@table_router.get("/tables/")
async def get_tables():
    with ClientDatabaseManager() as session:
        executor = SQLExecutor(session)
        tables = executor.get_all_table_names_as_list()
    return tables

@table_router.delete("/table/")
async def drop_table(table_name: str):
    manager = TableManager()
    manager.drop_table(table_name)
    return {"message": f"Dropped table {table_name}"}