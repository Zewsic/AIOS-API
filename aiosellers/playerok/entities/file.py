from __future__ import annotations

from dataclasses import dataclass

from ..schemas.basic import File as SchemaFile


@dataclass(slots=True)
class File:
    id: str
    url: str
    filename: str | None = None
    mime: str | None = None

    @classmethod
    def from_schema(cls, f: SchemaFile) -> "File":
        return cls(id=f.id, url=f.url, filename=f.filename, mime=f.mime)
