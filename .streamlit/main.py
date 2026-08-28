from fastapi import FastAPI

app = FastAPI()

# Define a GET endpoint
@app.get("/api/greet")
def read_greet():
    return {"message": "Hello, welcome to my API!"}
