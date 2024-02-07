from typing import List

from pydantic import BaseModel


class GenerateEmbededTokenRequest(BaseModel):
    workspace_ids: List[str]
    dataset_ids: List[str]
    report_ids: List[str]
