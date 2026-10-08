from fastapi import APIRouter, Depends,status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.promocode import PromoCodeModel
from database import get_async_db


router = APIRouter(prefix="/promocodes")


@router.delete("/{promocode_id}")
async def delete_promo(
    promocode_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    stmt = select(PromoCodeModel).where(
        PromoCodeModel.id == promocode_id,
        PromoCodeModel.is_active.is_(True)
    ).limit(1)
    promo = (await db.scalars(stmt)).first()
    if promo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode not found or inactive")

    promo.is_active = False
    await db.commit()
    return {"status": "success", "message": "Promocode marked as inactive"}
