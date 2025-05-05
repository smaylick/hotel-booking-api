FROM python:3.13.1

# 1. Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# 2. Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# 3. Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# 4. Копируем весь проект
COPY . /app

# 5. PYTHONPATH = /app/src (чтобы Django видел config.settings)
ENV PYTHONPATH=/app/src

# Открываем порт 8000
EXPOSE 8000

# 6. Стандартная команда — runserver (миграции ты можешь делать в docker-compose)
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
