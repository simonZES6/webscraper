from pydantic import BaseModel, HttpUrl

class User(BaseModel):
    name: str = "default_name"   
    email: str
    password: str
    url: HttpUrl