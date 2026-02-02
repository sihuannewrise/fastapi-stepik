# python -m app.models.categories

from sqlalchemy.schema import CreateTable
from app.models.products import Product
print(CreateTable(Category.__table__))
print(CreateTable(Product.__table__))
