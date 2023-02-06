from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings


from app.getters.universal_user import get_universal_user
from app.models import Object
from app.schemas.object import ObjectGet

from app.utils.time_stamp import to_timestamp

from app.getters.act_base import get_acts_bases
from app.getters.object import get_object
from app.models import ActFact
from app.getters.status import get_statuses
from app.schemas.act_fact import ActFactGet


def get_acts_facts(obj: ActFact, request: Optional[Request],
                   config: Settings = settings) -> Optional[ObjectGet]:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if obj.file is not None:
            obj.file = url + str(obj.file)
        else:
            obj.file = None

    return ActFactGet(
        id=obj.id,
        object_id=get_object(obj.object, request=request) if obj.object is not None else None,
        act_base_id=get_acts_bases(obj.act_base, request=request) if obj.act_base is not None else None,
        step_list_fact=obj.step_list_fact,

        date_create=obj.date_create,
        date_start=obj.date_start,
        date_finish=obj.date_finish,

        foreman_id=get_universal_user(obj.foreman, request=request) if obj.foreman is not None else None,
        main_mechanic_id=get_universal_user(obj.main_mechanic, request=request) if obj.main_mechanic is not None else None,

        file=obj.file,
        status_id=get_statuses(obj.status) if obj.status is not None else None
    )
