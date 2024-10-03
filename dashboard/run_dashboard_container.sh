source .env
docker run -p 8501:8501 --env-file .env $DASHBOARD_CONTAINER