FROM python:3.12.3
# Устанавливаем рабочую директорию в контейнере
WORKDIR /library_app
# Копируем зависимости в контейнер
COPY requirements.txt .
# Устанавливаем зависимости без кеширования версий
RUN pip install --no-cache-dir -r requirements.txt
# Копируем код приложения в контейнер
COPY . .
