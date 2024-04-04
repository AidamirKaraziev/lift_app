import logging
from fastapi import APIRouter, Depends, Query

from app.api import deps
from app.core.response import ListOfEntityResponse
from app.core.response import Meta

from app.crud.crud_status import crud_status
from app.getters.status import get_statuses


router = APIRouter()


# Вывод всех Должностей
@router.get('/statuses/',
            response_model=ListOfEntityResponse,
            name='Список статусов',
            description='Получение списка всех статусов',
            tags=['Админ панель / Статусы']
            )
def get_data(
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_status.get_multi(db=session, page=None))

    data, paginator = crud_status.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_statuses(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main__":
    logging.info('Running...')
