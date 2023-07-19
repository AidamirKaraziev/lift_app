import logging
from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta

from app.crud.crud_execution_status import crud_status
from app.getters.execution_status import get_status

router = APIRouter()


@router.get('/statuses/',
            response_model=ListOfEntityResponse,
            name='Список статусов',
            description='Получение списка всех статусов',
            tags=['Админ панель / Статусы']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_status.get_multi(db=session, page=None))

    data, paginator = crud_status.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_status(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main__":
    logging.info('Running...')