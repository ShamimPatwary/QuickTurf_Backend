from pydantic import BaseModel, EmailStr


class TurfAdminLogin(BaseModel):
    email: EmailStr
    password: str


class TurfAdminChangePassword(BaseModel):
    old_password: str
    new_password: str


class TurfAdminOut(BaseModel):
    id: int
    turf_id: int
    email: EmailStr

    class Config:
        from_attributes = True
