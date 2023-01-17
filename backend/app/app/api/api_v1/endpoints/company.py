import logging
from typing import Optional

from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path, Request

from app.api import deps

from app.core.response import ListOfEntityResponse, SingleEntityResponse, Meta

from app.getters.company import get_company

from app.exceptions import UnfoundEntity, UnprocessableEntity
from app.schemas.company import CompanyUpdate, CompanyGet, CompanyCreate
from app.crud.crud_company import crud_company

from app.crud.crud_universal_user import crud_universal_users

from app.core.roles import ADMIN, CLIENT
from app.core.templates_raise import get_raise

# from backend.app.app.getters.universal_user import get_universal_user

ROLES_ELIGIBLE = [ADMIN]
ROLES_ELIGIBLE_ADMIN_CLIENT = [ADMIN, CLIENT]

PATH_MODEL = "company"
PATH_TYPE = "photo"
router = APIRouter()


# Вывод всех Компаний
# GET-MULTY
@router.get('/all-company/',
            response_model=ListOfEntityResponse,
            name='Список Компаний',
            description='Получение списка всех компаний',
            tags=['Админ панель / Компании']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_company.get_multi(db=session, page=None))

    data, paginator = crud_company.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_company(datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# CREATE NEW COMPANY
@router.post('/company/',
             response_model=SingleEntityResponse,
             name='Добавить Компанию',
             description='Добавить одну компанию в базу данных ',
             tags=['Админ панель / Компании']
             )
def create_company(
        request: Request,
        new_data: CompanyCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    # сделать проверку на роль Администратора
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    company, code, index = crud_company.create_company(db=session, new_data=new_data)
    get_raise(code=code)
    return SingleEntityResponse(data=get_company(company=company, request=request))


# GET ID
@router.get('/company/{company_id}/',
            response_model=SingleEntityResponse,
            name='Компания',
            description='Получение данных компании',
            tags=['Админ панель / Компании']
            )
def get_data(
        request: Request,
        company_id: int = Path(..., title='ID компании'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    return SingleEntityResponse(data=get_company(crud_company.get(db=session, id=company_id), request=request))


# UPDATE
@router.put('/company/{company_id}/',
            response_model=SingleEntityResponse,
            name='Изменить данные компании',
            description='Изменяет изменяет данные компании',
            tags=['Админ панель / Компании'])
def update_company(
        request: Request,
        new_data: CompanyUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        company_id: int = Path(..., title='Id проекта'),
        session=Depends(deps.get_db)
):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE_ADMIN_CLIENT)
    get_raise(code=code)

    company, code, indexes = crud_company.update_company(db=session, company=new_data, company_id=company_id)
    get_raise(code=code)

    return SingleEntityResponse(data=get_company(company=company, request=request))


# UPDATE PHOTO
@router.put("/company/{company_id}/photo/",
            response_model=SingleEntityResponse[CompanyGet],
            name='Изменить фотографию',
            description='Изменить фотографию для компаний, если отправить пустой файл сбрасывает фото',
            tags=['Админ панель / Компании'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        company_id: int = Path(..., title='Id компании'),
        session=Depends(deps.get_db),
        ):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE_ADMIN_CLIENT)
    get_raise(code=code)

    obj, code, indexes = crud_company.get_company(db=session, company_id=company_id)
    get_raise(code=code)
    crud_company.adding_file(db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE, db_obj=obj)

    return SingleEntityResponse(data=get_company(crud_company.get(db=session, id=company_id), request=request))


# АПИ ПО АРХИВАЦИИ КОМПАНИИ
@router.get('/company/{company_id}/archive/',
            response_model=SingleEntityResponse,
            name='Заморозить компании',
            description='Архивация компании',
            tags=['Админ панель / Компании'])
def archiving_companies(
        request: Request,
        company_id: int = Path(..., title='Id КОМПАНИИ'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_company.archiving_company(db=session,
                                                        current_user=current_user,
                                                        company_id=company_id,
                                                        role_list=ROLES_ELIGIBLE)
    get_raise(code=code)
    # получение списка клиентов этой компании
    # users = crud_universal_users.get_clients_list(db=session, company_id=company_id)
    # print("@"*100)
    # print(users)

    return SingleEntityResponse(data=get_company(obj, request=request))


# АПИ ПО РАЗАРХИВАЦИИ КОМПАНИИ
@router.get('/company/{company_id}/unzip/',
            response_model=SingleEntityResponse,
            name='Разморозка компании',
            description='Разархивация Компании, доступ к приложению размораживается',
            tags=['Админ панель / Компании'])
def unzipping_companies(
        request: Request,
        company_id: int = Path(..., title='Id КОМПАНИИ'),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db)
):
    obj, code, indexes = crud_company.unzipping_company(db=session,
                                                        current_user=current_user,
                                                        company_id=company_id,
                                                        role_list=ROLES_ELIGIBLE)
    get_raise(code=code)
    return SingleEntityResponse(data=get_company(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
