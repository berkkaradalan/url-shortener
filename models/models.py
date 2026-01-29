from pydantic import BaseModel, AnyUrl
from datetime import datetime

class ShortenRequest(BaseModel):
    url: AnyUrl

class ShortenResponse(BaseModel):
    short_url: str
    url_id: str
    original_url: str

class URLMapping(BaseModel):
    url_id: str
    long_url: str
    created_at: datetime