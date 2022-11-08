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


PATH_MODEL = "universal_user"
PATH_TYPE_PHOTO = "photo"
PATH_TYPE_IDENTITY_CARD = "identity_card"
PATH_TYPE_QUALIFICATION = "qualification_file"

router = APIRouter()


# SIGN-IN
# Вход по почте и паролю
@router.post('/cp/sign-in/', response_model=SingleEntityResponse[TokenBase],
             name='Войти в админ панель',
             description='Войти в админ панель',
             tags=['Вход / Админ панель'])
def entrance(
    universal_user: UniversalUserEntrance,
    session=Depends(deps.get_db),
):
    db_obj = crud_universal_users.get_universal_user(session, universal_user=universal_user)
    token = create_token_universal_user(subject=db_obj.id)
    return SingleEntityResponse(data=TokenBase(token=token))


# GET-MULTY
@router.get('/all-users/',
            response_model=ListOfEntityResponse,
            name='Список пользователей',
            description='Получение списка всех пользователей',
            tags=['Админ панель / Пользователь']
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


# GET-MULTY EMPLOYEE
@router.get('/all-employee/',
            response_model=ListOfEntityResponse,
            name='Список сотрудников',
            description='Получение списка всех сотрудников',
            tags=['Админ панель / Пользователь']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_universal_users.get_multi_employee(db=session, page=None))

    data, paginator = crud_universal_users.get_multi_employee(db=session, page=page)

    return ListOfEntityResponse(data=[get_universal_user(datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET
@router.get('/cp/universal-user/me/',
            response_model=SingleEntityResponse[UniversalUserGet],
            name='Получить данные профиля ',
            description='Получение всех  данных профиля, по токену',
            tags=['Админ панель / Пользователь']
            )
def get_data(
        request: Request,
        current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    return SingleEntityResponse(data=get_universal_user(current_universal_user, request=request))


# GET BY ID
@router.get('/cp/universal-user/{user_id}/',
            response_model=SingleEntityResponse[UniversalUserGet],
            name='Получить данные профиля по id ',
            description='Получение данных профиля по id',
            tags=['Админ панель / Пользователь']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        user_id: int = Path(..., title='ID user'),
        current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    user = crud_universal_users.get(db=session, id=user_id)
    if user is None:
        raise UnfoundEntity(
            message="Нет такого пользователя!",
            num=105,
            description="Нет пользователя с таким id!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_universal_user(user, request=request))


# UPDATE SELF
@router.put('/cp/universal-user/me/',
            response_model=SingleEntityResponse[UniversalUserGet],
            name='Изменить пользователя',
            description='Изменить данные текущего пользователя',
            tags=['Админ панель / Пользователь']
            )
def update_user(
        request: Request,
        new_data: UniversalUserUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):

    db_obj, code, index = crud_universal_users.update_user_self(
        db=session, current_user=current_user, new_data=new_data)
    if code == -105:
        raise UnfoundEntity(
            message="Нет такого пользователя!",
            num=105,
            description="Нет пользователя с таким id!",
            path="$.body"
        )
    if code == -107:
        raise UnprocessableEntity(
            message="Пользователь не актуален!",
            num=2,
            description="Статус пользователя не актуален, возможно его удалили!",
            path="$.body"
        )
    if code == -101:
        raise UnfoundEntity(
            message="Такого города не существует!",
            num=101,
            description="Выберете существующий город!",
            path="$.body"
        )

    return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


# UPDATE photo
@router.put("/cp/universal_user/me/photo/",
            response_model=SingleEntityResponse,
            name='Изменить фото',
            description='Изменить фото для пользователя, если отправить пусто поле информация сбросится',
            tags=['Админ панель / Пользователь'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    save_path = crud_universal_users.adding_file(
        db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_PHOTO, db_obj=current_user)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_universal_user(current_user, request=request))


# UPDATE identity-card
@router.put("/cp/universal_user/me/identity-card/",
            response_model=SingleEntityResponse,
            name='Изменить удостоверение',
            description='Изменить удостоверение для пользователя, если отправить пусто поле информация сбросится',
            tags=['Админ панель / Пользователь'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    save_path = crud_universal_users.adding_file(
        db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_IDENTITY_CARD, db_obj=current_user)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_universal_user(current_user, request=request))


# UPDATE qualification_file
@router.put("/cp/universal_user/me/qualification-file /",
            response_model=SingleEntityResponse,
            name='Изменить ЦОК',
            description='Изменить ЦОК для пользователя, если отправить пусто поле информация сбросится',
            tags=['Админ панель / Пользователь'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    save_path = crud_universal_users.adding_file(
        db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_QUALIFICATION, db_obj=current_user)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_universal_user(current_user, request=request))


if __name__ == "__main__":
    logging.info('Running...')
