FROM python:3.8

WORKDIR /app/

RUN pip3 install pip==23.0
# Копирование файлов из директории ./app в контейнер
COPY ./app /app

# Установка зависимостей из файла req.txt
COPY req.txt /app/
RUN pip3 install -r req.txt

ENV C_FORCE_ROOT=1
ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
