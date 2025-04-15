import datetime
import os
from uuid import uuid4

import jwt
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, User_table, Offer_table, Mentor_table

get_offers_router = APIRouter()

@get_offers_router.get("/mentors/offer")
def post_offer(db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    user_data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    user = db.query(User_table).filter(User_table.user_id == user_data["sub"]).first()
    mentor = db.query(Mentor_table).filter(Mentor_table.user_id == user.user_id).first()

    offers = db.query(Offer_table).filter(Offer_table.mentor_id == mentor.mentor_id).all()

    # send_email("New offer", f"You have received an offer from {user.contact}", mentor_contact.contact)

    result = [
        {
            "offer_id": f"{new_offer.offer_id}",
            "mentor_id": f"{new_offer.mentor_id}",
            "user_id": f"{new_offer.user_id}",
            "message": f"{new_offer.message}",
            "date": new_offer.date
        }
        for new_offer in offers]
    return result
