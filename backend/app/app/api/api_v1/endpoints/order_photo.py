import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
from fastapi.params import Path

from app.api import deps

from app.core.response import ListOfEntityResponse, SingleEntityResponse, Meta
from app.core.templates_raise import get_raise
from app.core.roles import ADMIN, FOREMAN, DISPATCHER, MECHANIC, ENGINEER

from app.crud.crud_order_photo import crud_order_photo
from app.getters.order_photo import getting_order_photo

from app.schemas.order_photo import OrderPhotoGet

ROLES_ELIGIBLE = [ADMIN, FOREMAN, DISPATCHER]
ALL_EMPLOYER = [ADMIN, FOREMAN, MECHANIC, ENGINEER, DISPATCHER]
PATH_MODEL = "order_photo"
PATH_TYPE = "photo"
router = APIRouter()


# GET-MULTY
@router.get('/order-photo/all',
            response_model=ListOfEntityResponse,
            name='get_order_photo',
            description='Получение списка всех фотографий',
            tags=['Админ панель / Фотографии Задачи']
            )
def get_order_photo(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_order_photo.get_multi(db=session, page=None))

    data, paginator = crud_order_photo.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[getting_order_photo(obj=datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET ORDERS BY ORDER_ID
@router.get('/order-photo/{order_id}',
            response_model=ListOfEntityResponse,
            name='get_photo_by_order_id',
            description='Получение списка всех фотографий по номеру задачи',
            tags=['Админ панель / Фотографии Задачи']
            )
def get_photo_by_order_id(
        request: Request,
        session=Depends(deps.get_db),
        order_id: int = Path(..., title='Id задачи'),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_order_photo.get_photo_by_order_id(db=session, order_id=order_id))

    data, code, indexes = crud_order_photo.get_photo_by_order_id(db=session, order_id=order_id)
    get_raise(code=code)
    return ListOfEntityResponse(data=[getting_order_photo(obj=datum, request=request) for datum in data])


# GET BY ID
@router.get('/order-photo/{order_photo_id}/',
            response_model=SingleEntityResponse[OrderPhotoGet],
            name='get_order_photo_by_id',
            description='Получить фотографию по id',
            tags=['Админ панель / Фотографии Задачи']
            )
def get_order_photo_by_id(
        request: Request,
        session=Depends(deps.get_db),
        order_photo_id: int = Path(..., title='ID order_photo'),
        # current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    obj, code, indexes = crud_order_photo.get_photo_by_id(db=session, order_photo_id=order_photo_id)
    get_raise(code=code)

    return SingleEntityResponse(data=getting_order_photo(obj, request))


@router.post("/order-photo/{order_id}/",
             response_model=SingleEntityResponse,
             name='add_photo',
             description='Добавить фотографию к задаче',
             tags=['Админ панель / Фотографии Задачи'],
             )
def add_photo(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        order_id: int = Path(..., title='Id задачи'),
        session=Depends(deps.get_db),
        ):
    obj, code, indexes = crud_order_photo.check_executor(db=session, order_id=order_id, executor_id=current_user.id)
    get_raise(code=code)

    obj, code, indexes = crud_order_photo.add_photo(db=session, file=file, path_model=PATH_MODEL, path_type=PATH_TYPE,
                                                    order_id=order_id)
    get_raise(code=code)

    data, code, indexes = crud_order_photo.get_photo_by_order_id(db=session, order_id=order_id)
    get_raise(code=code)
    return ListOfEntityResponse(data=[getting_order_photo(obj=datum, request=request) for datum in data])


if __name__ == "__main__":
    logging.info('Running...')
