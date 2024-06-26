from typing import List

import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from utils.sql_string_manager import SQLStringManager


class SQLExecutor:
    def __init__(self, session: Session):
        self.session = session
        self.database_type = "postgres"
        self.sql_string_manager = SQLStringManager()

    def append_df_to_table(self, df: pd.DataFrame, table_name: str):
        try:
            df.to_sql(table_name, self.session.bind, if_exists="append", index=False)
        except Exception as e:
            self.session.rollback()
            print(
                f"An error occurred while appending data to table {table_name}: {str(e)}"
            )
            raise

    def create_table_for_data_profile(
        self, org_id: int, table_name: str, column_names_and_types: dict
    ):
        """Creates a table for a data profile."""
        try:
            create_query = (
                self.sql_string_manager.generate_create_query_for_data_profile_table(
                    table_name, column_names_and_types
                )
            )
            self.session.execute(text(create_query))
            self.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            raise

    def execute_create_query(self, create_query: str):
        try:
            self.session.execute(text(create_query))
            self.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            raise

    def execute_select_query(self, query: str, format_as_dict: bool = True):
        try:
            result_proxy = self.session.execute(text(query))
            # Fetch all results
            result_set = result_proxy.fetchall()

            if format_as_dict:
                # Convert to a list of dictionaries
                result = [dict(row) for row in result_set]
                return result

            return result_set
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def drop_table(self, table_name: str):
        try:
            drop_query = text(f"DROP TABLE {table_name};")
            self.session.execute(drop_query)
            self.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            raise

    def generate_query_for_all_table_names(self):
        if self.database_type == "sqlite":
            return "SELECT name FROM sqlite_master WHERE type='table';"
        elif self.database_type == "postgres":
            return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        else:
            return ""

    def get_all_table_names_as_str(self) -> str:
        try:
            # Using the engine from the session to get table names
            table_names = self.get_all_table_names_as_list()
            table_names_str = ", ".join(table_names)
            return table_names_str
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def get_all_table_names_as_list(self) -> List:
        try:
            # Using the engine from the session to get table names
            table_names: List = self.session.bind.table_names()
            return table_names
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def get_table_columns(self, table_name: str) -> List:
        try:
            engine = self.session.bind
            inspector = inspect(engine)
            columns = inspector.get_columns(table_name)
            column_names = [column["name"] for column in columns]
            return column_names
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
