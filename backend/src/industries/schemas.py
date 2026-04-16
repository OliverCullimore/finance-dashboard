from pydantic import BaseModel


class IndustryBase(BaseModel):
    name: str = None
