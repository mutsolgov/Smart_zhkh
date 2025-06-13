# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Установка зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . /app/

# Копируем и делаем исполняемым entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Открываем порт
EXPOSE 8000

# Задаём точку входа
ENTRYPOINT ["/app/entrypoint.sh"]
