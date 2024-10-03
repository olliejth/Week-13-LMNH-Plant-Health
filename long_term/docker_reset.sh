source .env
docker rmi $IMAGE_LONG_TERM_NAME_PIPELINE
docker build -t $IMAGE_LONG_TERM_NAME_PIPELINE . --platform "linux/amd64"