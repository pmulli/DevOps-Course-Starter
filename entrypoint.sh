#!/bin/sh
poetry run gunicorn -b 0.0.0.0:80 "todo_app.app:create_app()"