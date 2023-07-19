from sqlalchemy.orm import Session

from app import crud, schemas
# from app.core.config import
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.core.config import settings


# Я не знаю что делает эта часть кода, но вот так проект запускается
from app.db import session
from app.db.session import get_session
from app.models import Role, Status, TypeObject, TypeContract, Location, FaultCategory


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_tel(db, tel=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            tel=settings.FIRST_SUPERUSER
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841


def check_roles(db: Session):
    admin = db.query(Role).filter(Role.name == 'admin', Role.id == 1).first()
    foreman = db.query(Role).filter(Role.name == 'foreman', Role.id == 2).first()
    mechanic = db.query(Role).filter(Role.name == 'mechanic', Role.id == 3).first()
    engineer = db.query(Role).filter(Role.name == 'engineer', Role.id == 4).first()
    dispatcher = db.query(Role).filter(Role.name == 'dispatcher', Role.id == 5).first()
    client = db.query(Role).filter(Role.name == 'client', Role.id == 6).first()
    if admin is not None:
        admin_role_is_exist = True
    else:
        admin_role_is_exist = False

    if foreman is not None:
        foreman_role_is_exist = True
    else:
        foreman_role_is_exist = False

    if mechanic is not None:
        mechanic_role_is_exist = True
    else:
        mechanic_role_is_exist = False

    if engineer is not None:
        engineer_role_is_exist = True
    else:
        engineer_role_is_exist = False

    if dispatcher is not None:
        dispatcher_role_is_exist = True
    else:
        dispatcher_role_is_exist = False

    if client is not None:
        client_role_is_exist = True
    else:
        client_role_is_exist = False

    return admin_role_is_exist, foreman_role_is_exist, mechanic_role_is_exist, engineer_role_is_exist, \
           dispatcher_role_is_exist, client_role_is_exist


def create_roles():

    for db in get_session():
        roles = []

    admin_role_is_exist, foreman_role_is_exist, mechanic_role_is_exist, engineer_role_is_exist, \
           dispatcher_role_is_exist, client_role_is_exist = check_roles(db=db)
    if not admin_role_is_exist:
        roles.append(Role(id=1, name="admin"))

    if not foreman_role_is_exist:
        roles.append(Role(id=2, name="foreman"))

    if not mechanic_role_is_exist:
        roles.append(Role(id=3, name="mechanic"))

    if not engineer_role_is_exist:
        roles.append(Role(id=4, name="engineer"))

    if not dispatcher_role_is_exist:
        roles.append(Role(id=5, name="dispatcher"))

    if not client_role_is_exist:
        roles.append(Role(id=6, name="client"))

    [db.add(role) for role in roles]
    db.commit()
    db.close()


def check_statuses(db: Session):
    status_1 = db.query(Status).filter(Status.name == 'Создано', Status.id == 1).first()
    status_2 = db.query(Status).filter(Status.name == 'Принято', Status.id == 2).first()
    status_3 = db.query(Status).filter(Status.name == 'В процессе', Status.id == 3).first()
    status_4 = db.query(Status).filter(Status.name == 'Выполнено', Status.id == 4).first()
    status_5 = db.query(Status).filter(Status.name == 'Проблема', Status.id == 5).first()

    if status_1 is not None:
        status_1_is_exist = True
    else:
        status_1_is_exist = False

    if status_2 is not None:
        status_2_is_exist = True
    else:
        status_2_is_exist = False

    if status_3 is not None:
        status_3_is_exist = True
    else:
        status_3_is_exist = False

    if status_4 is not None:
        status_4_is_exist = True
    else:
        status_4_is_exist = False

    if status_5 is not None:
        status_5_is_exist = True
    else:
        status_5_is_exist = False

    return status_5_is_exist, status_4_is_exist, status_3_is_exist, status_2_is_exist, status_1_is_exist


def create_statuses():

    for db in get_session():
        statuses = []

    status_5_is_exist, status_4_is_exist, status_3_is_exist, status_2_is_exist, status_1_is_exist = check_statuses(db=db)
    if not status_1_is_exist:
        statuses.append(Status(id=1, name="Создано"))

    if not status_2_is_exist:
        statuses.append(Status(id=2, name="Принято"))

    if not status_3_is_exist:
        statuses.append(Status(id=3, name="В процессе"))

    if not status_4_is_exist:
        statuses.append(Status(id=4, name="Выполнено"))

    if not status_5_is_exist:
        statuses.append(Status(id=5, name="Проблема"))

    [db.add(status) for status in statuses]
    db.commit()
    db.close()


def check_type_objects(db: Session):
    type_1 = db.query(TypeObject).filter(TypeObject.name == 'Лифт без МП', TypeObject.id == 1).first()
    type_2 = db.query(TypeObject).filter(TypeObject.name == 'Лифт с МП', TypeObject.id == 2).first()
    type_3 = db.query(TypeObject).filter(TypeObject.name == 'Траволатор', TypeObject.id == 3).first()
    type_4 = db.query(TypeObject).filter(TypeObject.name == 'Эскалатор', TypeObject.id == 4).first()
    type_5 = db.query(TypeObject).filter(TypeObject.name == 'Грузовой лифт', TypeObject.id == 5).first()
    type_6 = db.query(TypeObject).filter(TypeObject.name == 'Инвалидный подъемник', TypeObject.id == 6).first()

    if type_1 is not None:
        type_1_is_exist = True
    else:
        type_1_is_exist = False

    if type_2 is not None:
        type_2_is_exist = True
    else:
        type_2_is_exist = False

    if type_3 is not None:
        type_3_is_exist = True
    else:
        type_3_is_exist = False

    if type_4 is not None:
        type_4_is_exist = True
    else:
        type_4_is_exist = False

    if type_5 is not None:
        type_5_is_exist = True
    else:
        type_5_is_exist = False

    if type_6 is not None:
        type_6_is_exist = True
    else:
        type_6_is_exist = False

    return type_6_is_exist, type_5_is_exist, type_4_is_exist, type_3_is_exist, type_2_is_exist, type_1_is_exist


def create_type_objects():
    for db in get_session():
        type_objects = []

    type_6_is_exist, type_5_is_exist, type_4_is_exist, type_3_is_exist, type_2_is_exist, type_1_is_exist = \
        check_type_objects(db=db)
    if not type_1_is_exist:
        type_objects.append(TypeObject(id=1, name="Лифт без МП"))
    if not type_2_is_exist:
        type_objects.append(TypeObject(id=2, name="Лифт с МП"))
    if not type_3_is_exist:
        type_objects.append(TypeObject(id=3, name="Траволатор"))
    if not type_4_is_exist:
        type_objects.append(TypeObject(id=4, name="Эскалатор"))
    if not type_5_is_exist:
        type_objects.append(TypeObject(id=5, name="Грузовой лифт"))
    if not type_6_is_exist:
        type_objects.append(TypeObject(id=6, name="Инвалидный подъемник"))

    [db.add(t_o) for t_o in type_objects]
    db.commit()
    db.close()


def check_type_contracts(db: Session):
    type_1 = db.query(TypeContract).filter(TypeContract.name == 'Государственный', TypeContract.id == 1).first()
    type_2 = db.query(TypeContract).filter(TypeContract.name == 'Коммерческий', TypeContract.id == 2).first()
    if type_1 is not None:
        type_1_is_exist = True
    else:
        type_1_is_exist = False

    if type_2 is not None:
        type_2_is_exist = True
    else:
        type_2_is_exist = False

    return type_2_is_exist, type_1_is_exist


def create_type_contracts():
    for db in get_session():
        type_contracts = []

    type_2_is_exist, type_1_is_exist = check_type_contracts(db=db)
    if not type_1_is_exist:
        type_contracts.append(TypeContract(id=1, name="Государственный"))
    if not type_2_is_exist:
        type_contracts.append(TypeContract(id=2, name="Коммерческий"))

    [db.add(t_o) for t_o in type_contracts]
    db.commit()
    db.close()


def check_locations(db: Session):
    loc_1 = db.query(Location).filter(Location.name == 'Краснодар', Location.id == 1).first()
    loc_2 = db.query(Location).filter(Location.name == 'Москва', Location.id == 2).first()
    loc_3 = db.query(Location).filter(Location.name == 'Ростов на Дону', Location.id == 3).first()
    if loc_1 is not None:
        loc_1_is_exist = True
    else:
        loc_1_is_exist = False
    if loc_2 is not None:
        loc_2_is_exist = True
    else:
        loc_2_is_exist = False
    if loc_3 is not None:
        loc_3_is_exist = True
    else:
        loc_3_is_exist = False
    return loc_1_is_exist, loc_2_is_exist, loc_3_is_exist


def create_locations():
    for db in get_session():
        locations = []

    loc_1_is_exist, loc_2_is_exist, loc_3_is_exist = check_locations(db=db)
    if not loc_1_is_exist:
        locations.append(Location(id=1, name="Краснодар"))
    if not loc_2_is_exist:
        locations.append(Location(id=2, name="Москва"))
    if not loc_3_is_exist:
        locations.append(Location(id=3, name="Ростов на Дону"))

    [db.add(loc) for loc in locations]
    db.commit()
    db.close()


def check_fault_category(db: Session):
    fc_1 = db.query(FaultCategory).filter(
        FaultCategory.name == 'AA (Застревание пассажира. Опасность)', FaultCategory.id == 1).first()
    fc_2 = db.query(FaultCategory).filter(
        FaultCategory.name == 'А (Остановка лифта, подъемника, эскалатора, траволатора)', FaultCategory.id == 2).first()
    fc_3 = db.query(FaultCategory).filter(
        FaultCategory.name == 'В (Ухудшение рабочих характеристик, требуется наладка)', FaultCategory.id == 3).first()
    fc_4 = db.query(FaultCategory).filter(
        FaultCategory.name == 'Н (Незначительные проблемы)', FaultCategory.id == 4).first()
    fc_5 = db.query(FaultCategory).filter(
        FaultCategory.name == 'Д (Заказчик или другие)', FaultCategory.id == 5).first()
    fc_6 = db.query(FaultCategory).filter(FaultCategory.name == 'ТО (Плановые работы)', FaultCategory.id == 6).first()
    fc_7 = db.query(FaultCategory).filter(
        FaultCategory.name == 'ПТО (Периодическое техническое освидетельствование)', FaultCategory.id == 7).first()
    fc_8 = db.query(FaultCategory).filter(
        FaultCategory.name == 'КР (Капитальный ремонт, Ремонт)', FaultCategory.id == 8).first()
    fc_9 = db.query(FaultCategory).filter(FaultCategory.name == 'С (Проблемы по связи)', FaultCategory.id == 9).first()
    fc_10 = db.query(FaultCategory).filter(FaultCategory.name == 'Л (Ложный вызов)', FaultCategory.id == 10).first()

    if fc_1 is not None:
        fc_1_is_exist = True
    else:
        fc_1_is_exist = False
    if fc_2 is not None:
        fc_2_is_exist = True
    else:
        fc_2_is_exist = False
    if fc_3 is not None:
        fc_3_is_exist = True
    else:
        fc_3_is_exist = False

    if fc_4 is not None:
        fc_4_is_exist = True
    else:
        fc_4_is_exist = False
    if fc_5 is not None:
        fc_5_is_exist = True
    else:
        fc_5_is_exist = False
    if fc_6 is not None:
        fc_6_is_exist = True
    else:
        fc_6_is_exist = False
    if fc_7 is not None:
        fc_7_is_exist = True
    else:
        fc_7_is_exist = False
    if fc_8 is not None:
        fc_8_is_exist = True
    else:
        fc_8_is_exist = False
    if fc_9 is not None:
        fc_9_is_exist = True
    else:
        fc_9_is_exist = False
    if fc_10 is not None:
        fc_10_is_exist = True
    else:
        fc_10_is_exist = False
    return fc_1_is_exist, fc_2_is_exist, fc_3_is_exist, fc_4_is_exist, fc_5_is_exist\
        , fc_6_is_exist, fc_7_is_exist, fc_8_is_exist, fc_9_is_exist, fc_10_is_exist


def create_fault_category():
    for db in get_session():
        fault_categories = []

    fc_1_is_exist, fc_2_is_exist, fc_3_is_exist, fc_4_is_exist, fc_5_is_exist, fc_6_is_exist, fc_7_is_exist,\
    fc_8_is_exist, fc_9_is_exist, fc_10_is_exist = check_fault_category(db=db)
    if not fc_1_is_exist:
        fault_categories.append(FaultCategory(id=1, name="AA (Застревание пассажира. Опасность)"))
    if not fc_2_is_exist:
        fault_categories.append(FaultCategory(id=2, name="А (Остановка лифта, подъемника, эскалатора, траволатора)"))
    if not fc_3_is_exist:
        fault_categories.append(FaultCategory(id=3, name="В (Ухудшение рабочих характеристик, требуется наладка)"))
    if not fc_4_is_exist:
        fault_categories.append(FaultCategory(id=4, name="Н (Незначительные проблемы)"))
    if not fc_5_is_exist:
        fault_categories.append(FaultCategory(id=5, name="Д (Заказчик или другие)"))
    if not fc_6_is_exist:
        fault_categories.append(FaultCategory(id=6, name="ТО (Плановые работы)"))
    if not fc_7_is_exist:
        fault_categories.append(FaultCategory(id=7, name="ПТО (Периодическое техническое освидетельствование)"))
    if not fc_8_is_exist:
        fault_categories.append(FaultCategory(id=8, name="КР (Капитальный ремонт, Ремонт)"))
    if not fc_9_is_exist:
        fault_categories.append(FaultCategory(id=9, name="С (Проблемы по связи)"))
    if not fc_10_is_exist:
        fault_categories.append(FaultCategory(id=10, name="Л (Ложный вызов)"))

    [db.add(fc) for fc in fault_categories]
    db.commit()
    db.close()


def create_initial_data():
    try:
        create_roles()
    except Exception as ex:
        print(f"НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ РОЛЕЙ {ex}")
    try:
        create_statuses()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ СТАТУСОВ")
    try:
        create_type_objects()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ ТИПЫ ТЕХНИКИ")
    try:
        create_type_contracts()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ ТИПЫ КОНТРАКТЫ")
    try:
        create_locations()
    except :
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ ГОРОДОВ")
    try:
        create_fault_category()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ КАТЕГОРИЙ НЕИСПРАВНОСТИ")
