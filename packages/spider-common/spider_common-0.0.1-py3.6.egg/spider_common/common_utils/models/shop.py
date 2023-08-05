from scrapy.item import Field
from .base import BaseModel


class ShopModel(BaseModel):
    city = Field()
    address = Field()
    cellphone = Field()
    telephone = Field()
