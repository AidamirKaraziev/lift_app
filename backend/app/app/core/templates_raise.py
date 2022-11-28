from app.exceptions import UnprocessableEntity, InaccessibleEntity, UnfoundEntity


email_already_have = -100
location_not_found = -101

role_not_found = -102
role_incorrectly_selected = -1021  # неправильно выбрано, попытка создать клиента
role_without_access = -1022  # недостаточно прав
role_no_rights = -1023  # нет прав
role_changeable_list = -1024  # Не входит в список меняемых пользователей

working_specialty_not_found = -103

division_not_found = -104
division_not_none = -1041  # уже существует такой
division_cannot_be_assigned_to_this_user = -1042  # нельзя назначить этому пользователю
division_is_not_actual = -1043  # НЕ АКТУАЛЬНЫЙ УЧАСТОК

user_not_found = -105

company_not_found = -106
company_already_exists = -1061  # Такая компания уже есть

not_is_actual = -107
not_attribute_in_model = -108

checked_items_is_not_in_the_list = -109  # Одного из проверяемых элементов нет в проверяемом списке


def get_raise(code: int):
    if code == -100:
        raise InaccessibleEntity(
            message="Пользователь с таким email уже есть!",
            num=100,
            description="Укажите другой email, для регистрации",
            path="$.body"
        )
    if code == -101:
        raise UnfoundEntity(
            message="Такого города не существует!",
            num=101,
            description="Выберете существующий город!",
            path="$.body"
        )
    if code == -102:
        raise UnfoundEntity(
            message="Такой Должности нет!",
            num=102,
            description="Выберете существующую должность!",
            path="$.body"
        )
    if code == -1021:
        raise InaccessibleEntity(
            message="Неправильно выбрана должность!",
            num=1021,
            description="Выберете правильную должность!!",
            path="$.body"
        )
    if code == -1022:
        raise InaccessibleEntity(
            message="Пользователь не обладает правами!",
            num=1022,
            description="Пользователь не обладает правами, к созданию других пользователей!",
            path="$.body"
        )
    if code == -1023:
        raise InaccessibleEntity(
            message="Вы не обладаете правами!",
            num=1023,
            description="Пользователь не обладает правами!",
            path="$.body"
        )
    if code == -1024:
        raise InaccessibleEntity(
            message="Этого пользователя нет в изменяемом списке!",
            num=1024,
            description="Этого пользователя нет в изменяемом списке!",
            path="$.body"
        )
    if code == -103:
        raise UnfoundEntity(
            message="Такой Специальности нет!",
            num=103,
            description="Выберете существующую Специальность!",
            path="$.body"
        )
    if code == -104:
        raise UnfoundEntity(
            message="Такого Участка нет!",
            num=104,
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
    if code == -1042:
        raise UnprocessableEntity(
            message="Нельзя назначить этому пользователю участок!",
            num=1042,
            description="Нельзя назначить этому пользователю участок!",
            path="$.body"
        )
    if code == -1043:
        raise UnprocessableEntity(
            message="Участок не актуален!",
            num=1043,
            description="Участок был удален или заморожен!",
            path="$.body"
        )
    if code == -105:
        raise UnfoundEntity(
            message="Нет такого пользователя!",
            num=105,
            description="Нет пользователя с таким id!",
            path="$.body"
        )
    if code == -106:
        raise UnfoundEntity(
            message="Такой компании нет!",
            num=106,
            description="Выберете существующую Компанию или создайте новую!",
            path="$.body"
        )
    if code == -1061:
        raise UnprocessableEntity(
            message="Такая компания уже есть в базе данных",
            num=1,
            description="Компания с таким названием уже есть в базе данных!",
            path="$.body"
        )
    if code == -107:
        raise UnprocessableEntity(
            message="Пользователь не актуален!",
            num=107,
            description="Статус пользователя не актуален, возможно его удалили!",
            path="$.body"
        )

    if code == -108:
        raise UnprocessableEntity(
            message="Модель в базе данных не имеет такого атрибута для файла!",
            num=108,
            description="Модель в базе данных не имеет такого атрибута для файла!",
            path="$.body"
        )
    if code == -109:
        raise UnprocessableEntity(
            message="Один из проверяемых элементов отсутствует в списке",
            num=109,
            description="Один из проверяемых элементов отсутствует в списке",
            path="$.body"
        )
    if code != 0:
        raise UnfoundEntity(
            message=f"АЙДАМИР ВНЕСИ RAISE {code}",
            num=999,
            description=f"АЙДАМИР ВНЕСИ RAISE {code}",
            path="$.body"
            )
