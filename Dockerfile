# Базовый образ Python
FROM python:3.10-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY snippet.py .
COPY .env .

# Команда запуска бота
CMD ["python", "snippet.py"]