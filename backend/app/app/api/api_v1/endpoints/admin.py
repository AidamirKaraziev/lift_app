import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from fastapi.params import Path

# from app.api import deps
from app.core.response import SingleEntityResponse

from app.crud.crud_universal_user import crud_universal_users
from app.schemas.universal_user import UniversalUserEntrance, UniversalUserGet

from app.getters.universal_user import get_universal_user

from app.api import deps

# from app.schemas.admin import AdminGet

from app.crud.crud_admin import crud_admin
from app.exceptions import UnfoundEntity, InaccessibleEntity, UnprocessableEntity
from app.schemas.universal_user import UniversalUserRequest

from app.schemas.universal_user import UniversalUserUpdate

from fastapi import Response, Request
from mimetypes import guess_type

from os.path import isfile

from app.schemas.universal_user import EmployeeCreate
from app.schemas.admin import AdminCreate
from app.schemas.client import ClientCreate

from app.core.templates_raise import get_raise
from app.schemas.universal_user import UniversalUserDivision

from app.core.roles import FOREMAN, MECHANIC, ENGINEER, DISPATCHER, ADMIN

ROLES_ELIGIBLE = [ADMIN]
EMPLOYEE_LIST = [FOREMAN, MECHANIC, ENGINEER, DISPATCHER]
ALL_EMPLOYEE = [ADMIN, FOREMAN, MECHANIC, ENGINEER, DISPATCHER]


router = APIRouter()


@router.get("/static/{filename:path}", name='Получить статический файл', tags=['Инструменты'])
async def get_site(filename):
    filename = 'static/' + filename
    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, 'rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)

#
# # CREATE NEW UNIVERSAL_USER
# @router.post('/cp/admin/universal-user/',
#              response_model=SingleEntityResponse[UniversalUserGet],
#              name='Создать универсального пользователя',
#              description='Создать универсального пользователя',
#              tags=['Админ панель / Администратор']
#              )
# def create_universal_user(
#         request: Request,
#         new_data: UniversalUserRequest,
#         current_user=Depends(deps.get_current_universal_user_by_bearer),
#         session=Depends(deps.get_db),
# ):
#     db_obj, code, index = crud_admin.create_new_user(db=session, current_user=current_user, new_data=new_data)
#
#     if code == -1:
#         raise UnfoundEntity(
#             message="Токен не распознан!",
#             num=1,
#             description="Такого пользователя не существует!",
#             path="$.body"
#         )
#     if code == -2:
#         raise InaccessibleEntity(
#             message="Пользователь не обладает правами!",
#             num=2,
#             description="Пользователь не обладает правами, к созданию других пользователей!",
#             path="$.body"
#         )
#     if code == -9:
#         raise InaccessibleEntity(
#             message="Впишите email, это обязательно!",
#             num=2,
#             description="Укажите email, для регистрации",
#             path="$.body"
#         )
#     if code == -10:
#         raise InaccessibleEntity(
#             message="Пользователь с таким email уже есть!",
#             num=2,
#             description="Укажите другой email, для регистрации",
#             path="$.body"
#         )
#     if code == -3:
#         raise UnprocessableEntity(
#             message="Не указан пароль!",
#             num=3,
#             description="Необходимо указать пароль",
#             path="$.body"
#         )
#
#     # проверка локации и зоны ответственности
#     if code == -4:
#         raise UnfoundEntity(
#             message="Такого города нет!",
#             num=4,
#             description="Введен неправильный id города!",
#             path="$.body"
#         )
#
#     if code == -5:
#         raise UnprocessableEntity(
#             message="Выберите должность!",
#             num=5,
#             description="Необходимо выбрать должность!",
#             path="$.body"
#         )
#     if code == -6:
#         raise UnfoundEntity(
#             message="Такой Должности нет!",
#             num=6,
#             description="Выберете существующую должность!",
#             path="$.body"
#         )
#     if code == -7:
#         raise UnfoundEntity(
#             message="Такой Специальности нет!",
#             num=7,
#             description="Выберете существующую Специальность!",
#             path="$.body"
#         )
#     if code == -8:
#         raise UnfoundEntity(
#             message="Такой компании нет!",
#             num=8,
#             description="Выберете существующую Компанию или создайте новую!",
#             path="$.body"
#         )
#
#     return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


# CREATE NEW EMPLOYEE
@router.post('/cp/admin/create-employee/',
             response_model=SingleEntityResponse[UniversalUserGet],
             name='Создать сотрудника',
             description='Создать сотрудника',
             tags=['Админ панель / Администратор']
             )
def create_employee_person(
        request: Request,
        new_data: EmployeeCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj, code, index = crud_admin.create_user_employee(db=session, current_user=current_user, new_data=new_data)
    if code == -105:
        raise UnfoundEntity(
            message="Токен не распознан!",
            num=105,
            description="Такого пользователя не существует!",
            path="$.body"
        )
    if code == -1022:
        raise InaccessibleEntity(
            message="Вы не обладаете правами!",
            num=2,
            description="Пользователь не обладает правами, к созданию таких пользователей!",
            path="$.body"
        )
    if code == -1021:
        raise InaccessibleEntity(
            message="Неправильно выбрана должность!",
            num=2,
            description="Пользователь не обладает правами, к созданию таких пользователей!",
            path="$.body"
        )
    if code == -100:
        raise InaccessibleEntity(
            message="Пользователь с таким email уже есть!",
            num=2,
            description="Укажите другой email, для регистрации",
            path="$.body"
        )

    # проверка локации и зоны ответственности
    if code == -101:
        raise UnfoundEntity(
            message="Такого города нет!",
            num=4,
            description="Введен неправильный id города!",
            path="$.body"
        )

    if code == -102:
        raise UnfoundEntity(
            message="Такой Должности нет!",
            num=6,
            description="Выберете существующую должность!",
            path="$.body"
        )
    if code == -103:
        raise UnfoundEntity(
            message="Такой Специальности нет!",
            num=7,
            description="Выберете существующую Специальность!",
            path="$.body"
        )
    if code == -104:
        raise UnfoundEntity(
            message="Такого Участка нет!",
            num=8,
            description="Выберете существующую Участок или создайте новую!",
            path="$.body"
        )

    return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


# CREATE NEW Admin
@router.post('/cp/admin/create-admin/',
             response_model=SingleEntityResponse[UniversalUserGet],
             name='Создать Администратора',
             description='Создать Администратора',
             tags=['Админ панель / Администратор']
             )
def create_admin_person(
        request: Request,
        new_data: AdminCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj, code, index = crud_admin.create_user_admin(db=session, current_user=current_user, new_data=new_data)
    if code == -105:
        raise UnfoundEntity(
            message="Токен не распознан!",
            num=105,
            description="Такого пользователя не существует!",
            path="$.body"
        )
    if code == -1022:
        raise InaccessibleEntity(
            message="Вы не обладаете правами!",
            num=2,
            description="Пользователь не обладает правами, к созданию таких пользователей!",
            path="$.body"
        )

    if code == -100:
        raise InaccessibleEntity(
            message="Пользователь с таким email уже есть!",
            num=2,
            description="Укажите другой email, для регистрации",
            path="$.body"
        )

    # проверка локации и зоны ответственности
    if code == -101:
        raise UnfoundEntity(
            message="Такого города нет!",
            num=4,
            description="Введен неправильный id города!",
            path="$.body"
        )

    if code == -102:
        raise UnfoundEntity(
            message="Такой Должности нет!",
            num=6,
            description="Выберете существующую должность!",
            path="$.body"
        )
    if code == -1021:
        raise InaccessibleEntity(
            message="Неправильно выбрана должность!",
            num=2,
            description="Пользователь не обладает правами, к созданию таких пользователей!",
            path="$.body"
        )

    if code == -103:
        raise UnfoundEntity(
            message="Такой Специальности нет!",
            num=7,
            description="Выберете существующую Специальность!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


# CREATE NEW CLIENT
@router.post('/cp/admin/create-client/',
             response_model=SingleEntityResponse[UniversalUserGet],
             name='Создать клиента',
             description='Создать клиента',
             tags=['Админ панель / Администратор']
             )
def create_client_person(
        request: Request,
        new_data: ClientCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj, code, index = crud_admin.create_user_client(db=session, current_user=current_user, new_data=new_data)
    get_raise(code=code)

    # if code == -105:
    #     raise UnfoundEntity(
    #         message="Токен не распознан!",
    #         num=105,
    #         description="Такого пользователя не существует!",
    #         path="$.body"
    #     )
    # if code == -1022:
    #     raise InaccessibleEntity(
    #         message="Вы не обладаете правами!",
    #         num=1022,
    #         description="Пользователь не обладает правами, к созданию таких пользователей!",
    #         path="$.body"
    #     )
    #
    # if code == -100:
    #     raise InaccessibleEntity(
    #         message="Пользователь с таким email уже есть!",
    #         num=100,
    #         description="Укажите другой email, для регистрации",
    #         path="$.body"
    #     )
    #
    # # проверка локации и зоны ответственности
    # if code == -101:
    #     raise UnfoundEntity(
    #         message="Такого города нет!",
    #         num=101,
    #         description="Введен неправильный id города!",
    #         path="$.body"
    #     )
    #
    # if code == -102:
    #     raise UnfoundEntity(
    #         message="Такой Должности нет!",
    #         num=102,
    #         description="Выберете существующую должность!",
    #         path="$.body"
    #     )
    # if code == -1021:
    #     raise InaccessibleEntity(
    #         message="Неправильно выбрана должность!",
    #         num=1021,
    #         description="Пользователь не обладает правами, к созданию таких пользователей!",
    #         path="$.body"
    #     )
    # if code == -106:
    #     raise UnfoundEntity(
    #         message="Такой компании нет!",
    #         num=106,
    #         description="Выберете существующую Компанию или создайте новую!",
    #         path="$.body"
    #     )

    return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


#  АПИ ПО ИЗМЕНЕНИЮ УЧАСТКА ДЛЯ СОТРУДНИКА
@router.put('/cp/admin/{employee_id}/division/',
            response_model=SingleEntityResponse,
            name='Изменить участок для пользователя',
            description='Изменить участок для пользователя',
            tags=['Админ панель / Администратор'])
def update_dvision_for_employee(
        request: Request,
        new_data: UniversalUserDivision,
        employee_id: int = Path(..., title='Id пользователя'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_admin.change_division_for_employee(db=session,
                                                                 current_user=current_user,
                                                                 division=new_data,
                                                                 employee_id=employee_id,
                                                                 role_list=ROLES_ELIGIBLE,
                                                                 employee_list=EMPLOYEE_LIST)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


# АПИ ПО АРХИВАЦИИ ПОЛЬЗОВАТЕЛЕЙ
@router.get('/cp/admin/{id_user}/archive/',
            response_model=SingleEntityResponse,
            name='Заморозить сотрудника',
            description='Архивация пользователя, доступ к приложению замораживается',
            tags=['Админ панель / Администратор'])
def archiving_users(
        request: Request,
        id_user: int = Path(..., title='Id пользователя'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_admin.archiving_user(db=session,
                                                   current_user=current_user,
                                                   id_user=id_user,
                                                   role_list=ROLES_ELIGIBLE,
                                                   employee_list=ALL_EMPLOYEE)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


# АПИ ПО РАЗАРХИВАЦИИ ПОЛЬЗОВАТЕЛЕЙ
@router.get('/cp/admin/{id_user}/unzip/',
            response_model=SingleEntityResponse,
            name='Разморозка сотрудника',
            description='Разархивация пользователя, доступ к приложению размораживается',
            tags=['Админ панель / Администратор'])
def unzipping_users(
        request: Request,
        id_user: int = Path(..., title='Id пользователя'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_admin.unzipping_user(db=session,
                                                   current_user=current_user,
                                                   id_user=id_user,
                                                   role_list=ROLES_ELIGIBLE,
                                                   employee_list=ALL_EMPLOYEE)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
