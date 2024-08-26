# Используйте базовый образ Python
FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Копируйте файл зависимостей и установите зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте весь проект в контейнер
COPY . .

# Укажите переменную окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Укажите порт, который ваше приложение будет использовать
EXPOSE 5000

# Команда, которая будет выполнена при запуске контейнера
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
