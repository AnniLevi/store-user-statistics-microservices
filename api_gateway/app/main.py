from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return "Hello in API Gateway - FastAPI"
