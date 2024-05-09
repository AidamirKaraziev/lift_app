FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-2020-04-27

WORKDIR /app/

RUN pip3 install --upgrade pip
RUN pip install --force-reinstall httpcore==0.15
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2

# Копирование файлов из директории ./app в контейнер
COPY ./app /app

# Установка зависимостей из файла req.txt
COPY req.txt /app/
RUN pip3 install -r req.txt

COPY ./app /app
ENV PYTHONPATH=/app
