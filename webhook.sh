#! /usr/bin/env bash
set -x
echo excute azure webhook to trigger restart with latest docker image

curl -dH -X POST "https://\$$WEBHOOK_USERNAME:$WEBHOOK_PASSWORD@pdm-todo.scm.azurewebsites.net/docker/hook"
