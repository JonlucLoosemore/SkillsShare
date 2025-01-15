@echo off
REM Stop and remove the webx-container if it exists
docker stop webx-container
docker rm webx-container

REM Build the Docker image
docker build -t webx-app .

REM Run the Docker container
docker run -d -p 3000:80 --name webx-container webx-app

echo Docker commands executed successfully!
pause