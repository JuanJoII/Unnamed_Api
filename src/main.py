from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference
from src.api.v1.users import router as user_router

app = FastAPI()

add_scalar_reference(app)
app.include_router(user_router)


@app.get("/health")
async def health_check():
    message = "App is running"
    return {"message": message}
