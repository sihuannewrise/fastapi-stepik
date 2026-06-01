# python -m app.models.categories

from sqlalchemy.schema import CreateTable
from app.models.products import Product
from app.models.categories import Category

print(CreateTable(Category.__table__))
print(CreateTable(Product.__table__))
