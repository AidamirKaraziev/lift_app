import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from fastapi.params import Path

# from app.api import deps
from app.core.response import SingleEntityResponse
from app.schemas.token import TokenBase

# from app.schemas.super_users import SuperUserEntrance, SuperUserGet

# from app.getters.super_user import get_super_user
#
# from app.exceptions import UnfoundEntity, InaccessibleEntity
# from app.schemas.super_users import SuperUserRequest
#
# # from app.crud.crud_super_users import crud_super_users
#
# from app.core.security import get_password_hash
# from app.crud.crud_location import crud_location
# from app.exceptions import UnprocessableEntity
# from app.utils.time_stamp import date_from_timestamp
#
# # from app.crud.crud_super_users import crud_super_users
# #
# # from app.getters.super_user import get_super_user_delete

from app.crud.crud_universal_user import crud_universal_users
from app.schemas.universal_user import UniversalUserEntrance, UniversalUserGet

from app.getters.universal_user import get_universal_user

from app.api import deps

from app.core.security import create_token_universal_user

from app.exceptions import UnfoundEntity, InaccessibleEntity, UnprocessableEntity
from app.schemas.universal_user import UniversalUserUpdate

# from backend.app.app.core.response import ListOfEntityResponse, Meta

from app.core.response import ListOfEntityResponse, SingleEntityResponse
from app.core.response import Meta

from app.db.init_db import create_initial_data

PATH_MODEL = "universal_user"
PATH_TYPE_PHOTO = "photo"
PATH_TYPE_IDENTITY_CARD = "identity_card"
PATH_TYPE_QUALIFICATION = "qualification_file"

router = APIRouter()


# GET-MULTY
@router.get('/test-apis/',
            response_model=ListOfEntityResponse,
            name='Тестовые АПИ',
            description='Тестовые Апи',
            tags=['Админ панель / Тест']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_universal_users.get_multi(db=session, page=None))

    data, paginator = crud_universal_users.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_universal_user(datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET
@router.get('/test-api/',
            response_model=SingleEntityResponse[UniversalUserGet],
            name='Тестовые АПИ',
            description='Тестовые Апи',
            tags=['Админ панель / Тест']
            )
def get_data(
        request: Request,
        # current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    D = create_initial_data()
    print(D)

    return SingleEntityResponse(data=D)


if __name__ == "__main__":
    logging.info('Running...')
