# SkillsShare

docker build -t skillshare-app . 

docker run -d -p 8000:8000 --name skillshare-app-container skillshare-app

http://localhost:8000/status

/db_rows?skill_name="NAME" 
(if skill name = all, then all will be returned.)
skill names include: 

Web Development
Data Science 
Spanish
Photography
Graphic Design
Project Management
Creative Writing
Digital Marketing