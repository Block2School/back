from pydantic import BaseModel

class TestChallengeResponseModel(BaseModel):
    success: bool
    output: str
    error_description: str
    input: str
    expected_output: str