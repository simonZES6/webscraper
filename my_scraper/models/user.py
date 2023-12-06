from pydantic import BaseModel

class User(BaseModel):
    name: str = "default_name"   
    email: str
    password: str
    url: str