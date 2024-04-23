from pydantic import UUID4, BaseModel
from pydantic import Field
from .user import UserSchema

class TokenData(BaseModel):
    id: UUID4

class SuccessResponseForLogin(BaseModel):
    message: str = Field(title="Message",
                         default="success", description="The success message")
    data: UserSchema = Field(..., title="User's data",
                             description="The user's data")
    token: TokenData