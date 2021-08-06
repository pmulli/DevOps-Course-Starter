FROM python:3.9.2-slim-buster
RUN apt-get update
RUN apt-get -y install gunicorn
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
COPY ./todo_app ./todo_app
COPY ./.env ./.env

ENV WEBAPP_PORT=80
EXPOSE ${WEBAPP_PORT}
ENV PATH="/todo_app:${PATH}"
RUN poetry install --no-root --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:80", "todo_app.app:app"]