from fastapi import FastAPI

app = FastAPI(title="Multi-School AI Education Platform")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Education Platform API"}
