echo excute azure webhook to trigger restart with latest docker image
echo $WEBHOOK_URL
env
curl -dH -X POST "$WEBHOOK_URL"