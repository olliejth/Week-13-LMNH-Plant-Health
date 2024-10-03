source .env
bash docker_auth_client.sh
bash docker_reset.sh
bash docker_tag_ecr.sh
bash docker_push.sh