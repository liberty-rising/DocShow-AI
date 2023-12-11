from csv import Sniffer
from fastapi import File, UploadFile
from io import StringIO
from typing import Any, Dict, Optional

import logging
import os
import pandas as pd
import sys

from databases.database_manager import DatabaseManager
from databases.table_manager import TableManager


def execute_select_query(query: str):
    with DatabaseManager() as session:
        table_manager = TableManager(session)
        results = table_manager.execute_select_query(query)
    return results


def process_file(file: UploadFile, encoding: str) -> Any:
    """
    Process the uploaded file based on its type.

    Parameters:
        file (UploadFile): The uploaded file.
        encoding (str): The encoding of the file.

    Returns:
        Any: Processed content of the file.
    """
    if file.filename is None:
        raise ValueError("File must have a filename")

    # Find file type by file extension
    file_type = file.filename.split(".")[-1].lower()

    # Define the dictionary with types for values
    files: Dict[str, Optional[str]] = {
        "processed_df": None,
        "sample_file_content_str": None,
        "header_str": None,
    }

    if file_type == "csv":
        # Sniff the first 1024 bytes to check for a header
        sample = file.file.read(4096).decode(encoding)
        has_header = Sniffer().has_header(sample)

        # Reset the file pointer
        file.file.seek(0)

        # Read the entire file into a DataFrame
        df = pd.read_csv(file.file, encoding=encoding, header=0 if has_header else None)
        df.columns = map(str.lower, df.columns)  # make all columns lowercase

        # Store the header as a string, if it exists
        header_str = ",".join(df.columns) if has_header else None

        # Get the first 10 lines
        sampled_df = df.head(10)

        buffer = StringIO()
        sampled_df.to_csv(buffer, index=False)

        # Reset the file pointer to the beginning of the file for further use
        file.file.seek(0)

        files["processed_df"] = df
        files["sample_file_content_str"] = buffer.getvalue()
        files["header_str"] = header_str

    elif file_type == "pdf":
        # PDF processing logic here
        pass
    elif file_type in ["img", "jpg", "jpeg", "png"]:
        # Image processing logic here
        pass
    else:
        raise ValueError("Unsupported file type")

    return files["processed_df"], files["sample_file_content"], files["header_str"]


def save_to_data_lake(file: UploadFile = File(...)):
    pass


def get_app_logger(name):
    logger = logging.getLogger(name)

    # Set log level based on the environment
    log_level = logging.DEBUG if os.getenv("APP_ENV") == "development" else logging.INFO

    logger.setLevel(log_level)

    # You can add handlers, formatters here if needed
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    return logger
