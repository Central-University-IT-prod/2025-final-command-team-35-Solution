from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, User_table, Mentor_table
from .response_model import Response_mentor

get_mentor_router = APIRouter()

@get_mentor_router.get("/mentors/{mentor_id}", status_code=200, response_model=Response_mentor)
def get_mentor(mentor_id: UUID, db: Session = Depends(get_db)):
    mentor = db.query(Mentor_table).filter(Mentor_table.mentor_id == mentor_id).first()

    if not mentor:
        return JSONResponse(status_code=404, content={"status": "Mentor not found"})

    user = db.query(User_table).filter(User_table.user_id == mentor.user_id).first()

    result = \
        {
            "mentor_id": str(mentor.mentor_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "direction": mentor.direction,
            "about": user.about,
            "contact": user.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(user.user_id)}" if user.avatar is not None else None
        }


    return result