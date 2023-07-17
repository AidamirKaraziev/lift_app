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
from app.models import Role


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
    if admin_role_is_exist:
        pass
    if not admin_role_is_exist:
        roles.append(Role(id=1, name="admin"))

    if foreman_role_is_exist:
        pass
    if not foreman_role_is_exist:
        roles.append(Role(id=2, name="foreman"))

    if mechanic_role_is_exist:
        pass
    if not mechanic_role_is_exist:
        roles.append(Role(id=3, name="mechanic"))

    if engineer_role_is_exist:
        pass
    if not engineer_role_is_exist:
        roles.append(Role(id=4, name="engineer"))

    if dispatcher_role_is_exist:
        pass
    if not dispatcher_role_is_exist:
        roles.append(Role(id=5, name="dispatcher"))

    if client_role_is_exist:
        pass
    if not client_role_is_exist:
        roles.append(Role(id=6, name="client"))

    [db.add(role) for role in roles]
    db.commit()
    db.close()


def create_initial_data():
    create_roles()
