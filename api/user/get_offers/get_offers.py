import os
from typing import List

import jwt
from fastapi import APIRouter
from fastapi.params import Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from .response_model import Response_offer

from ...database import get_db, Offer_table

get_offers_router = APIRouter()

@get_offers_router.get("/user/offers", status_code=200, response_model=List[Response_offer])
def get_mentors(db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    offers = db.query(Offer_table).filter(Offer_table.user_id == data["sub"]).all()

    result = [
        {
            "mentor_id": str(offer.mentor_id),
            "user_id": str(offer.user_id),
            "message": offer.message,
            "status": offer.status,
            "date": offer.date.isoformat()
        }
        for offer in offers
    ]

    return result