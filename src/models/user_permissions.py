from sqlmodel import Field, SQLModel

class UserPermissions(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    permission_id: int = Field(foreign_key="permissions.id", primary_key=True)