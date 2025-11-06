# Dockerfile
# Используем лёгкий базовый образ
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем системные зависимости чтобы всё компилировалось
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements-файлы
COPY requirements.txt requirements-dev.txt ./

# Устанавливаем зависимости (включая dev для тестов и линтеров)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копируем приложение
COPY ./app ./app
COPY ./tests ./tests

# Открываем порт для приложения
EXPOSE 8000

# Команда запуска Uvicorn. (По умолчанию запускаем сервер)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
