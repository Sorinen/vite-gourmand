from pydantic import BaseModel


class ImageMenuBase(BaseModel):
    url: str
    ordre: int
    menu_id: int


class ImageMenuCreate(ImageMenuBase):
    pass


class ImageMenu(ImageMenuBase):
    id: int

    class Config:
        from_attributes = True

