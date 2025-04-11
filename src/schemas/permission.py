from sqlmodel import SQLModel

class PermissionsResponse(SQLModel):
    id: int
    name:str
    prefix: str
    module: str
    status: bool