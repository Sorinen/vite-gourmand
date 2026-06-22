from pydantic import BaseModel


class MenuBase(BaseModel):
    titre: str
    description: str
    nombre_personnes_min: int
    prix_base: float
    conditions: str
    stock_disponible: int
    actif: bool
    theme_id: int
    regime_id: int


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: int

    class Config:
        from_attributes = True