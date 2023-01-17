import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from fastapi.params import Path

from app.schemas.token import TokenBase

from app.crud.crud_universal_user import crud_universal_users
from app.schemas.universal_user import UniversalUserEntrance, UniversalUserGet

from app.getters.universal_user import get_universal_user

from app.api import deps

from app.core.security import create_token_universal_user

from app.exceptions import UnfoundEntity, InaccessibleEntity, UnprocessableEntity
from app.schemas.universal_user import UniversalUserUpdate

from app.core.response import ListOfEntityResponse, SingleEntityResponse, Meta

from app.core.templates_raise import get_raise
from app.crud.crud_company import crud_company

from app.crud.crud_object import crud_objects
from app.getters.object import get_object

from app.schemas.object import ObjectGet
from app.core.roles import ADMIN, FOREMAN
from app.schemas.object import ObjectCreate

# PATH_MODEL = "universal_user"
# PATH_TYPE_PHOTO = "photo"
# PATH_TYPE_IDENTITY_CARD = "identity_card"
# PATH_TYPE_QUALIFICATION = "qualification_file"
from app.schemas.object import ObjectUpdate

ROLES_ELIGIBLE = [ADMIN, FOREMAN]

router = APIRouter()


# GET-MULTY
@router.get('/all-objects/',
            response_model=ListOfEntityResponse,
            name='Список объектов',
            description='Получение списка всех объектов',
            tags=['Админ панель / Объекты']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_objects.get_multi(db=session, page=None))

    data, paginator = crud_objects.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_object(datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET BY ID
@router.get('/object/{object_id}/',
            response_model=SingleEntityResponse[ObjectGet],
            name='Получить данные объекта по id ',
            description='Получение данных объекта по id',
            tags=['Админ панель / Объекты']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        object_id: int = Path(..., title='ID object'),
        # current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    obj, code, indexes = crud_objects.get_obj(db=session, id=object_id)
    get_raise(code=code)
    return SingleEntityResponse(data=get_object(obj, request))


# CREATE NEW OBJECT
@router.post('/object/',
             response_model=SingleEntityResponse,
             name='Добавить объект',
             description='Добавить один объект в базу данных ',
             tags=['Админ панель / Объекты']
             )
def create_object(
        request: Request,
        new_data: ObjectCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    # сделать проверку на роль Администратора и Прораба
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, index = crud_objects.create_object(db=session, new_data=new_data)
    get_raise(code=code)
    return SingleEntityResponse(data=get_object(obj, request))


# UPDATE
@router.put('/object/{object_id}/',
            response_model=SingleEntityResponse,
            name='Изменить данные объекта',
            description='Изменяет изменяет данные объекта',
            tags=['Админ панель / Объекты'])
def update_object(
        request: Request,
        new_data: ObjectUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        object_id: int = Path(..., title='Id объекта'),
        session=Depends(deps.get_db)
):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, indexes = crud_objects.update_object(db=session, new_data=new_data, object_id=object_id)
    get_raise(code=code)

    return SingleEntityResponse(data=get_object(obj, request=request))


#
# # GET-MULTY EMPLOYEE
# @router.get('/cp/all-employee/',
#             response_model=ListOfEntityResponse,
#             name='Список сотрудников',
#             description='Получение списка всех сотрудников',
#             tags=['Админ панель / Пользователь']
#             )
# def get_data(
#         request: Request,
#         session=Depends(deps.get_db),
#         page: int = Query(1, title="Номер страницы")
# ):
#     logging.info(crud_universal_users.get_multi_employee(db=session, page=None))
#
#     data, paginator = crud_universal_users.get_multi_employee(db=session, page=page)
#
#     return ListOfEntityResponse(data=[get_universal_user(datum, request=request) for datum in data],
#                                 meta=Meta(paginator=paginator))
#
#
# # GET CLIENT OF COMPANY
# @router.get('/cp/client/{company_id}/',
#             response_model=ListOfEntityResponse,
#             name='Список клиентов определенной компании',
#             description='Список клиентов определенной компании',
#             tags=['Админ панель / Пользователь']
#             )
# def get_data(
#         request: Request,
#         session=Depends(deps.get_db),
#         company_id: int = Path(..., title='ID user'),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         page: int = Query(1, title="Номер страницы")
# ):
#     # проверка компании
#     comp, code, indexes = crud_company.get_company(db=session, company_id=company_id)
#     get_raise(code=code)
#
#     logging.info(crud_universal_users.get_multi_client_by_company(db=session, company_id=company_id, page=None))
#
#     data, paginator = crud_universal_users.get_multi_client_by_company(db=session, page=page, company_id=company_id)
#
#     return ListOfEntityResponse(data=[get_universal_user(datum, request=request) for datum in data],
#                                 meta=Meta(paginator=paginator))
#
#
# # GET CLIENT
# @router.get('/cp/all-client/',
#             response_model=ListOfEntityResponse,
#             name='Список клиентов ',
#             description='Список клиентов',
#             tags=['Админ панель / Пользователь']
#             )
# def get_data(
#         request: Request,
#         session=Depends(deps.get_db),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         page: int = Query(1, title="Номер страницы")
# ):
#     # проверка компании
#
#     logging.info(crud_universal_users.get_multi_clients(db=session, page=None))
#
#     data, paginator = crud_universal_users.get_multi_clients(db=session, page=page)
#
#     return ListOfEntityResponse(data=[get_universal_user(datum, request=request) for datum in data],
#                                 meta=Meta(paginator=paginator))
#
#
# # GET
# @router.get('/cp/universal-user/me/',
#             response_model=SingleEntityResponse[UniversalUserGet],
#             name='Получить данные профиля ',
#             description='Получение всех  данных профиля, по токену',
#             tags=['Админ панель / Пользователь']
#             )
# def get_data(
#         request: Request,
#         current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
# ):
#     return SingleEntityResponse(data=get_universal_user(current_universal_user, request=request))
#
#
#
#
# # UPDATE SELF
# @router.put('/cp/universal-user/me/',
#             response_model=SingleEntityResponse[UniversalUserGet],
#             name='Изменить пользователя',
#             description='Изменить данные текущего пользователя',
#             tags=['Админ панель / Пользователь']
#             )
# def update_user(
#         request: Request,
#         new_data: UniversalUserUpdate,
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
# ):
#     role_list = [current_user.role_id]
#     changeable_list = role_list
#     obj, code, indexes = crud_universal_users.updating_user(db=session,
#                                                             current_user=current_user,
#                                                             user_id=current_user.id,
#                                                             new_data=new_data,
#                                                             role_list=role_list,
#                                                             changeable_list=changeable_list)
#
#     get_raise(code=code)
#     return SingleEntityResponse(data=get_universal_user(obj, request=request))
#
#
# # UPDATE photo
# @router.put("/cp/universal-user/me/photo/",
#             response_model=SingleEntityResponse,
#             name='Изменить фото',
#             description='Изменить фото для пользователя, если отправить пусто поле информация сбросится',
#             tags=['Админ панель / Пользователь'],
#             )
# def create_upload_file(
#         request: Request,
#         file: Optional[UploadFile] = File(None),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
#         ):
#     save_path = crud_universal_users.adding_file(
#         db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_PHOTO, db_obj=current_user)
#     if not save_path:
#         raise UnfoundEntity(message="Не отправлен загружаемый файл",
#                             num=2,
#                             description="Попробуйте загрузить файл еще раз",
#                             path="$.body",
#                             )
#     return SingleEntityResponse(data=get_universal_user(current_user, request=request))
#
#
# # UPDATE identity-card
# @router.put("/cp/universal-user/me/identity-card/",
#             response_model=SingleEntityResponse,
#             name='Изменить удостоверение',
#             description='Изменить удостоверение для пользователя, если отправить пусто поле информация сбросится',
#             tags=['Админ панель / Пользователь'],
#             )
# def create_upload_file(
#         request: Request,
#         file: Optional[UploadFile] = File(None),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
#         ):
#     save_path = crud_universal_users.adding_file(
#         db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_IDENTITY_CARD, db_obj=current_user)
#     if not save_path:
#         raise UnfoundEntity(message="Не отправлен загружаемый файл",
#                             num=2,
#                             description="Попробуйте загрузить файл еще раз",
#                             path="$.body",
#                             )
#     return SingleEntityResponse(data=get_universal_user(current_user, request=request))
#
#
# # UPDATE qualification_file
# @router.put("/cp/universal-user/me/qualification-file/",
#             response_model=SingleEntityResponse,
#             name='Изменить ЦОК',
#             description='Изменить ЦОК для пользователя, если отправить пусто поле информация сбросится',
#             tags=['Админ панель / Пользователь'],
#             )
# def create_upload_file(
#         request: Request,
#         file: Optional[UploadFile] = File(None),
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
#         ):
#     save_path = crud_universal_users.adding_file(
#         db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE_QUALIFICATION, db_obj=current_user)
#     if not save_path:
#         raise UnfoundEntity(message="Не отправлен загружаемый файл",
#                             num=2,
#                             description="Попробуйте загрузить файл еще раз",
#                             path="$.body",
#                             )
#     return SingleEntityResponse(data=get_universal_user(current_user, request=request))


if __name__ == "__main__":
    logging.info('Running...')

