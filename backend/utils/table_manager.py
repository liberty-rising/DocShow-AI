from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse
from databases.db_utils import ClientDatabaseManager, SQLExecutor, TableMetadataManager
from llms.base import BaseLLM
from utils.sql_string_manipulator import SQLStringManipulator

class TableManager:
    def __init__(self, database: str, llm: BaseLLM):
        """database is app or client"""
        self.database = database
        self.llm = llm

    def create_table_with_llm(self, sample_content: str, extra_desc: str):
        """
        Creates a table using an LLM based on sample file content and a message.

        Parameters:
        - sample_file_content (str): The sample file content used to create the table.
        - extra_desc (str): Additional message to give context to LLM for table creation.

        Returns:
        - create_query: str containing the SQL create table query if successful, None otherwise.
        """
        try:
            with ClientDatabaseManager() as conn:
                sql_executor = SQLExecutor(conn)
                table_names = sql_executor.get_all_table_names()
                
            raw_create_query = self.llm.generate_create_statement(sample_content, table_names, extra_desc)

            create_query = SQLStringManipulator(raw_create_query).extract_sql_query_from_text()  # Just in case

            if SQLStringManipulator(create_query).is_valid_create_table_query():  # Checks if the query is valid
                with ClientDatabaseManager() as conn:
                    sql_executor = SQLExecutor(conn)
                    sql_executor.execute_create_query(create_query)
                return create_query
        except Exception as e:
            # Log the error message here
            print(f"An error occurred while creating the table: {str(e)}")
            return None
    
    def create_table_desc_with_llm(self, create_query: str, sample_content: str, extra_desc: str):
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
            description = self.llm.generate_table_desc(create_query, sample_content, extra_desc)
            
            table_name = SQLStringManipulator(create_query).get_table_from_create_query()
            
            # Store description in separate table
            with TableMetadataManager(database="client") as manager:
                manager.store_table_desc(table_name, create_query, description)

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
        with TableMetadataManager(database="client") as manager:
            table_metadata = manager.get_metadata()
            formatted_table_metadata = manager.format_table_metadata_for_llm(table_metadata)

        table_name = self.llm.fetch_table_name_from_sample(sample_content, extra_desc, formatted_table_metadata)
        return table_name

    def append_to_table(self, processed_file: UploadFile, table_name: str):
        """
        Appends the uploaded file to the given table.
        Uses ClientDatabaseManager for database connection and SQLExecutor for SQL operations.

        Parameters:
        - processed_file (UploadFile): The uploaded file to be appended.
        - sample_content (str): The sample content for table determination.
        - extra_desc (str): Additional metadata or instructions.

        Side-effects:
        - Appends data to the table determined by the LLM.
        - Raises an HTTPException if the table name cannot be determined.
        """

        if table_name:
            with ClientDatabaseManager() as conn:
                sql_executor = SQLExecutor(conn)
                sql_executor.append_csv_to_table(processed_file, table_name)
        else:
            raise HTTPException(status_code=400, detail="Could not determine table name")

    def drop_table(self, table_name: str):
        # Logic to drop a table
        pass

    def get_table_metadata(self):
        # Logic to get metadata of a table
        pass

    def list_all_tables(self):
        # Logic to list all tables
        pass

    def validate_table_exists(self, table_name: str):
        # Logic to validate if a table exists
        pass