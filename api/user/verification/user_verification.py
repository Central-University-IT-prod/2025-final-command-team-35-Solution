import redis
from fastapi import APIRouter, Depends
from fastapi import Query
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from api.database import get_db, User_table, get_cache

user_verification = APIRouter(prefix="/user")


@user_verification.get("/verify")
def verify(db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_cache), token: str = Query(...)):
    user_id = redis_client.get(token)
    user = db.query(User_table).get(user_id)
    if not user:
        return  JSONResponse(status_code=404, content={"status": "verification request doesn't exists"})

    user.is_active = True

    db.commit()
    return RedirectResponse("https://prod-team-35-lg7sic6v.REDACTED/login")
