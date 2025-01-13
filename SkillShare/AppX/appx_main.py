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

# Simple GET endpoint 1
@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}

# Simple GET endpoint 2
@app.get("/status")
def get_status():
    return {"status": "API is running smoothly!"}

# Enhanced GET endpoint 3 - Search for a skill or return all rows
@app.get("/db_rows")
def get_db_rows(skill_name: str = Query(..., description="Skill name to search for, or 'all' to retrieve all rows")):
    # Using the provided credentials directly in the function
    server = "sql.bsite.net\MSSQL2016"
    database = "skillshare_"
    username = "skillshare_"
    password = "ThisisnotaPassw0rd!"

    # Connect to the remote MSSQL database using the provided credentials
    conn = connect_to_db(server, database, username, password)
    cursor = conn.cursor()

    try:
        if skill_name.lower() == "all":
            # Query to retrieve all rows
            cursor.execute("SELECT * FROM dbo.skills")
        else:
            # Query to search for a specific skill name
            cursor.execute("SELECT * FROM dbo.skills WHERE skills_name = ?", skill_name)

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]  # Extract column names
        result = [dict(zip(columns, row)) for row in rows]  # Convert rows to list of dictionaries

    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error querying the database: {str(e)}")

    # Close the database connection
    conn.close()

    # Return the rows as a response
    return {"rows": result}