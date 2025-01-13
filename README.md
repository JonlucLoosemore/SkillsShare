# SkillsShare

docker build -t skillshare-app . 

docker run -d -p 8000:8000 --name skillshare-app-container skillshare-app

http://localhost:8000/status