import logging
from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path

from app.api import deps

from app.core.response import ListOfEntityResponse
from app.core.response import Meta

from app.crud.crud_step import crud_step
from app.getters.step import get_step

router = APIRouter()


# Вывод всех Step
@router.get('/steps/',
            response_model=ListOfEntityResponse,
            name='Список шагов',
            description='Получение списка всех названий шагов',
            tags=['Админ панель / Название Шагов']
            )
def get_data(
        # current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_step.get_multi(db=session, page=None))

    data, paginator = crud_step.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_step(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main__":
    logging.info('Running...')
