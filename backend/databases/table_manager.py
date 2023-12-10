from sqlalchemy.orm import Session
from typing import Optional

import pandas as pd

from fastapi import HTTPException
from databases.sql_executor import SQLExecutor
from databases.table_metadata_manager import TableMetadataManager
from llms.base import BaseLLM
from models.organization_table_map import OrganizationTableMap
from utils.sql_string_manipulator import SQLStringManipulator


class TableManager:
    """
    Manages table operations.
    Has functions that integrate a Large Language Model (LLM) and SQLExecutor.

    Attributes:
        llm (BaseLLM): Instance of a Large Language Model for SQL operations.
        session (Optional[str]): The session used for database operations.
    """

    def __init__(self, llm: BaseLLM = None, session: Optional[Session] = None):
        self.llm = llm
        self.session = session

    def _map_table_to_org(
        self, org_id: int, table_name: str, alias: Optional[str] = None
    ):
        """Maps a table to an organization."""
        try:
            if self.session:
                self.session.add(
                    OrganizationTableMap(table_name=table_name, organization_id=org_id)
                )
                self.session.commit()
        except Exception as e:
            self.session.rollback() if self.session else None
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def create_table_with_llm(self, sample_content: str, header: str, extra_desc: str):
        """
        Creates a table using an LLM based on sample file content and a message.

        Parameters:
        - sample_file_content (str): The sample file content used to create the table.
        - extra_desc (str): Additional message to give context to LLM for table creation.

        Returns:
        - create_query: str containing the SQL create table query if successful, None otherwise.
        """
        try:
            sql_executor = SQLExecutor(self.session)
            table_names = sql_executor.get_all_table_names_as_str()

            raw_create_query = self.llm.generate_create_statement(
                sample_content, header, table_names, extra_desc
            )

            create_query = SQLStringManipulator(
                raw_create_query
            ).extract_sql_query_from_text()  # Just in case

            if SQLStringManipulator(
                create_query
            ).is_valid_create_table_query():  # Checks if the query is valid
                sql_executor = SQLExecutor(self.session)
                sql_executor.execute_create_query(create_query)
                return create_query
        except Exception as e:
            # Log the error message here
            print(f"An error occurred while creating the table: {str(e)}")
            return None

    def create_table_desc_with_llm(
        self, create_query: str, sample_content: str, extra_desc: str
    ):
        """
        Fetches and stores the description of a table created in LLM based on the CREATE TABLE query,
        sample file content, and a message.

        Parameters:
        - create_query (str): The CREATE TABLE query used to create the table.
        - sample_content (str): Sample file content used in table creation.
        - extra_desc (str): Additional message to give context to LLM for generating the table description.
        """
        try:
            # API call to generate and fetch table description
            description = self.llm.generate_table_desc(
                create_query, sample_content, extra_desc
            )

            table_name = SQLStringManipulator(
                create_query
            ).get_table_from_create_query()

            # Store description in separate table
            manager = TableMetadataManager(self.session)
            manager.add_table_metadata(table_name, create_query, description)

        except Exception as e:
            # Log the error message here
            print(f"An error occurred while fetching table description: {str(e)}")
            return None

    def determine_table(self, sample_content: str, extra_desc: str) -> str:
        """
        Determines the appropriate table based on sample data and a message, returns that table's name.

        Parameters:
        - sample_content (str): The sample content for table determination.
        - extra_desc (str): Additional metadata or instructions.

        Returns:
        - table_name: str containing the table's name.
        """
        manager = TableMetadataManager(self.session)
        table_metadata = manager.get_metadata()
        formatted_table_metadata = manager.format_table_metadata_for_llm(table_metadata)

        table_name: str = self.llm.fetch_table_name_from_sample(
            sample_content, extra_desc, formatted_table_metadata
        )
        return table_name

    def create_table_from_df(self, df: pd.DataFrame, org_id: int, table_name: str):
        try:
            executor = SQLExecutor(self.session)
            executor.append_df_to_table(df, org_id, table_name)
            self._map_table_to_org(org_id, table_name)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def create_table_from_query(self, query: str):
        executor = SQLExecutor(self.session)
        executor.execute_create_query(query)

    def append_to_table(self, processed_df: pd.DataFrame, table_name: str):
        """
        Appends the uploaded file to the given table.
        Uses DatabaseManager for database connection and SQLExecutor for SQL operations.

        Parameters:
        - processed_file (UploadFile): The uploaded file to be appended.
        - sample_content (str): The sample content for table determination.
        - extra_desc (str): Additional metadata or instructions.

        Side-effects:
        - Appends data to the table determined by the LLM.
        - Raises an HTTPException if the table name cannot be determined.
        """

        if table_name:
            sql_executor = SQLExecutor(self.session)
            sql_executor.append_df_to_table(processed_df, table_name)
        else:
            raise HTTPException(
                status_code=400, detail="Could not determine table name"
            )

    def drop_table(self, table_name: str):
        # Logic to drop a table
        try:
            executor = SQLExecutor(self.session)
            executor.drop_table(table_name)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def get_org_tables(self, org_id: int):
        """Returns a list of all of the tables present within the organization."""
        try:
            executor = SQLExecutor(self.session)
            tables = executor.get_org_tables(org_id)
            return tables
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def get_table_columns(self, table_name: str):
        """Returns a list of all of the columns present within the table."""
        try:
            executor = SQLExecutor(self.session)
            columns = executor.get_table_columns(table_name)
            return columns
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def get_table_metadata(self):
        # Logic to get metadata of a table
        pass

    def list_all_tables(self):
        # Logic to list all tables
        pass

    def validate_table_exists(self, table_name: str):
        # Logic to validate if a table exists
        pass
