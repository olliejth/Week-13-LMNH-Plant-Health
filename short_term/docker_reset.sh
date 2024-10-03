source .env
docker rmi $IMAGE_SHORT_TERM_NAME_PIPELINE
docker build -t $IMAGE_SHORT_TERM_NAME_PIPELINE . --platform "linux/amd64" 