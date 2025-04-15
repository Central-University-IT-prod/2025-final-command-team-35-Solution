from fastapi import APIRouter

from .send_request.send_request import send_request_router
from .get_student.get_student import get_student_router
from .get_students.get_students import get_students_router

mentor_router = APIRouter(tags=["Mentors"])

mentor_router.include_router(send_request_router)
mentor_router.include_router(get_students_router)
mentor_router.include_router(get_student_router)