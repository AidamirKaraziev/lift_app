import logging
from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path

from app.api import deps

from app.core.response import ListOfEntityResponse
from app.core.response import Meta

from app.crud.crud_type_act import crud_type_acts
from app.getters.type_act import get_type_acts

router = APIRouter()


# Вывод всех типов АКТОВ
@router.get('/type-acts/',
            response_model=ListOfEntityResponse,
            name='Список типов актов',
            description='Получение списка всех типов актов',
            tags=['Админ панель / Типы Актов']
            )
def get_data(
        current_user=Depends(deps.get_current_universal_user_by_bearer),
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_type_acts.get_multi(db=session, page=None))

    data, paginator = crud_type_acts.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_type_acts(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main__":
    logging.info('Running...')
