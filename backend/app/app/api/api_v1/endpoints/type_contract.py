import logging
from fastapi import APIRouter, Depends, Query

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta

from app.crud.crud_type_contract import crud_type_contract
from app.getters.type_contract import get_type_contracts


router = APIRouter()


# Вывод всех типов Договора
@router.get('/contracts/',
            response_model=ListOfEntityResponse,
            name='Список типов договора',
            description='Получение списка всех типов договора',
            tags=['Админ панель / Типы Договора']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_type_contract.get_multi(db=session, page=None))

    data, paginator = crud_type_contract.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_type_contracts(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main__":
    logging.info('Running...')
