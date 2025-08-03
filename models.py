from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    photo: str = Field(default="No add photo section", max_length=2048)
    name: str = Field(max_length=100)
    job: str = Field(max_length=100)
    phone: str = Field(max_length=18)
    location: str = Field(max_length=255)
    links: str = Field(default="")
    profile: str = Field(default="")
    education: str = Field(default="")
    skills: str = Field(default="")
    courses: Optional[int] = Field(default="")
    experience: Optional[int] = Field(default="")
    languages: str = Field(default="")
    notice: Optional[str] = Field(default="", max_length=150)


class  DownloadToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token : str 
    user_id : int
    created_at : datetime = Field(default_factory=datetime.now)
   


