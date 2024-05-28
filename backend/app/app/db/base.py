# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.reason_fault import ReasonFault # noqa
from app.models.act_base import ActBase # noqa
from app.models.order import Order # noqa
from app.models.act_fact import ActFact # noqa
from app.models.status import Status # noqa
from app.models.area_of_responsibility import AreaOfResponsibility # noqa
from app.models.company import Company # noqa
from app.models.contact_person import ContactPerson # noqa
from app.models.contract import Contract # noqa
from app.models.cost_type import CostType # noqa
from app.models.division import Division # noqa
from app.models.factory_model import FactoryModel # noqa
from app.models.location import Location # noqa
from app.models.object import Object # noqa
from app.models.order_photo import OrderPhoto # noqa
from app.models.organization import Organization # noqa
from app.models.type_object import TypeObject # noqa
from app.models.fault_category import FaultCategory # noqa
from app.models.role import Role # noqa
from app.models.working_specialty import WorkingSpecialty # noqa
from app.models.universal_user import UniversalUser # noqa
from app.models.type_contract import TypeContract # noqa
from app.models.type_act import TypeAct # noqa
from app.models.sub_step import SubStep # noqa
from app.models.step import Step # noqa
