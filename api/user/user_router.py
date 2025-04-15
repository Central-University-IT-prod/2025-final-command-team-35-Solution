from fastapi import APIRouter

from .avatar.get_avatar import get_avatar_router
from .get_mentor_by_id.get_mentors_by_id import get_mentor_router
from .get_mentors_list.get_mentors_list import get_mentors_router
from .get_offer_by_id.get_offer_by_id import get_offer_by_id_router
from .get_offers.get_offers import get_offers_router
from .get_profile.get_profile import get_profile_router
from .sign_in.user_auth_sign_in_post import user_auth_sign_in_router
from .sign_up.user_auth_post import user_auth_post_router
from .update.user_data_update import user_update_data_patch
from .verification.user_verification import user_verification

user_router = APIRouter(tags=["Users"])
user_router.include_router(user_update_data_patch)
user_router.include_router(user_auth_post_router)
user_router.include_router(user_auth_sign_in_router)
user_router.include_router(user_verification)
user_router.include_router(get_offer_by_id_router)
user_router.include_router(get_mentor_router)
user_router.include_router(get_profile_router)
user_router.include_router(get_mentors_router)
user_router.include_router(get_offers_router)
user_router.include_router(get_avatar_router)
