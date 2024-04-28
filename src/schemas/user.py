from pydantic import BaseModel, Field, UUID4
from datetime import datetime, date


class UserBase(BaseModel):
    username: str = Field(..., description="The username of the current user")


class UserLogin(UserBase):
    password: str = Field(
        ..., title="Password", description="Password of length 8 or more", min_length=8
    )


class UserUpdate(BaseModel):
    password: str = Field(
        ..., title="Password", description="Password of length 8 or more", min_length=8
    )


class UserSchema(BaseModel):
    id: UUID4 = Field(..., title="ID", description="ID of the user record")
    username: str = Field(
        ..., title="Username", description="The Username of the current user"
    )
    first_name: str = (
        Field(..., title="First Name", description="First Name of the user"),
    )
    last_name: str = (
        Field(..., title="Last Name", description="Last Name of the user"),
    )
    is_active: bool = Field(..., title="Is Active", description="Status of the user")
    # profile: str | None = Field(title="Profile",
    #                             description="Profile connected to the user", default=None)
    created_at: datetime = (
        Field(title="Created At", description="Date and time user was created at"),
    )
    updated_at: datetime = (
        Field(title="Updated At", description="Date and time user was updated at"),
    )

    # class Config:
    #     orm_mode = True


# define success and error responses for views and multidata


class SuccessResponse(BaseModel):
    message: str = Field(
        title="Message", default="success", description="The success message"
    )
    data: UserSchema = Field(..., title="User's data", description="The user's data")


class MultiSuccessResponse(BaseModel):
    message: str = Field(
        title="Message", default="success", description="The success message"
    )
    data: list[UserSchema] = Field(
        title="Users data", description="The list of users data", default=[]
    )


class ErrorResponse(BaseModel):
    detail: str = Field(
        title="Detail", default="error", description="The error message"
    )
