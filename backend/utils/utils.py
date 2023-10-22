from fastapi import File, UploadFile
from io import StringIO
from typing import Any

import pandas as pd


def process_file(file: UploadFile, encoding: str, is_header: bool) -> Any:
    """
    Process the uploaded file based on its type.

    Parameters:
        file (UploadFile): The uploaded file.
        encoding (str): The encoding of the file.

    Returns:
        Any: Processed content of the file.
    """
    # Find file type by file extension
    file_type = file.filename.split(".")[-1].lower()

    files = {"processed_df": None, "sample_file_content": None}

    if file_type == 'csv':
        df = pd.read_csv(file.file, encoding=encoding, header=0 if is_header else None)

        # Get the first 10 lines
        sampled_df = df.head(10)

        buffer = StringIO()
        sampled_df.to_csv(buffer, index=False)

        # Reset the file pointer to the beginning of the file for further use
        file.file.seek(0)

        files["processed_df"] = df
        files["sample_file_content"] = buffer.getvalue()

    elif file_type == 'pdf':
        # PDF processing logic here
        pass
    elif file_type in ['img','jpg','jpeg','png']:
        # Image processing logic here
        pass
    else:
        raise ValueError("Unsupported file type")
    
    return files["processed_df"], files["sample_file_content"]

def save_to_data_lake(file: UploadFile = File(...)):
    pass