from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pyodbc

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for specific origins (adjust this as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (for local dev, you can specify "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Create an APIRouter instance
router = APIRouter()

# Function to connect to a remote MSSQL database
def connect_to_db(server: str, database: str, username: str, password: str):
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Function to get skill_id from skill_name
def get_skill_id(skill_name: str, server: str, database: str, username: str, password: str) -> int:
    conn = connect_to_db(server, database, username, password)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT skills_id FROM dbo.skills WHERE skills_name = ?", skill_name)
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the database: {str(e)}")
    finally:
        conn.close()

# Endpoint to get skill_id from skill_name
@router.get("/get_skill_id/{skill_name}")
def get_skill_id_from_name(
    skill_name: str,
    server: str = Query("sql.bsite.net\\MSSQL2016", description="Database server"),
    database: str = Query("skillshare_", description="Database name"),
    username: str = Query("skillshare_", description="Username"),
    password: str = Query("ThisisnotaPassw0rd!", description="Password")
):
    try:
        skill_id = get_skill_id(skill_name, server, database, username, password)
        return {"skill_name": skill_name, "skill_id": skill_id}
    except HTTPException as e:
        raise e

# Endpoint to delete skill by skill_id
@router.delete("/delete_skill/{skill_id}")
def delete_skill_by_id(
    skill_id: int,
    server: str = Query("sql.bsite.net\\MSSQL2016", description="Database server"),
    database: str = Query("skillshare_", description="Database name"),
    username: str = Query("skillshare_", description="Username"),
    password: str = Query("ThisisnotaPassw0rd!", description="Password")
):
    conn = connect_to_db(server, database, username, password)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.skills WHERE skills_id = ?", skill_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        return {"message": f"Skill with ID {skill_id} successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting the skill: {str(e)}")
    finally:
        conn.close()

# Status endpoint to check API status
@app.get("/status")
def get_status():
    return {"status": "API is running smoothly!"}

# Register router with FastAPI app
app.include_router(router)
