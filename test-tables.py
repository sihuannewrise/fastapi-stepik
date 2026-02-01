from sqlalchemy.schema import CreateTable

from app.models.categories import Category


print(CreateTable(Category.__table__))
