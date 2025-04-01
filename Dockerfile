FROM python:3.13.1

# Устанавливаем poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости через poetry без создания виртуального окружения
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Копируем весь проект
COPY . /app

# Открываем порт 8000 для Django
EXPOSE 8000

# Команда запуска Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]