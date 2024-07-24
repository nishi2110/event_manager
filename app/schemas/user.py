from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: constr(regex=r'^[a-zA-Z0-9_]+$', min_length=3, max_length=20)
    password: constr(min_length=8)
