from fastapi import FastAPI, HTTPException, Query
import pyodbc

# Initialize the FastAPI app
app = FastAPI()

# Function to connect to a remote MSSQL database
def connect_to_db(server: str, database: str, username: str, password: str):
    try:
        # Connection string for MSSQL
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
    # Connect to the remote MSSQL database using the provided credentials
    conn = connect_to_db(server, database, username, password)
    cursor = conn.cursor()

    try:
        # Query to fetch the skill_id for the given skill_name
        cursor.execute("SELECT skills_id FROM dbo.skills WHERE skills_name = ?", skill_name)
        
        # Fetch the result
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        # Return the skill_id
        return result[0]

    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error querying the database: {str(e)}")

    finally:
        # Close the database connection
        conn.close()

# Endpoint to get skill_id from skill_name
@app.get("/get_skill_id/{skill_name}")
def get_skill_id_from_name(skill_name: str, server: str = Query("sql.bsite.net\\MSSQL2016", description="Database server"),
                           database: str = Query("skillshare_", description="Database name"),
                           username: str = Query("skillshare_", description="Username"),
                           password: str = Query("ThisisnotaPassw0rd!", description="Password")):
    try:
        skill_id = get_skill_id(skill_name, server, database, username, password)
        return {"skill_name": skill_name, "skill_id": skill_id}
    except HTTPException as e:
        raise e

# Endpoint to delete skill by skill_id
@app.delete("/delete_skill/{skill_id}")
def delete_skill_by_id(skill_id: int, server: str = Query("sql.bsite.net\\MSSQL2016", description="Database server"),
                       database: str = Query("skillshare_", description="Database name"),
                       username: str = Query("skillshare_", description="Username"),
                       password: str = Query("ThisisnotaPassw0rd!", description="Password")):
    # Connect to the remote MSSQL database using the provided credentials
    conn = connect_to_db(server, database, username, password)
    cursor = conn.cursor()

    try:
        # Query to delete the skill by ID
        cursor.execute("DELETE FROM dbo.skills WHERE skills_id = ?", skill_id)
        
        # Commit the transaction
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        return {"message": f"Skill with ID {skill_id} successfully deleted"}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error deleting the skill: {str(e)}")
    finally:
        # Close the database connection
        conn.close()