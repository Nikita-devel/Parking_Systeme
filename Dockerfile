# Використовуємо базовий образ Python 3.10
FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock $APP_HOME/
COPY alembic $APP_HOME/alembic
COPY main.py $APP_HOME/

# Копіюємо весь код додатка у контейнер
COPY src $APP_HOME/src

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

#  порт
EXPOSE 8000

# Запускаємо
CMD ["python", "main.py"]
