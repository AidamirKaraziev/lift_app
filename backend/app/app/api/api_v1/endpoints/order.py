import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
from fastapi.params import Path

from app.api import deps

from app.core.response import ListOfEntityResponse, SingleEntityResponse, Meta
from app.core.templates_raise import get_raise
from app.core.roles import ADMIN, FOREMAN, DISPATCHER, MECHANIC, ENGINEER

from app.crud.crud_universal_user import crud_universal_users
from app.crud.crud_order import crud_orders
from app.schemas.order import OrderGet, OrderCreate, OrderUpdate

from app.getters.order import getting_order

ROLES_ELIGIBLE = [ADMIN, FOREMAN, DISPATCHER]
ALL_EMPLOYER = [ADMIN, FOREMAN, MECHANIC, ENGINEER, DISPATCHER]

router = APIRouter()


# GET-MULTY
@router.get('/order/all',
            response_model=ListOfEntityResponse,
            name='get_orders',
            description='Получение списка всех задач',
            tags=['Админ панель / Задачи']
            )
def get_orders(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_orders.get_multi(db=session, page=None))

    data, paginator = crud_orders.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[getting_order(obj=datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET BY ID
@router.get('/order/{order_id}/',
            response_model=SingleEntityResponse[OrderGet],
            name='get_order_by_id',
            description='Получение данных задачи по id',
            tags=['Админ панель / Задачи']
            )
def get_order_by_id(
        request: Request,
        session=Depends(deps.get_db),
        order_id: int = Path(..., title='ID order'),
        # current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    obj, code, indexes = crud_orders.get_order_by_id(db=session, order_id=order_id)
    get_raise(code=code)
    return SingleEntityResponse(data=getting_order(obj, request))


# CREATE NEW OBJECT
@router.post('/order/',
             response_model=SingleEntityResponse,
             name='create_order',
             description='Создать задачу',
             tags=['Админ панель / Задачи']
             )
def create_order(
        request: Request,
        new_data: OrderCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    # сделать проверку на роль Администратора и Прораба
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, index = crud_orders.create_order(db=session, new_data=new_data, current_user=current_user)
    get_raise(code=code)
    return SingleEntityResponse(data=getting_order(obj, request))


# UPDATE
@router.put('/order/{order_id}/',
            response_model=SingleEntityResponse,
            name='update_order',
            description='Изменяет изменяет данные задачи',
            tags=['Админ панель / Задачи'])
def update_order(
        request: Request,
        new_data: OrderUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        order_id: int = Path(..., title='Id задачи'),
        session=Depends(deps.get_db)
):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ALL_EMPLOYER)
    get_raise(code=code)

    obj, code, indexes = crud_orders.update_order(db=session, new_data=new_data, order_id=order_id)
    get_raise(code=code)

    return SingleEntityResponse(data=getting_order(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
