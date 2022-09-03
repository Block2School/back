from pydantic import BaseModel
from models.response.AccountResponseModel import AccountResponseModel

class AccountResponseModelList(BaseModel):
    data: list[AccountResponseModel]