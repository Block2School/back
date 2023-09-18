from pydantic import BaseModel

class SubmitChallengeResponseModel(BaseModel):
    success: bool
    output: str
    expected_output: str
    error_description: str