# Указываем базовый образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка последней версии Poetry (совместимой с вашим pyproject.toml)
RUN pip install --upgrade pip && \
    pip install poetry==2.0.0

# Проверяем установку
RUN poetry --version

# Копирование файлов проекта
COPY pyproject.toml poetry.lock* ./

# Показываем структуру pyproject.toml
RUN cat pyproject.toml

# Настройка Poetry
RUN poetry config virtualenvs.create false

# Установка зависимостей
RUN poetry install --no-interaction -v

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]