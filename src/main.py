from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference

app = FastAPI()

add_scalar_reference(app)

@app.get("/health")
async def health_check():
    message = "App is running"
    return {"message": message}