#! /usr/bin/env bash
set -x
echo excute azure webhook to trigger restart with latest docker image

curl -dH -X POST $WEBHOOK_URL
