from sqlalchemy.orm import Session
from sqlalchemy import select

from app import crud, schemas
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.core.config import settings
from app.db import session
from app.db.session import get_session
from app.models import Role, Status, TypeObject, TypeContract, Location, FaultCategory, ReasonFault, TypeAct, CostType


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


def check_cost_type(db: Session):
    check_list = [
        CostType(id=1, name='С НДС'),
        CostType(id=2, name='Без НДС')]
    creation_list = []
    for obj in check_list:
        query = db.query(CostType).filter(CostType.id == obj.id, CostType.name == obj.name).first()
        if query is None:
            creation_list.append(obj)
    return creation_list


def create_cost_type():
    for db in get_session():
        creation_list = check_cost_type(db)
        [db.add(obj) for obj in creation_list]
        db.commit()
        db.close()


def check_roles(db: Session):
    check_list = [
        Role(id=1, name='Админ'),
        Role(id=2, name='Прораб'),
        Role(id=3, name='Механик'),
        Role(id=4, name='Инженер наладчик'),
        Role(id=5, name='Диспетчер'),
        Role(id=6, name='Клиент')
    ]
    creation_list = []
    for obj in check_list:
        query = db.query(Role).filter(Role.id == obj.id, Role.name == obj.name).first()
        if query is None:
            creation_list.append(obj)
    return creation_list


def create_roles():
    for db in get_session():
        creation_list = check_roles(db)
        [db.add(obj) for obj in creation_list]
        db.commit()
        db.close()


def check_statuses(db: Session):
    check_list = [
        Status(id=1, name='Создано'),
        Status(id=2, name='Принято'),
        Status(id=3, name='В процессе'),
        Status(id=4, name='Выполнено'),
        Status(id=5, name='Проблема')
    ]
    creation_list = []
    for obj in check_list:
        query = db.query(Status).filter(Status.id == obj.id, Status.name == obj.name).first()
        if query is None:
            creation_list.append(obj)
    return creation_list


def create_statuses():
    for db in get_session():
        creation_list = check_statuses(db)
        [db.add(obj) for obj in creation_list]
        db.commit()
        db.close()


def check_type_objects(db: Session):
    check_list = [
        Status(id=1, name='Лифт без МП'),
        Status(id=2, name='Лифт с МП'),
        Status(id=3, name='Траволатор'),
        Status(id=4, name='Эскалатор'),
        Status(id=5, name='Грузовой лифт'),
        Status(id=6, name='Инвалидный подъемник'),
    ]
    creation_list = []
    for obj in check_list:
        query = db.query(Status).filter(Status.id == obj.id, Status.name == obj.name).first()
        if query is None:
            creation_list.append(obj)
    return creation_list


def create_type_objects():
    for db in get_session():
        creation_list = check_type_objects(db)
        [db.add(obj) for obj in creation_list]
        db.commit()
        db.close()


def check_type_contracts(db: Session):
    check_list = [
        Status(id=1, name='Государственный'),
        Status(id=2, name='Коммерческий')
    ]
    creation_list = []
    for obj in check_list:
        query = db.query(Status).filter(Status.id == obj.id, Status.name == obj.name).first()
        if query is None:
            creation_list.append(obj)
    return creation_list


def create_type_contracts():
    for db in get_session():
        creation_list = check_type_contracts(db)
        [db.add(obj) for obj in creation_list]
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


def check_reason_fault(db: Session):
    r_f_1 = db.query(ReasonFault).filter(ReasonFault.name == 'Авария главного привода по УКСЛ.', ReasonFault.id == 1).first()
    r_f_2 = db.query(ReasonFault).filter(ReasonFault.name == 'АБЛ', ReasonFault.id == 2).first()
    r_f_3 = db.query(ReasonFault).filter(ReasonFault.name == 'Не сработал датчик УБ', ReasonFault.id == 3).first()
    r_f_4 = db.query(ReasonFault).filter(ReasonFault.name == 'NAV - не готов, очень серьезная ошибка',
                                         ReasonFault.id == 4).first()
    r_f_5 = db.query(ReasonFault).filter(ReasonFault.name == '43 - не исправна цепь блокировки.',
                                         ReasonFault.id == 5).first()
    r_f_6 = db.query(ReasonFault).filter(ReasonFault.name == '160 - проникновение в шахту.',
                                         ReasonFault.id == 6).first()
    r_f_7 = db.query(ReasonFault).filter(ReasonFault.name == '28 - залипание верхних и нижних концевых выключателей.',
                                         ReasonFault.id == 7).first()
    r_f_8 = db.query(ReasonFault).filter(ReasonFault.name == '17 - отсутствует сигнал от инвертора.',
                                         ReasonFault.id == 8).first()
    r_f_9 = db.query(ReasonFault).filter(ReasonFault.name == '47 - многократный реверс.', ReasonFault.id == 9).first()
    r_f_10 = db.query(ReasonFault).filter(ReasonFault.name == '41 - разрыв цепи безопасности.',
                                          ReasonFault.id == 10).first()
    r_f_11 = db.query(ReasonFault).filter(ReasonFault.name == '72 - разомкнута KV-15 или выключателей ДК.',
                                          ReasonFault.id == 11).first()
    r_f_12 = db.query(ReasonFault).filter(ReasonFault.name == 'ТО', ReasonFault.id == 12).first()
    r_f_13 = db.query(ReasonFault).filter(ReasonFault.name == '21 - время перемещения превышает заданное время.',
                                          ReasonFault.id == 13).first()
    r_f_14 = db.query(ReasonFault).filter(ReasonFault.name == '10 - разрыв цепи аварийной опасности.',
                                          ReasonFault.id == 14).first()
    r_f_15 = db.query(ReasonFault).filter(ReasonFault.name == 'Нет Связи.', ReasonFault.id == 15).first()
    r_f_16 = db.query(ReasonFault).filter(ReasonFault.name == '44 - Охрана шахты.', ReasonFault.id == 16).first()
    r_f_17 = db.query(ReasonFault).filter(ReasonFault.name == 'Сгорел блок обь.', ReasonFault.id == 17).first()
    r_f_18 = db.query(ReasonFault).filter(ReasonFault.name == 'Пожарная опасность.', ReasonFault.id == 18).first()
    r_f_19 = db.query(ReasonFault).filter(ReasonFault.name == '5 - ошибка тормоза.', ReasonFault.id == 19).first()
    r_f_20 = db.query(ReasonFault).filter(ReasonFault.name == 'Перезапуск в присутствии механика.',
                                          ReasonFault.id == 20).first()
    if r_f_1 is not None:
        r_f_1_is_exist = True
    else:
        r_f_1_is_exist = False
    if r_f_2 is not None:
        r_f_2_is_exist = True
    else:
        r_f_2_is_exist = False
    if r_f_3 is not None:
        r_f_3_is_exist = True
    else:
        r_f_3_is_exist = False

    if r_f_4 is not None:
        r_f_4_is_exist = True
    else:
        r_f_4_is_exist = False
    if r_f_5 is not None:
        r_f_5_is_exist = True
    else:
        r_f_5_is_exist = False
    if r_f_6 is not None:
        r_f_6_is_exist = True
    else:
        r_f_6_is_exist = False
    if r_f_7 is not None:
        r_f_7_is_exist = True
    else:
        r_f_7_is_exist = False
    if r_f_8 is not None:
        r_f_8_is_exist = True
    else:
        r_f_8_is_exist = False
    if r_f_9 is not None:
        r_f_9_is_exist = True
    else:
        r_f_9_is_exist = False
    if r_f_10 is not None:
        r_f_10_is_exist = True
    else:
        r_f_10_is_exist = False
    if r_f_11 is not None:
        r_f_11_is_exist = True
    else:
        r_f_11_is_exist = False
    if r_f_12 is not None:
        r_f_12_is_exist = True
    else:
        r_f_12_is_exist = False
    if r_f_13 is not None:
        r_f_13_is_exist = True
    else:
        r_f_13_is_exist = False

    if r_f_14 is not None:
        r_f_14_is_exist = True
    else:
        r_f_14_is_exist = False
    if r_f_15 is not None:
        r_f_15_is_exist = True
    else:
        r_f_15_is_exist = False
    if r_f_16 is not None:
        r_f_16_is_exist = True
    else:
        r_f_16_is_exist = False
    if r_f_17 is not None:
        r_f_17_is_exist = True
    else:
        r_f_17_is_exist = False
    if r_f_18 is not None:
        r_f_18_is_exist = True
    else:
        r_f_18_is_exist = False
    if r_f_19 is not None:
        r_f_19_is_exist = True
    else:
        r_f_19_is_exist = False
    if r_f_20 is not None:
        r_f_20_is_exist = True
    else:
        r_f_20_is_exist = False

    return r_f_1_is_exist, r_f_2_is_exist, r_f_3_is_exist, r_f_4_is_exist, r_f_5_is_exist, r_f_6_is_exist, \
           r_f_7_is_exist, r_f_8_is_exist, r_f_9_is_exist, r_f_10_is_exist, r_f_11_is_exist, r_f_12_is_exist,\
           r_f_13_is_exist, r_f_14_is_exist, r_f_15_is_exist, r_f_16_is_exist, r_f_17_is_exist, r_f_18_is_exist, \
           r_f_19_is_exist, r_f_20_is_exist


def create_reason_fault():
    for db in get_session():
        reasons_faults = []
    r_f_1_is_exist, r_f_2_is_exist, r_f_3_is_exist, r_f_4_is_exist, r_f_5_is_exist, r_f_6_is_exist, \
    r_f_7_is_exist, r_f_8_is_exist, r_f_9_is_exist, r_f_10_is_exist, r_f_11_is_exist, r_f_12_is_exist, \
    r_f_13_is_exist, r_f_14_is_exist, r_f_15_is_exist, r_f_16_is_exist, r_f_17_is_exist, r_f_18_is_exist, \
    r_f_19_is_exist, r_f_20_is_exist = check_reason_fault(db=db)

    if not r_f_1_is_exist:
        reasons_faults.append(ReasonFault(id=1, name='Авария главного привода по УКСЛ.'))
    if not r_f_2_is_exist:
        reasons_faults.append(ReasonFault(id=2, name='АБЛ'))
    if not r_f_3_is_exist:
        reasons_faults.append(ReasonFault(id=3, name='Не сработал датчик УБ'))
    if not r_f_4_is_exist:
        reasons_faults.append(ReasonFault(id=4, name='NAV - не готов, очень серьезная ошибка'))
    if not r_f_5_is_exist:
        reasons_faults.append(ReasonFault(id=5, name="43 - не исправна цепь блокировки."))
    if not r_f_6_is_exist:
        reasons_faults.append(ReasonFault(id=6, name="160 - проникновение в шахту."))
    if not r_f_7_is_exist:
        reasons_faults.append(ReasonFault(id=7, name="28 - залипание верхних и нижних концевых выключателей."))
    if not r_f_8_is_exist:
        reasons_faults.append(ReasonFault(id=8, name="17 - отсутствует сигнал от инвертора."))
    if not r_f_9_is_exist:
        reasons_faults.append(ReasonFault(id=9, name="47 - многократный реверс."))
    if not r_f_10_is_exist:
        reasons_faults.append(ReasonFault(id=10, name="41 - разрыв цепи безопасности."))
    if not r_f_11_is_exist:
        reasons_faults.append(ReasonFault(id=11, name="72 - разомкнута KV-15 или выключателей ДК."))
    if not r_f_12_is_exist:
        reasons_faults.append(ReasonFault(id=12, name="ТО"))
    if not r_f_13_is_exist:
        reasons_faults.append(ReasonFault(id=13, name="21 - время перемещения превышает заданное время."))
    if not r_f_14_is_exist:
        reasons_faults.append(ReasonFault(id=14, name="10 - разрыв цепи аварийной опасности."))
    if not r_f_15_is_exist:
        reasons_faults.append(ReasonFault(id=15, name="Нет Связи."))
    if not r_f_16_is_exist:
        reasons_faults.append(ReasonFault(id=16, name="44 - Охрана шахты."))
    if not r_f_17_is_exist:
        reasons_faults.append(ReasonFault(id=17, name="Сгорел блок обь."))
    if not r_f_18_is_exist:
        reasons_faults.append(ReasonFault(id=18, name="Пожарная опасность."))
    if not r_f_19_is_exist:
        reasons_faults.append(ReasonFault(id=19, name="5 - ошибка тормоза."))
    if not r_f_20_is_exist:
        reasons_faults.append(ReasonFault(id=20, name="Перезапуск в присутствии механика."))

    [db.add(r_f) for r_f in reasons_faults]
    db.commit()
    db.close()


def check_type_acts(db: Session):
    ta_1 = db.query(TypeAct).filter(TypeAct.name == 'ТО 1', TypeAct.id == 1).first()
    ta_3 = db.query(TypeAct).filter(TypeAct.name == 'ТО 3', TypeAct.id == 3).first()
    ta_6 = db.query(TypeAct).filter(TypeAct.name == 'ТО 6', TypeAct.id == 6).first()
    ta_12 = db.query(TypeAct).filter(TypeAct.name == 'ТО 12', TypeAct.id == 12).first()

    if ta_1 is not None:
        ta_1_is_exist = True
    else:
        ta_1_is_exist = False
    if ta_3 is not None:
        ta_3_is_exist = True
    else:
        ta_3_is_exist = False
    if ta_6 is not None:
        ta_6_is_exist = True
    else:
        ta_6_is_exist = False

    if ta_12 is not None:
        ta_12_is_exist = True
    else:
        ta_12_is_exist = False

    return ta_1_is_exist, ta_3_is_exist, ta_6_is_exist, ta_12_is_exist


def create_type_act():
    for db in get_session():
        type_acts = []
    ta_1_is_exist, ta_3_is_exist, ta_6_is_exist, ta_12_is_exist = check_type_acts(db=db)

    if not ta_1_is_exist:
        type_acts.append(TypeAct(id=1, name='ТО 1'))
    if not ta_3_is_exist:
        type_acts.append(TypeAct(id=3, name='ТО 3'))
    if not ta_6_is_exist:
        type_acts.append(TypeAct(id=6, name='ТО 6'))
    if not ta_12_is_exist:
        type_acts.append(TypeAct(id=12, name='ТО 12'))

    [db.add(ta) for ta in type_acts]
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
    try:
        create_reason_fault()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ ПРИЧИН НЕИСПРАВНОСТИ")
    try:
        create_type_act()
    except:
        print("НЕ СОЗДАЛ БАЗУ ДАННЫХ ДЛЯ ТИПОВ АКТОВ")
    try:
        create_cost_type()
    except:
        print("НЕ СОЗДАЛ В БАЗЕ ДАННЫХ ТИПЫ ЦЕН")
