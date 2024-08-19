#! /usr/bin/env bash

# Установите рабочий каталог для alembic и выполнения миграций
# shellcheck disable=SC2164
cd /app/src

# Run migrations
alembic upgrade head
