from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings


# from app.schemas.super_users import SuperUserGet
from app.utils.time_stamp import to_timestamp

from app.getters.location import get_location

from app.getters.role import get_roles
from app.getters.working_specialty import get_working_specialty
from app.models import UniversalUser

from app.schemas.admin import AdminGet


def get_admin(admin: UniversalUser, request: Optional[Request],
              config: Settings = settings) -> Optional[AdminGet]:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if admin.photo is not None:
            admin.photo = url + str(admin.photo)
        else:
            admin.photo = None
    admin.birthday = to_timestamp(admin.birthday)
    return AdminGet(
        id=admin.id,
        name=admin.name,
        email=admin.email,
        contact_phone=admin.contact_phone,
        birthday=admin.birthday,
        photo=admin.photo,
        location_id=get_location(admin.location) if admin.location is not None else None,
        role_id=get_roles(admin.role) if admin.role is not None else None,
        working_specialty_id=get_working_specialty(admin.working_specialty)
        if admin.working_specialty is not None else None,
        identity_card=admin.identity_card,
        # company_id=admin.company_id,
        is_actual=admin.is_actual
    )

