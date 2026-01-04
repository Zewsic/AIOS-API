from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )


class PageInfo(ApiModel):
    start_cursor: str | None = Field(None, alias="startCursor")
    end_cursor: str | None = Field(None, alias="endCursor")
    has_previous_page: bool | None = Field(None, alias="hasPreviousPage")
    has_next_page: bool | None = Field(None, alias="hasNextPage")


class File(ApiModel):
    id: str = Field(alias="id")
    url: str = Field(alias="url")
    filename: str = Field(alias="filename")
    mime: str = Field(alias="mime")
