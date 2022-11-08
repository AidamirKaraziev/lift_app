from app.exceptions import UnprocessableEntity

from app.exceptions import InaccessibleEntity, UnfoundEntity

code: int = 1
email_already_have = -100
location_is_none_not_found = -101

role_is_none_not_found = -102
role_incorrectly_selected = -1021  # неправильно выбрано, попытка создать клиента
role_without_access = -1022  # недостаточно прав
role_no_rights = -1023  # нет прав


working_specialty_not_found = -103

division_not_found = -104
division_not_none = -1041  # уже существует такой
cannot_be_assigned_to_this_user = -1042  # нельзя назначить этому пользователю

user_not_found = -105

company_not_found = -106

not_is_actual = -107
not_attribute_in_model = -108

if code == -100:
    raise UnprocessableEntity(
        # message="Сферы деятельности с таким названием уже есть!",
        # num=2,
        # description="Выберите другое название сферы деятельности!",
        # path="$.body"
    )
if code == -101:
    raise UnprocessableEntity(
        # message="Сферы деятельности с таким названием уже есть!",
        # num=2,
        # description="Выберите другое название сферы деятельности!",
        # path="$.body"
    )
if code == -105:
    raise UnfoundEntity(
        message="Токен не распознан!",
        num=105,
        description="Такого пользователя не существует!",
        path="$.body"
    )
if code == -1022:
    raise InaccessibleEntity(
        message="Пользователь не обладает правами!",
        num=2,
        description="Пользователь не обладает правами, к созданию других пользователей!",
        path="$.body"
    )
if code == -1021:
    raise InaccessibleEntity(
        message="Неправильно выбрана должность!",
        num=2,
        description="Выберете правильную должность!!",
        path="$.body"
    )
if code == -1022:
    raise InaccessibleEntity(
        message="Вы не обладаете правами!",
        num=2,
        description="Пользователь не обладает правами, к созданию таких пользователей!",
        path="$.body"
    )
if code == -1023:
    raise InaccessibleEntity(
        message="Вы не обладаете правами!",
        num=2,
        description="Пользователь не обладает правами!",
        path="$.body"
    )
if code == -104:
    raise UnfoundEntity(
        message="Такого Участка нет!",
        num=8,
        description="Выберете существующую Участок или создайте новую!",
        path="$.body"
    )
# if code == -1041:
#     raise UnprocessableEntity(
#         message="Н!",
#         num=2,
#         description="Выберите другое название сферы деятельности!",
#         path="$.body"
#     )
if code == -106:
    raise UnfoundEntity(
        message="Такой компании нет!",
        num=106,
        description="Выберете существующую Компанию или создайте новую!",
        path="$.body"
    )
if code == -105:
    raise UnfoundEntity(
        message="Нет такого пользователя!",
        num=105,
        description="Нет пользователя с таким id!",
        path="$.body"
    )
if code == -107:
    raise UnprocessableEntity(
        message="Пользователь не актуален!",
        num=107,
        description="Статус пользователя не актуален, возможно его удалили!",
        path="$.body"
    )
if code == -101:
    raise UnfoundEntity(
        message="Такого города не существует!",
        num=101,
        description="Выберете существующий город!",
        path="$.body"
    )
if code == -108:
    raise UnprocessableEntity(
        message="Модель в базе данных не имеет такого атрибута для файла!",
        num=108,
        description="Модель в базе данных не имеет такого атрибута для файла!",
        path="$.body"
    )
