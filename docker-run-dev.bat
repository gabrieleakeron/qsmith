@echo off
REM Stop and relaunch Docker container using docker-compose-dev.yml

echo Stopping and removing the current container...
docker compose -f docker-compose.yml down

echo Rebuilding and relaunching the container...
docker compose -f docker-compose.yml up --build -d

echo Done!
pause