import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from fastapi.params import Path
from app.api import deps

from app.crud.crud_universal_user import crud_universal_users
from app.core.response import ListOfEntityResponse, SingleEntityResponse, Meta


from app.core.templates_raise import get_raise


from app.crud.crud_object import crud_objects
from app.getters.object import get_object
from app.schemas.object import ObjectCreate, ObjectUpdate, ObjectGet

from app.core.roles import ADMIN, FOREMAN

from app.exceptions import UnfoundEntity

PATH_MODEL = "objects"
PATH_TYPE_LETTER_OF_APPOINTMENT = "letter_of_appointment"
PATH_TYPE_ACCEPTANCE_CERTIFICATE = "acceptance_certificate"
PATH_TYPE_ACT_PTO = "act_pto"

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

    return ListOfEntityResponse(data=[get_object(obj=datum, request=request) for datum in data],
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
    obj, code, indexes = crud_objects.getting_object(db=session, object_id=object_id)
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


# UPDATE letter_of_appointment
@router.put("/object/{object_id}/letter_of_appointment/",
            response_model=SingleEntityResponse[ObjectGet],
            name='Изменить Письмо о назначение',
            description='Изменить Письмо о назначение для объектов, если отправить пустой файл - сбрасывает',
            tags=['Админ панель / Объекты'],
            )
def create_letter_of_appointment_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        object_id: int = Path(..., title='Id объекта'),
        session=Depends(deps.get_db),
        ):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, indexes = crud_objects.getting_object(db=session, object_id=object_id)
    get_raise(code=code)

    crud_objects.adding_file(db=session, file=file, path_model=PATH_MODEL,
                             path_type=PATH_TYPE_LETTER_OF_APPOINTMENT, db_obj=obj)
    return SingleEntityResponse(data=get_object(crud_objects.get(db=session, id=object_id), request=request))


# UPDATE acceptance_certificate
@router.put("/object/{object_id}/acceptance_certificate/",
            response_model=SingleEntityResponse[ObjectGet],
            name='Изменить Акт приемки',
            description='Изменить Акт приемки для объектов, если отправить пустой файл - сбрасывает',
            tags=['Админ панель / Объекты'],
            )
def create_acceptance_certificate_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        object_id: int = Path(..., title='Id объекта'),
        session=Depends(deps.get_db),
        ):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, indexes = crud_objects.getting_object(db=session, object_id=object_id)
    get_raise(code=code)

    crud_objects.adding_file(db=session, file=file, path_model=PATH_MODEL,
                             path_type=PATH_TYPE_ACCEPTANCE_CERTIFICATE, db_obj=obj)
    return SingleEntityResponse(data=get_object(crud_objects.get(db=session, id=object_id), request=request))


# UPDATE act_pto
@router.put("/object/{object_id}/act_pto/",
            response_model=SingleEntityResponse[ObjectGet],
            name='Изменить Акт ПТО',
            description='Изменить Акт ПТО для объектов, если отправить пустой файл - сбрасывает',
            tags=['Админ панель / Объекты'],
            )
def create_act_pto_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        object_id: int = Path(..., title='Id объекта'),
        session=Depends(deps.get_db),
        ):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, indexes = crud_objects.getting_object(db=session, object_id=object_id)
    get_raise(code=code)

    crud_objects.adding_file(db=session, file=file, path_model=PATH_MODEL,
                             path_type=PATH_TYPE_ACT_PTO, db_obj=obj)
    return SingleEntityResponse(data=get_object(crud_objects.get(db=session, id=object_id), request=request))


# АПИ ПО АРХИВАЦИИ объекта
@router.get('/object/{object_id}/archive/',
            response_model=SingleEntityResponse,
            name='Заморозить объекта',
            description='Архивация объекта',
            tags=['Админ панель / Объекты'])
def archiving_objects(
        request: Request,
        object_id: int = Path(..., title='Id объекта'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_objects.archiving_object(db=session,
                                                       current_user=current_user,
                                                       object_id=object_id,
                                                       role_list=ROLES_ELIGIBLE)
    get_raise(code=code)
    return SingleEntityResponse(data=get_object(obj, request=request))


# АПИ ПО РАЗАРХИВАЦИИ объекта
@router.get('/object/{object_id}/unzip/',
            response_model=SingleEntityResponse,
            name='Разморозка объекта',
            description='Разархивация объекта, доступ к приложению размораживается',
            tags=['Админ панель / Объекты'])
def unzipping_objects(
        request: Request,
        object_id: int = Path(..., title='Id объекта'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_objects.unzipping_object(db=session,
                                                       current_user=current_user,
                                                       object_id=object_id,
                                                       role_list=ROLES_ELIGIBLE)
    get_raise(code=code)
    return SingleEntityResponse(data=get_object(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
