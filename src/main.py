from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference
from src.api.v1.users import router as user_router
from src.api.v1.auth import router as auth_router

app = FastAPI()

add_scalar_reference(app)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check():
    message = "App is running"
    return {"message": message}
