from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings


from app.models.super_users import SuperUser
from app.schemas.super_users import SuperUserGet
from app.utils.time_stamp import to_timestamp

from app.getters.location import get_location

from app.schemas.super_users import SuperUserGetDelete


def get_super_user(super_user: SuperUser, request: Optional[Request],
                   config: Settings = settings) -> Optional[SuperUserGet]:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if super_user.photo is not None:
            super_user.photo = url + str(super_user.photo)
        else:
            super_user.photo = None
    super_user.birthday = to_timestamp(super_user.birthday)
    return SuperUserGet(
        id=super_user.id,
        name=super_user.name,
        email=super_user.email,
        contact_phone=super_user.contact_phone,
        birthday=super_user.birthday,
        photo=super_user.photo,
        location_id=get_location(super_user.location) if super_user.location is not None else None,
        is_super_user=super_user.is_super_user
    )


def get_super_user_delete(super_user: SuperUser, request: Optional[Request],
                          config: Settings = settings) -> Optional[SuperUserGetDelete]:
    if super_user.birthday is not None:
        super_user.birthday = to_timestamp(super_user.birthday)
    else:
        super_user.birthday = None
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if super_user.photo is not None:
            super_user.photo = url + str(super_user.photo)
        else:
            super_user.photo = None
    return SuperUserGetDelete(
        id=super_user.id,
        name=super_user.name,
        email=super_user.email,
        contact_phone=super_user.contact_phone,
        birthday=super_user.birthday,
        photo=super_user.photo,
        # location_id=get_location(super_user.location) if super_user.location is not None else None,
        location=super_user.location_id,
        is_super_user=super_user.is_super_user
    )
