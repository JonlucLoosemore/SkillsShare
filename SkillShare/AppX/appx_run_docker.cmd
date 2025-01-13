@echo off
REM Build the Docker image
docker build -t appx_main.py .

REM Run the Docker container
docker run -d -p 8000:8000 --name appx-container appx_main.py

echo Docker commands executed successfully!
pause