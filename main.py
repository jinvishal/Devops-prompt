from fastapi import FastAPI
from core.api import users, auth, schools, roles

app = FastAPI(title="Multi-School AI Education Platform")

# Include the API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(schools.router)
app.include_router(roles.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Education Platform API. Visit /docs for documentation."}
