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

from app.exceptions import UnfoundEntity, InaccessibleEntity, UnprocessableEntity
from app.schemas.universal_user import UniversalUserRequest

from app.schemas.universal_user import UniversalUserUpdate

from fastapi import Response, Request
from mimetypes import guess_type

from os.path import isfile

from app.getters.client import get_client
from app.schemas.client import ClientGet

from app.crud.crud_client import crud_client
from app.schemas.client import ClientUpdateSelf

router = APIRouter()


# GET
@router.get('/cp/client/me/',
            response_model=SingleEntityResponse[ClientGet],
            name='Получить данные клиента ',
            description='Получение всех данных профиля клиента по токену',
            tags=['Админ панель / Клиент']
            )
def get_data(
        request: Request,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
):
    return SingleEntityResponse(data=get_client(current_user, request=request))


# UPDATE SELF
@router.put('/cp/client/me/',
            response_model=SingleEntityResponse[ClientGet],
            name='Изменить данные клиента',
            description='Изменить данные текущего клиента',
            tags=['Админ панель / Клиент']
            )
def update_client_self(
        request: Request,
        new_data: ClientUpdateSelf,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):

    db_obj, code, index = crud_client.updating_client_self(
        db=session, current_user=current_user, obj_in=new_data)
    if code == -1:
        raise UnfoundEntity(
            message="Клиента с таким id не существует!",
            num=1,
            description="Клиента с таким id не существует!",
            path="$.body"
        )
    if code == -2:
        raise InaccessibleEntity(
            message="Вы не обладаете правами клиента",
            num=4,
            description="Вы не обладаете правами клиента!",
            path="$.body",
        )
    if code == -3:
        raise UnfoundEntity(
            message="Такого города не существует!",
            num=1,
            description="Нет выбранного вами города",
            path="$.body"
        )

    return SingleEntityResponse(data=get_client(db_obj, request=request))


# УЖЕ НЕ НАДО ТАК КАК Я СДЕЛАЛ УНИВЕРСАЛЬНУЮ ЗАГРУЗКУ ДЛЯ ВСЕХ ЮЗЕРОВ
# # UPDATE PHOTO BY TOKEN IN UNIVERSAL_USER
# @router.put("/cp/client/me/photo/",
#             response_model=SingleEntityResponse[ClientGet],
#             name='Изменить фотографию',
#             description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
#             tags=['Админ панель / Клиент'],
#             )
# def create_upload_file(
#         request: Request,
#         file: Optional[UploadFile] = File(None),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
#         ):
#     save_path = crud_universal_users.adding_photo(db=session, file=file, id_user=current_user.id)
#     if not save_path:
#         raise UnfoundEntity(
#             message="Не отправлен загружаемый файл",
#             num=2,
#             description="Попробуйте загрузить файл еще раз",
#             path="$.body",
#             )
#     return SingleEntityResponse(data=get_client(current_user, request=request))


if __name__ == "__main__":
    logging.info('Running...')


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNjY2MzUyOTE3LCJpYXQiOjE2NjU2NjE3MTcsIm5iZiI6MTY2NTY2MTcxNywianRpIjoiNWE3OWVhMTEtMTRmZS00OGFmLThkNGYtZDU2NDg0NGY3OTYzIn0.n0oyR1H6BNGO4iHySVhZSkeqQ9zQtQtRn2lUeWut7NY




