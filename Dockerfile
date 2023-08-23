# Используем базовый образ Python
FROM python:3.10.6

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt /app/

# Копируем файл настроек в контейнер
# COPY .env .
# COPY .env /app/.env

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . /app/

# Команда для запуска приложения при старте контейнера
# CMD ["python", "manage.py", "runserver"]