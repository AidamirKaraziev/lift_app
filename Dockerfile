FROM python:3.8

# Установите рабочий каталог
WORKDIR /app

# Скопируйте зависимости
COPY req.txt .

# Установите зависимости
# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt

# Копируем остальной код приложения
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Добавляем скрипт для выполнения миграций и запуска приложения
COPY prestart.sh /prestart.sh
RUN chmod +x /prestart.sh

# Запустите скрипт prestart.sh и затем приложение
CMD ["sh", "-c", "/prestart.sh && uvicorn src.main:app --host 0.0.0.0 --port 8000 ${UVICORN_RELOAD}"]