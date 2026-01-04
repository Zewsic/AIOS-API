import logging

from pydantic import BaseModel, ConfigDict, Field, model_validator

logger = logging.getLogger(__name__)


class ApiModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )


class UnimplementedApiModel(ApiModel):
    model_config = ConfigDict(
        extra="allow",
    )

    @model_validator(mode="before")
    @classmethod
    def _log_unimplemented(cls, data):
        if isinstance(data, dict):
            keys = list(data.keys())
            logger.warning(
                f"Model {cls.__name__} is unimplemented. Received keys: {keys}. "
                "Add these fields to the model if needed."
            )
        return data


class PageInfo(ApiModel):
    start_cursor: str | None = Field(None, alias="startCursor")
    end_cursor: str | None = Field(None, alias="endCursor")
    has_previous_page: bool | None = Field(None, alias="hasPreviousPage")
    has_next_page: bool | None = Field(None, alias="hasNextPage")


class File(ApiModel):
    id: str = Field(alias="id")
    url: str = Field(alias="url")
    filename: str | None = Field(None, alias="filename")
    mime: str | None = Field(None, alias="mime")
