import logging
from typing import Optional

from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path, Request

from app.api import deps

from app.core.response import ListOfEntityResponse, SingleEntityResponse
from app.core.response import Meta


from app.getters.company import get_company

from app.exceptions import UnprocessableEntity
from app.schemas.company import CompanyCreate

from app.exceptions import UnfoundEntity
from app.schemas.company import CompanyUpdate

from app.crud.crud_company import crud_company

from app.schemas.company import CompanyGet

from app.crud.crud_contact_person import crud_contact_person
from app.getters.contact_person import get_contact_person
from app.schemas.contact_person import ContactPersonCreate

from app.exceptions import InaccessibleEntity

from app.schemas.contact_person import ContactPersonUpdate

from app.crud.crud_universal_user import crud_universal_users

from app.core.templates_raise import get_raise

from app.core.roles import ADMIN, FOREMAN, CLIENT
from app.schemas.contact_person import ContactPersonGet

PATH_MODEL = "contact_person"
PATH_TYPE = "photo"

ADMIN_FOREMAN_ROLE = [ADMIN, FOREMAN]
ROLE_ADMIN_FOREMAN_CLIENT = [ADMIN, FOREMAN, CLIENT]

router = APIRouter()
# DELETE


# Вывод всех контактных лиц
# GET-MULTY
@router.get('/all-contact-person/',
            response_model=ListOfEntityResponse,
            name='Список контактных лиц',
            description='Получение списка всех контактных лиц',
            tags=['Админ панель / Контактное лицо']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_company.get_multi(db=session, page=None))

    data, paginator = crud_contact_person.get_multi(db=session, page=page)
    return ListOfEntityResponse(data=[get_contact_person(datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# CREATE NEW contact person
@router.post('/contact-person/',
             response_model=SingleEntityResponse,
             name='Добавить контактное лицо',
             description='Добавить контактное лицо в базу данных ',
             tags=['Админ панель / Контактное лицо']
             )
def create_contact_person(
        request: Request,
        new_data: ContactPersonCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    contact_person, code, index = crud_contact_person.create_contact_person(db=session, new_data=new_data, user=current_user)
    if code == -1:
        raise InaccessibleEntity(
            message="Вы не обладаете правами",
            num=1,
            description="Вы не обладаете правами администратора и прораба",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Такое контактное лицо уже создано",
            num=2,
            description="Такое контактное лицо уже создано",
            path="$.body"
        )
    if code == -3:
        raise UnfoundEntity(
            message="Выбранной вами компании не существует!",
            num=3,
            description="Выбранной вами компании не существует!",
            path="$.body"
        )
    get_raise(code=code)
    return SingleEntityResponse(data=get_contact_person(contact_person=contact_person, request=request))


# GET ID
@router.get('/contact-person/{contact_person_id}/',
            response_model=SingleEntityResponse,
            name='Контактное лицо',
            description='Получение данных контактного лица',
            tags=['Админ панель / Контактное лицо']
            )
def get_data(
        request: Request,
        contact_person_id: int = Path(..., title='ID контактного лица'),
        session=Depends(deps.get_db),
):
    return SingleEntityResponse(data=get_contact_person(crud_contact_person.get(
        db=session, id=contact_person_id), request=request))


# UPDATE
@router.put('/contact-person/{contact_person_id}/',
            response_model=SingleEntityResponse,
            name='Изменить контактное лицо',
            description='Изменяет данные контактного лица',
            tags=['Админ панель / Контактное лицо'])
def update_contact_person(
        request: Request,
        new_data: ContactPersonUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        contact_person_id: int = Path(..., title='Id'),
        session=Depends(deps.get_db)
):
    contact_person, code, indexes = crud_contact_person.update_contact_person(
        db=session, new_data=new_data, contact_person_id=contact_person_id, user=current_user)
    if code == -1:
        raise InaccessibleEntity(
            message="Вы не обладаете правами",
            num=1,
            description="Вы не обладаете правами администратора и прораба",
            path="$.body"
        )
    if code == -2:
        raise UnfoundEntity(
            message="Выбранного вами контактного лица не существует!",
            num=2,
            description="Выбранного вами контактного лица не существует!",
            path="$.body"
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Невозможно заменить номер телефона!",
            num=3,
            description="Контактное лицо с таким номером уже есть!",
            path="$.body"
        )
    if code == -4:
        raise UnfoundEntity(
            message="Выбранной вами компании не существует!",
            num=4,
            description="Выберите компанию, из существующих",
            path="$.body"
        )
    return SingleEntityResponse(data=get_contact_person(contact_person=contact_person, request=request))


# UPDATE PHOTO
@router.put("/contact-person/{contact_person_id}/photo/",
            response_model=SingleEntityResponse,
            name='Изменить фотографию',
            description='Изменить фотографию для контактного лица, если отправить пустой файл сбрасывает фото',
            tags=['Админ панель / Контактное лицо'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        contact_person_id: int = Path(..., title='Id проекта'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ADMIN_FOREMAN_ROLE)
    if code == -1023:
        raise InaccessibleEntity(
            message="Вы не обладаете правами!",
            num=2,
            description="Пользователь не обладает правами!",
            path="$.body"
        )
    obj = crud_contact_person.get(db=session, id=contact_person_id)

    save_path = crud_contact_person.adding_file(db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE,
                                                db_obj=obj)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_contact_person(crud_contact_person.get(db=session, id=contact_person_id),
                                                        request=request))


# UPDATE Photo
@router.put("/contact-person/{contact_person_id}/photo/",
            response_model=SingleEntityResponse[ContactPersonGet],
            name='Изменить фото',
            description='Изменить фото для контактного лица, если отправить пустой файл сбрасывает фото',
            tags=['Админ панель / Контактное лицо'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        contact_person_id: int = Path(..., title='Id Договора'),
        session=Depends(deps.get_db),
        ):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLE_ADMIN_FOREMAN_CLIENT)
    get_raise(code=code)

    obj, code, indexes = crud_contact_person.get(db=session, id=contact_person_id)
    get_raise(code=code)
    save_path = crud_contact_person.adding_file(db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE,
                                                db_obj=obj)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_contact_person(obj, request=request))


# АПИ ПО АРХИВАЦИИ ДОГОВОРА
@router.get('/contact-person/{contact_person_id}/archive/',
            response_model=SingleEntityResponse,
            name='Заморозить Контактное лицо',
            description='Архивация Контактное лицо',
            tags=['Админ панель / Контактное лицо'])
def archiving_contracts(
        request: Request,
        contact_person_id: int = Path(..., title='Id Контактное лицо'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_contact_person.archiving_contact_person(db=session,
                                                                      current_user=current_user,
                                                                      contact_person_id=contact_person_id,
                                                                      role_list=ADMIN_FOREMAN_ROLE)
    get_raise(code=code)

    return SingleEntityResponse(data=get_contact_person(obj, request=request))


# АПИ ПО РАЗАРХИВАЦИИ Договора
@router.get('/contact-person/{contact_person_id}/unzip/',
            response_model=SingleEntityResponse,
            name='Разморозка Контактное лицо',
            description='Разархивация Контактное лицо',
            tags=['Админ панель / Контактное лицо'])
def unzipping_contracts(
        request: Request,
        contact_person_id: int = Path(..., title='Id Контактное лицо'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_contact_person.unzipping_contact_person(db=session,
                                                                      current_user=current_user,
                                                                      contact_person_id=contact_person_id,
                                                                      role_list=ADMIN_FOREMAN_ROLE)
    get_raise(code=code)
    return SingleEntityResponse(data=get_contact_person(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
