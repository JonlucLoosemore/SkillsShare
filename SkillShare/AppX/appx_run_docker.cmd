@echo off
REM Build the Docker image
echo Building the Docker image...
docker build -t appx-image .

REM Check if the container is already running
echo Checking for existing container...
docker ps -q --filter "name=appx-container" >nul 2>&1
if %errorlevel% equ 0 (
    echo Stopping existing container...
    docker stop appx-container
    echo Removing existing container...
    docker rm appx-container
)

REM Run the Docker container
echo Running the Docker container...
docker run -d -p 8000:8000 --name appx-container appx-image

echo Docker commands executed successfully!
pause