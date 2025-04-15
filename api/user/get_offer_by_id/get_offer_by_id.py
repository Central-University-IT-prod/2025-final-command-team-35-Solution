import os
from uuid import UUID

import jwt
from fastapi import APIRouter
from fastapi.params import Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from .response_model import Response_offer
from ...database import get_db, Offer_table

get_offer_by_id_router = APIRouter()

@get_offer_by_id_router.get("/user/offers/{id}", status_code=200, response_model=Response_offer)
def get_mentors(offer_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    offer = db.query(Offer_table).filter(Offer_table.user_id == data["sub"], Offer_table.offer_id == offer_id).first()

    result = \
        {
            "mentor_id": str(offer.mentor_id),
            "user_id": str(offer.user_id),
            "message": offer.message,
            "status": offer.status,
            "date": offer.date.isoformat()
        }

    return result