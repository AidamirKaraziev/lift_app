from fastapi import Request
from typing import Optional

from app.core.config import Settings, settings

from app.getters.factory_model import get_factory_model
from app.getters.type_act import get_type_acts
from app.models.act_base import ActBase
from app.schemas.act_base import ActBaseGet


def get_acts_bases(db_obj: ActBase, request: Optional[Request],
                   config: Settings = settings) -> Optional[ActBaseGet]:
    return ActBaseGet(
        id=db_obj.id,
        factory_model_id=get_factory_model(db_obj.factory_model) if db_obj.factory_model is not None else None,
        type_act_id=get_type_acts(db_obj.type_act) if db_obj.type_act is not None else None,
        step_list=db_obj.step_list
    )
