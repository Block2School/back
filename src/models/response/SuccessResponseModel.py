from pydantic import BaseModel

class SuccessResponseModel(BaseModel):
    success: str