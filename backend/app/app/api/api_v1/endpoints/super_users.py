import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from fastapi.params import Path

from app.api import deps
from app.core.response import SingleEntityResponse
from app.core.security import create_token_moderator
from app.schemas.token import TokenBase

from app.schemas.super_users import SuperUserEntrance, SuperUserGet

from app.getters.super_user import get_super_user

from app.exceptions import UnfoundEntity, InaccessibleEntity
from app.schemas.super_users import SuperUserRequest

# from app.crud.crud_super_users import crud_super_users

from app.core.security import get_password_hash
from app.crud.crud_location import crud_location
from app.exceptions import UnprocessableEntity
from app.utils.time_stamp import date_from_timestamp

from app.crud.crud_super_users import crud_super_users

from app.getters.super_user import get_super_user_delete

router = APIRouter()


# TEST for Vova
@router.get('/test-vova/',
            name='Тест для вовы',
            description='Должен получить цифру 2',
            tags=['Инструменты'])
def test_for_vova():
    return "2"


# SIGN-IN
# Вход по почте и паролю
@router.post('/cp/sign-in/', response_model=SingleEntityResponse[TokenBase],
             name='Войти в админ панель',
             description='Войти в админ панель',
             tags=['Вход / Админ панель'])
def entrance(
    super_user: SuperUserEntrance,
    session=Depends(deps.get_db),
):
    db_obj = crud_super_users.get_super_user(session, super_user=super_user)
    token = create_token_moderator(subject=db_obj.id)  # переделать получение токена, через модератора
    return SingleEntityResponse(data=TokenBase(token=token))


# GET
@router.get('/cp/super-user/me/',
            response_model=SingleEntityResponse[SuperUserGet],
            name='Получить данные профиля ',
            description='Получение всех  данных профиля супер-юзера, по токену',
            tags=['Админ панель / Профиль']
            )
def get_data(
        request: Request,
        current_super_user=Depends(deps.get_current_super_user_by_bearer),
):
    return SingleEntityResponse(data=get_super_user(current_super_user, request=request))


# UPDATE SELF
@router.put('/cp/super-user/me/',
            response_model=SingleEntityResponse[SuperUserGet],
            name='Изменить данные Супер-юзера',
            description='Изменить данные текущего Супер-юзера',
            tags=['Админ панель / Профиль']
            )
def update_super_user(
        request: Request,
        new_data: SuperUserRequest,

        current_super_user=Depends(deps.get_current_super_user_by_bearer),
        session=Depends(deps.get_db),
):

    db_obj, code, index = crud_super_users.updating_super_user_self(
        db=session, current_super_user=current_super_user, obj_in=new_data)
    if code == -1:
        raise UnfoundEntity(
            message="Супер-юзера с таким id не существует!",
            num=1,
            description="Супер-юзера с таким id не существует!",
            path="$.body"
        )
    if code == -2:
        raise UnfoundEntity(message="Неправильно указан город",
                            num=4,
                            description="Попробуйте указать город еще раз!",
                            path="$.body",
                            )
    if code == -3:
        raise InaccessibleEntity(message="Вы не обладаете правами назначать себя администратором",
                                 num=3,
                                 description="Вы не обладаете правами!",
                                 path="$.body",
                                 )

    return SingleEntityResponse(data=get_super_user(db_obj, request=request))


# CREATE NEW SUPER_USER ADMIN
# Создание юзера без токена
@router.post('/cp/create-super-user/',
             response_model=SingleEntityResponse[SuperUserGet],
             name='Создать супер-юзера',
             description='Создать супер-юзера',
             tags=['Инструменты']
             )
def create_super_user(
        request: Request,
        new_data: SuperUserRequest,
        session=Depends(deps.get_db),
):

    # проверка локации
    if new_data.location_id is not None:
        loc = crud_location.get(db=session, id=new_data.location_id)
        if loc is None:
            raise UnfoundEntity(
                message="Такого города нет!",
                num=3,
                description="Введен неправильный id города!",
                path="$.body"
            )

    db_obj = crud_super_users.get_by_email(db=session, email=new_data.email)
    if db_obj is not None:
        raise UnprocessableEntity(
            message="Супер-юзер с таким логином уже существует!",
            num=5,
            description="Попробуйте изменить логин для нового Супер-юзера!",
            path="$.body"
        )
    psw = get_password_hash(password=new_data.password)
    new_data.password = psw
    if new_data.birthday is not None:
        new_data.birthday = date_from_timestamp(new_data.birthday)
    return SingleEntityResponse(data=get_super_user(crud_super_users.create(db=session, obj_in=new_data),
                                                    request=request))


# UPDATE PHOTO BY TOKEN IN SUPER_USER
@router.put("/cp/super-user/me/photo/",
            response_model=SingleEntityResponse[SuperUserGet],
            name='Изменить фотографию',
            description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
            tags=['Админ панель / Профиль'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_super_user=Depends(deps.get_current_super_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    super_user_id = current_super_user.id
    save_path = crud_super_users.adding_photo(db=session, file=file, id_super_user=super_user_id)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_super_user(current_super_user, request=request))


# DELETE
@router.delete("/cp/super-user/me/",
               response_model=SingleEntityResponse,
               name='Удаляет текущего супер-юзера',
               description='Супер-юзер сам удаляет свой акк',
               tags=['Админ панель / Профиль'])
def remove_with_path(
        request: Request,
        current_super_user=Depends(deps.get_current_super_user_by_bearer),
        session=Depends(deps.get_db)
):
    return SingleEntityResponse(data=get_super_user_delete(
        crud_super_users.remove(db=session, id=current_super_user.id), request=request))


# CREATE NEW SUPER_USER
@router.post('/cp/super-user/super-user/',
             response_model=SingleEntityResponse[SuperUserGet],
             name='Создать супер-юзера',
             description='Создать супер-юзера',
             tags=['Админ панель / Руководитель']
             )
def create_super_user(
        request: Request,
        new_data: SuperUserRequest,
        current_super_user=Depends(deps.get_current_super_user_by_bearer),
        session=Depends(deps.get_db),
):

    admin = crud_super_users.get(db=session, id=current_super_user.id)
    if admin is None:
        raise UnfoundEntity(
            message="Токен не распознан!",
            num=1,
            description="Такого Супер-юзера не существует!",
            path="$.body"
        )
    if admin.is_super_user is not True:
        raise InaccessibleEntity(
            message="Юзер не обладает правами!",
            num=2,
            description="Юзер не обладает правами, к созданию других Юзеров!",
            path="$.body"
        )
    # проверка локации и зоны ответственности
    if new_data.location_id is not None:
        loc = crud_location.get(db=session, id=new_data.location_id)
        if loc is None:
            raise UnfoundEntity(
                message="Такого города нет!",
                num=3,
                description="Введен неправильный id города!",
                path="$.body"
            )

    db_obj = crud_super_users.get_by_email(db=session, email=new_data.email)
    if db_obj is not None:
        raise UnprocessableEntity(
            message="Супер-юзер с таким логином уже существует!",
            num=5,
            description="Попробуйте изменить логин для нового Супер-юзера!",
            path="$.body"
        )
    psw = get_password_hash(password=new_data.password)
    new_data.password = psw
    if new_data.birthday is not None:
        new_data.birthday = date_from_timestamp(new_data.birthday)
    return SingleEntityResponse(data=get_super_user(crud_super_users.create(db=session, obj_in=new_data),
                                                    request=request))


# UPDATE PHOTO BY TOKEN
# @router.put("/cp/moderators/me/photos/",
#             response_model=SingleEntityResponse[ModeratorGet],
#             name='Изменить фотографию',
#             description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
#             tags=['Админ панель / Профиль'],
#             )
# def create_upload_file(
#         request: Request,
#         file: Optional[UploadFile] = File(None),
#         current_moderator=Depends(deps.get_current_moderator_by_bearer),
#         session=Depends(deps.get_db),
#         ):
#     moderator_id = current_moderator.id
#     save_path = crud_moderator.adding_photo(db=session, file=file, id_moderator=moderator_id)
#     if not save_path:
#         raise UnfoundEntity(message="Не отправлен загружаемый файл",
#                             num=2,
#                             description="Попробуйте загрузить файл еще раз",
#                             path="$.body",
#                             )
#     return SingleEntityResponse(data=get_moderator(current_moderator, request=request))


if __name__ == "__main__":
    logging.info('Running...')
