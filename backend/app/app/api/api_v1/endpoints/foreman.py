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

from app.crud.crud_foreman import crud_foreman

from app.schemas.universal_user import UniversalUserDivision

from app.core.templates_raise import get_raise

from app.core.roles import MECHANIC, ENGINEER, DISPATCHER, FOREMAN

#
ROLES_ELIGIBLE = [FOREMAN]
EMPLOYEE_LIST = [MECHANIC, ENGINEER, DISPATCHER]
router = APIRouter()


# CREATE NEW EMPLOYEE
@router.post('/cp/foreman/create-employee/',
             response_model=SingleEntityResponse[UniversalUserGet],
             name='Создать сотрудника',
             description='Создать сотрудника',
             tags=['Админ панель / Прораб']
             )
def create_employee_person(
        request: Request,
        new_data: EmployeeCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj, code, index = crud_foreman.create_user_employee(db=session, current_user=current_user, new_data=new_data)
    get_raise(code=code)
    return SingleEntityResponse(data=get_universal_user(db_obj, request=request))


# UPDATE SELF
@router.put('/cp/foreman/me/division/',
            response_model=SingleEntityResponse[UniversalUserGet],
            name='Изменить участка',
            description='Изменить Участок текущего пользователя',
            tags=['Админ панель / Прораб']
            )
def update_user(
        request: Request,
        new_data: UniversalUserDivision,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    # проверка роли
    obj, code, indexes = crud_foreman.change_division_id(db=session, current_user=current_user, division=new_data,
                                                         role_list=ROLE_FOREMAN)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


#  АПИ ПО ИЗМЕНЕНИЮ УЧАСТКА ДЛЯ СОТРУДНИКА
@router.put('/cp/foreman/{employee_id}/division/',
            response_model=SingleEntityResponse,
            name='Изменить участок для пользователя',
            description='Изменить участок для пользователя',
            tags=['Админ панель / Прораб'])
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
                                                                 role_list=ROLE_FOREMAN,
                                                                 employee_list=EMPLOYEE_LIST)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


# АПИ ПО АРХИВАЦИИ ПОЛЬЗОВАТЕЛЕЙ
@router.get('/cp/foreman/{id_user}/archive/',
            response_model=SingleEntityResponse,
            name='Заморозить сотрудника',
            description='Архивация пользователя, доступ к приложению замораживается',
            tags=['Админ панель / Прораб'])
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
                                                   employee_list=EMPLOYEE_LIST)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


# АПИ ПО РАЗАРХИВАЦИИ ПОЛЬЗОВАТЕЛЕЙ
@router.get('/cp/foreman/{id_user}/unzip/',
            response_model=SingleEntityResponse,
            name='Разморозка сотрудника',
            description='Разархивация пользователя, доступ к приложению размораживается',
            tags=['Админ панель / Прораб'])
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
                                                   employee_list=EMPLOYEE_LIST)
    get_raise(code=code)

    return SingleEntityResponse(data=get_universal_user(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNjY4MTU5MTYyLCJpYXQiOjE2Njc0Njc5NjIsIm5iZiI6MTY2NzQ2Nzk2MiwianRpIjoiYWVjZThmM2UtNWY2Mi00YmIyLWJmODUtZDE3ZDY0Yzk0NzM2In0.LpFRCTtI7q2mtubooNjLRTymlQv2CjUxKe87cbhT7u4
