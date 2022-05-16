from pydantic import BaseModel

class DataListResponseModel(BaseModel):
    data: list[dict]