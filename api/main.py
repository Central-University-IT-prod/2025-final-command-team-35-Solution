import os
from uuid import uuid4

import bcrypt
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .admin.admin_router import admin_router
from .database import init_db, Admin_table, SessionLocal
from .mentor.mentor_router import mentor_router
from .offer.offer_router import offer_router
from .user.user_router import user_router

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

allowed_origins = [
    "https://prod-team-35-lg7sic6v.REDACTED",
    "http://localhost:5173",
    "http://REDACTED",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Разрешить все домены (или укажите конкретные, например ["https://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  #  Разрешить все заголовки
)

app.include_router(user_router, prefix="/api")
app.include_router(offer_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(mentor_router, prefix="/api")


@app.on_event("startup")
def start():
    init_db()

    db: Session = SessionLocal()

    admin_exists = db.query(Admin_table).filter(Admin_table.login == "admin").first()
    if not admin_exists:
        hashed_password = bcrypt.hashpw("test".encode(), bcrypt.gensalt(rounds=4))

        admin = Admin_table(
            admin_id=uuid4(),
            login="admin",
            password=hashed_password.decode()
        )
        db.add(admin)
        db.commit()
    db.close()

@app.get("/api/ping")
def ping():
    return JSONResponse(status_code=200, content="PROOOOOOOOOOD")

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "REDACTED")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))