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
PATH_MODEL = "company"
PATH_TYPE = "photo"
router = APIRouter()
# DELETE


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
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    company, code, index = crud_company.create_company(db=session, new_data=new_data)
    if code == -1:
        raise UnprocessableEntity(
            message="Такая компания уже есть в базе данных",
            num=1,
            description="Компания с таким названием уже есть в базе данных!",
            path="$.body"
        )
    if code == -2:
        raise UnfoundEntity(
            message="Выбранного вами города не существует!",
            num=1,
            description="Выберете город из представленных!",
            path="$.body"
        )
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
        company_id: int = Path(..., title='Id проекта'),
        session=Depends(deps.get_db)
):
    company, code, indexes = crud_company.update_company(db=session, company=new_data, company_id=company_id)
    if code == -1:
        raise UnfoundEntity(
            message="Компании с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Компания с таким названием уже есть!",
            num=2,
            description="Выберите другое название компании!",
            path="$.body"
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Такого города нет!",
            num=2,
            description="Выберите другой город!",
            path="$.body"
        )
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
        company_id: int = Path(..., title='Id компании'),
        # current_super_user=Depends(deps.get_current_super_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    obj = crud_company.get(db=session, id=company_id)

    save_path = crud_company.adding_file(db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE,
                                         db_obj=obj)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_company(crud_company.get(db=session, id=company_id), request=request))


if __name__ == "__main__":
    logging.info('Running...')
