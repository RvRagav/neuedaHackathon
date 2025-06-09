from fastapi import FastAPI
from .routers import carbon_calculator
app = FastAPI()

app.include_router(carbon_calculator.router, prefix="/api", tags=["carbon_calculator"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
