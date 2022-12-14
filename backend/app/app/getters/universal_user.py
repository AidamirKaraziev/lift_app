from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings


# from app.schemas.super_users import SuperUserGet
from app.utils.time_stamp import to_timestamp

from app.getters.location import get_location

from app.getters.role import get_roles
from app.getters.working_specialty import get_working_specialty
from app.models import UniversalUser
from app.schemas.universal_user import UniversalUserGet

from app.getters.company import get_company

from app.getters.division import get_division


def get_universal_user(universal_user: UniversalUser, request: Optional[Request],
                       config: Settings = settings) -> Optional[UniversalUserGet]:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if universal_user.photo is not None:
            universal_user.photo = url + str(universal_user.photo)
        else:
            universal_user.photo = None
        if universal_user.identity_card is not None:
            universal_user.identity_card = url + str(universal_user.identity_card)
        else:
            universal_user.identity_card = None
        if universal_user.qualification_file is not None:
            universal_user.qualification_file = url + str(universal_user.qualification_file)
        else:
            universal_user.qualification_file = None

    universal_user.birthday = to_timestamp(universal_user.birthday)
    universal_user.date_of_employment = to_timestamp(universal_user.date_of_employment)
    return UniversalUserGet(
        id=universal_user.id,
        name=universal_user.name,
        email=universal_user.email,
        contact_phone=universal_user.contact_phone,
        birthday=universal_user.birthday,
        photo=universal_user.photo,
        location_id=get_location(universal_user.location) if universal_user.location is not None else None,
        role_id=get_roles(universal_user.role) if universal_user.role is not None else None,
        working_specialty_id=get_working_specialty(universal_user.working_specialty)
        if universal_user.working_specialty is not None else None,
        identity_card=universal_user.identity_card,
        qualification_file=universal_user.qualification_file,
        company_id=get_company(company=universal_user.company, request=request)
        if universal_user.company is not None else None,
        division_id=get_division(obj=universal_user.division, request=request)
        if universal_user.division is not None else None,
        date_of_employment=universal_user.date_of_employment,
        is_actual=universal_user.is_actual
    )
