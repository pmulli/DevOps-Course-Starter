echo excute azure webhook to trigger restart with latest docker image
echo $WEBHOOK_URL
env
curl -dH -X POST "https://\$pdm-todo:9wcmycL3FDAXCHX6YQKLPBWJZnBAhaEomNSBqlRv7nimnwSDwiMrg1KaRnCw@pdm-todo.scm.azurewebsites.net/docker/hook"