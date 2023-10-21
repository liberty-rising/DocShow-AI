from fastapi import File, UploadFile
from io import StringIO
from typing import Any

from charset_normalizer import from_fp
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
    file_type = file.filename.split(".")[-1].lower()

    files = {"processed_file": None, "sample_file_content": None}

    if file_type == 'csv':
        # Use charset-normalizer to detect encoding and read the file content
        cm = from_fp(file.file)
        encoding = cm.best().encoding


        # Read the file content into a pandas DataFrame
        file.file.seek(0)  # Reset file pointer again to ensure correct reading
        df = pd.read_csv(file.file, encoding=encoding, nrows=10)
        print(df.head(1))

        buffer = StringIO()
        df.to_csv(buffer, index=False)

        # Reset the file pointer to the beginning of the file for further use
        file.file.seek(0)

        print(encoding)
        return

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