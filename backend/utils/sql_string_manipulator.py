from typing import Optional

import re


class SQLStringManipulator:
    """
    A class for manipulating SQL query strings.
    
    This class provides utility methods for tasks such as extracting table names,
    validating SQL queries, and extracting SQL queries from text. It does not 
    execute the SQL queries but rather provides a way to work with SQL string data.
    
    Attributes:
        query_str (str): The SQL query string to be manipulated.
    
    Methods:
        extract_table_name(): Extracts the table name from the SQL query string.
        is_valid_query(): Validates the SQL query string.
        extract_sql_query_from_text(): Extracts an SQL query from a given text.
    """

    def __init__(self, sql_string: str = ""):
        """
        Initializes an instance of the SQLStringManipulator class with a query string.
        
        Parameters:
            query_str (str): The SQL query string to be manipulated.
        """
        self.sql_string = sql_string
    
    def set_sql_string(self, sql_string: str):
        self.sql_string = sql_string
    
    def get_table_from_create_query(self) -> Optional[str]:
        """
        Extract the table name from a SQL CREATE TABLE query.
        
        Returns:
            str or None: The table name if the query is valid, otherwise None.
        """
        # Use regular expression to extract table name
        match = re.search(r'CREATE TABLE (\w+)', self.sql_string, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return "Invalid CREATE TABLE query"

    def is_valid_create_table_query(self) -> bool:
        """
        Validate if the SQL string is a valid CREATE TABLE query.
        
        Returns:
            bool: True if valid, otherwise False.
        """
        # Remove formatting
        clean_query = self.sql_string.replace("\n", " ").strip()

        pattern = r'^CREATE TABLE .+;\s*$'
        return bool(re.match(pattern, clean_query))
    
    def extract_sql_query_from_text(self) -> Optional[str]:
        """
        Extracts an SQL query from a given text.
        Useful when an LLM produces filler words/introductions when asked to generate SQL code.
        
        Returns:
            str or None: The SQL query if present, otherwise None.
        """
        match = re.findall(r'CREATE TABLE [^;]+;', self.sql_string)
        if match:
            # Extract only the last "CREATE TABLE" statement and add a space after "CREATE TABLE"
            last_statement = match[-1]
            return "CREATE TABLE " + last_statement.split("CREATE TABLE")[-1].strip()