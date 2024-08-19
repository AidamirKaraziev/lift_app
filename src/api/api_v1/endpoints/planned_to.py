import logging
from fastapi import APIRouter, Depends, Request, Query
from fastapi.params import Path
from src.api import deps
from src.crud.users.crud_universal_user import crud_universal_users
from src.core.response import ListOfEntityResponse, SingleEntityResponse, Meta

from src.core.templates_raise import get_raise
from src.core.roles import ADMIN, FOREMAN
from src.crud.crud_planned_to import crud_planned_to
from src.getters.planned_to import get_planned_to
from src.schemas.planned_to import PlannedTOGet, PlannedTOCreate, PlannedTOUpdate

ROLES_ELIGIBLE = [ADMIN, FOREMAN]
router = APIRouter()


# GET-MULTY
@router.get('/all-planned-to/',
            response_model=ListOfEntityResponse,
            name='get_all_planned_to',
            description='Получение списка всех Плановых ТО',
            tags=['Админ панель / Плановые ТО']
            )
def get_all_planned_to(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_planned_to.get_multi(db=session, page=None))

    data, paginator = crud_planned_to.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_planned_to(obj=datum, request=request) for datum in data],
                                meta=Meta(paginator=paginator))


# GET BY ID
@router.get('/planned-to/{planned_to_id}/',
            response_model=SingleEntityResponse[PlannedTOGet],
            name='get_planned_to_by_id',
            description='Получение данных планового ТО по id',
            tags=['Админ панель / Плановые ТО']
            )
def get_planned_to_by_id(
        request: Request,
        session=Depends(deps.get_db),
        planned_to_id: int = Path(..., title='ID planned TO'),
        # current_universal_user=Depends(deps.get_current_universal_user_by_bearer),
):
    obj, code, indexes = crud_planned_to.getting_planned_to(db=session, planned_to_id=planned_to_id)
    get_raise(code=code)
    return SingleEntityResponse(data=get_planned_to(obj, request))


# CREATE NEW ACT FACT
@router.post('/planned-to/',
             response_model=SingleEntityResponse,
             name='create_planned_to',
             description='Добавить плановое ТО в базу данных',
             tags=['Админ панель / Плановые ТО']
             )
def create_planned_to(
        request: Request,
        new_data: PlannedTOCreate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
):
    # сделать проверку на роль Администратора и Прораба
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, index = crud_planned_to.create_planned_to(db=session, new_data=new_data)
    get_raise(code=code)
    return SingleEntityResponse(data=get_planned_to(obj, request))


# UPDATE
@router.put('/planned-to/{planned_to_id}/',
            response_model=SingleEntityResponse,
            name='update_planned_to',
            description='Изменяет плановое ТО',
            tags=['Админ панель / Плановые ТО'])
def update_planned_to(
        request: Request,
        new_data: PlannedTOUpdate,
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        planned_to_id: int = Path(..., title='Id планового ТО'),
        session=Depends(deps.get_db)
):
    # проверка на роли
    code = crud_universal_users.check_role_list(current_user=current_user, role_list=ROLES_ELIGIBLE)
    get_raise(code=code)

    obj, code, indexes = crud_planned_to.update_planned_to(db=session, new_data=new_data, planned_to_id=planned_to_id)
    get_raise(code=code)

    return SingleEntityResponse(data=get_planned_to(obj, request=request))


if __name__ == "__main__":
    logging.info('Running...')
