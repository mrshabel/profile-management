from pydantic import UUID4, BaseModel
from pydantic import Field
from .user import UserSchema


class TokenData(BaseModel):
    id: UUID4


class UserData(UserSchema):
    password: str = Field(
        ..., title="Password", description="Password of length 8 or more", min_length=8
    )


class UserSignUp(BaseModel):
    username: str = Field(..., title="Username", description="Username of the user")
    first_name: str = Field(
        ..., title="First Name", description="First Name of the user"
    )
    last_name: str = Field(..., title="Last Name", description="Last Name of the user")
    password: str = Field(
        ..., title="Password", description="Password of length 8 or more", min_length=8
    )


class SuccessResponseForLogin(BaseModel):
    message: str = Field(
        title="Message", default="success", description="The success message"
    )
    data: UserSchema = Field(..., title="User's data", description="The user's data")
    token: str = Field(..., title="Token", description="Access token")


class SuccessResponseForSignup(BaseModel):
    message: str = Field(
        title="Message", default="success", description="The success message"
    )
