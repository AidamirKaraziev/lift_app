# Используем официальный образ Python 3.8 в качестве базового
FROM python:3.8-slim

# Устанавливаем системные зависимости, необходимые для сборки psycopg2
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY req.txt ./

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt

# Копируем исходный код в контейнер
COPY . .

# Команда по умолчанию для запуска вашего приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]