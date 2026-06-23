from pydantic import BaseModel


class ThemeBase(BaseModel):
    libelle: str


class ThemeCreate(ThemeBase):
    pass


class Theme(ThemeBase):
    id: int

    class Config:
        from_attributes = True