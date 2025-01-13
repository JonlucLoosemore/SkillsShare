from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI()

# Simple GET endpoint 1
@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}

# Simple GET endpoint 2
@app.get("/status")
def get_status():
    return {"status": "API is running smoothly!"}
