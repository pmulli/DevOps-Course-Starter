#! /usr/bin/env bash
set -x
echo excute azure webhook to trigger restart with latest docker image

curl -dH --fail -X POST "$(terraform output -raw webhook_url)"
