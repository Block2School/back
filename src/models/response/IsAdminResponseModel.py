from pydantic import BaseModel

class IsAdminResponseModel(BaseModel):
    is_admin: bool