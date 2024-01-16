from database.database_manager import DatabaseManager
from database.table_manager import TableManager
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from llms.base import BaseLLM
from llms.utils import get_llm_sql_object
from models.user import User
from security import get_current_user
from utils.utils import process_file, save_to_data_lake

file_router = APIRouter()


@file_router.get("/encodings/")
async def get_encodings(
    file_type: str = "", current_user: User = Depends(get_current_user)
):
    encodings = {"csv": ["utf_8", "ascii", "latin_1", "utf_16", "ANSI"], "pdf": []}
    return encodings.get("csv", None)


@file_router.get("/file_types/")
async def get_file_types(current_user: User = Depends(get_current_user)):
    return ["csv", "pdf"]


@file_router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    extra_desc: str = Form(default=""),
    is_new_table: bool = Form(default=False),
    encoding: str = Form(default=""),
    llm: BaseLLM = Depends(get_llm_sql_object),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a file and optionally include a message to clarify user data for the LLM.

    Parameters:
        file (UploadFile, required): The file to be uploaded and processed.
        extra_desc (str, optional): An optional message sent to the LLM to clarify the data from the user.
        is_new_table (bool, optional): Indicates whether the table is new. Defaults to False.
        encoding (str, optional): Indicates the encoding of the file. Useful for CSVs.
        llm (BaseLLM, required): An instance of a Language Learning Model (LLM), obtained through dependency injection. Responsible for generating the SQL table.

    Returns:
        JSONResponse: A JSON response containing either a success message and result or an error message.
    """
    try:
        # Process the file to get the sample content
        processed_df, sample_content, header = process_file(file, encoding)

        # Instantiate TableManager
        with DatabaseManager() as session:
            table_manager = TableManager(session, llm)

            # Create new table if necessary
            if is_new_table:
                create_table_query = table_manager.create_table_with_llm(
                    sample_content, header, extra_desc
                )
                table_manager.create_table_desc_with_llm(
                    create_table_query, sample_content, extra_desc
                )

            # Append file to table
            table_name = table_manager.determine_table(sample_content, extra_desc)
            table_manager.append_to_table(processed_df, table_name)

            # Optionally, save the file to a data lake
            save_to_data_lake(file)

        return JSONResponse(
            content={"message": "File processed successfully"}, status_code=200
        )

    except HTTPException as e:
        # Specific error handling for HTTP exceptions
        return JSONResponse(
            content={"message": f"HTTP Exception: {e.detail}"},
            status_code=e.status_code,
        )

    except Exception as e:
        # General error handling
        return JSONResponse(
            content={"message": f"An error occured: {str(e)}"}, status_code=500
        )
