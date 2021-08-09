FROM python:3.9.2-slim-buster as base
RUN pip install poetry
COPY poetry.lock pyproject.toml ./

FROM base as production
RUN poetry add gunicorn
RUN poetry install
COPY ./todo_app ./todo_app
ENV WEBAPP_PORT=80
EXPOSE ${WEBAPP_PORT}
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:80", "todo_app.app:create_app()"]

FROM base as development
RUN poetry install
COPY ./todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
