import os
from uuid import UUID, uuid4

import jwt
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .models.base_model import Answer
from .models.response_model import Response_offer
from ...database import get_db, User_table, Mentor_table, Offer_table, Students_table

answer_offer_router = APIRouter()

@answer_offer_router.post("/mentors/offers/{offer_id}", status_code=200, response_model=Response_offer)
def answer_offer(answer: Answer, offer_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    user_data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    mentor = db.query(User_table).filter(User_table.user_id == user_data["sub"]).first()

    mentor_id = db.query(Mentor_table).filter(Mentor_table.user_id == mentor.user_id).first()

    offer = db.query(Offer_table).filter(Offer_table.offer_id == offer_id).first()

    if answer.status:
        # send_email("Your offer was accepted", f"Contact of mentor {mentor.contact}", user.contact)

        new_student = Students_table(id=uuid4(), mentor_id=mentor_id, user_id=offer.user_id)

        offer = db.query(Offer_table).filter(Offer_table.offer_id == answer.offer_id).first()

        offer.status = True

        db.add(new_student)
        db.commit()

        result = \
            {
                "student_id": f"{new_student.id}",
                "mentor_id": f"{new_student.mentor_id}",
                "user_id": f"{new_student.user_id}"
            }

        return result

    else:
        # send_email("Your offer was not accepted", f"Sorry but mentor does not accepted your offer", user.contact)
        offer = db.query(Offer_table).filter(Offer_table.offer_id == answer.offer_id).first()

        offer.status = False

        db.commit()

        return JSONResponse(status_code=204, content={"status": "Mentor does not accepted offer"})