from pydantic import BaseModel


class SectorBase(BaseModel):
    name: str = None
