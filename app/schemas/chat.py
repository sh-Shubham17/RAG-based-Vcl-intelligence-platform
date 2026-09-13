from pydantic import BaseModel

class AskRequest(BaseModel):
    question:str
    source: str | None = None

class Source(BaseModel):
    source:str
    chunk:int
    score:float

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]