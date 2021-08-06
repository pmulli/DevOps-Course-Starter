FROM python:3.9.2-slim-buster
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry add gunicorn
COPY ./todo_app ./todo_app
COPY ./.env ./.env

ENV WEBAPP_PORT=80
EXPOSE ${WEBAPP_PORT}
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:80", "todo_app.app:app"]