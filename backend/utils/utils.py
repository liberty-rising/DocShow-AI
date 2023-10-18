from fastapi import File, HTTPException, UploadFile
from io import StringIO
from typing import Any, Dict, Tuple, Union

from backend.databases.db_utils import ClientDatabaseManager, SQLExecutor, TableMetadataManager
from backend.llms.base import BaseLLM
from backend.utils.sql_string_manipulator import SQLStringManipulator
from backend.utils.table_manager import TableManager

import pandas as pd

    
def process_file(file: UploadFile) -> Any:
    """
    Process the uploaded file based on its type.

    Parameters:
        file (UploadFile): The uploaded file.

    Returns:
        Any: Processed content of the file.
    """
    # Find file type by file extension
    file_name = file.filename
    file_type = file_name.split(".")[-1].lower()

    files = {"processed_file": None, "sample_file_content": None}

    if file_type == 'csv':
        df = pd.read_csv(file.file, nrows=10)
        buffer = StringIO()
        df.to_csv(buffer, index=False)

        files["processed_file"] = file
        files["sample_file_content"] = buffer.getvalue()

    elif file_type == 'pdf':
        # PDF processing logic here
        pass
    elif file_type in ['img','jpg','jpeg','png']:
        # Image processing logic here
        pass
    else:
        raise ValueError("Unsupported file type")
    
    return files["processed_file"], files["sample_file_content"]

def save_to_data_lake(file: UploadFile = File(...)):
    pass