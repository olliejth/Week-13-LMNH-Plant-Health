source .env
docker rmi $IMAGE_NAME
docker build -t $IMAGE_NAME .