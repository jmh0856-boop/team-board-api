from pydantic import AliasPath, BaseModel, ConfigDict, Field


class TagResponse(BaseModel):
    """태그 응답 스키마"""

    tag_id: int = Field(validation_alias=AliasPath("id"))
    name: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TagCreate(BaseModel):
    """태그 생성 요청 스키마"""

    names: list[str]  # 여러 태그 한번에 등록


class TagUpdate(BaseModel):
    """태그 수정 요청 스키마"""

    names: list[str]  # 태그 목록 전체 교체


class TagBaseResponse(BaseModel):
    """태그 응답 스키마"""

    success: bool = True
    data: list[TagResponse] = []
    message: str = "요청 성공"
