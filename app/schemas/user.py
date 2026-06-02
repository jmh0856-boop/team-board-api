from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBaseResponse(BaseModel):
    """회원가입 응답 스키마"""

    success: bool = True
    data: UserResponse | None = None
    message: str = "요청 성공"
