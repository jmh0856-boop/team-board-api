from pydantic import AliasPath, BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: int = Field(validation_alias=AliasPath("id"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserBaseResponse(BaseModel):
    """회원가입 응답 스키마"""

    success: bool = True
    data: UserResponse | None = None
    message: str = "요청 성공"
