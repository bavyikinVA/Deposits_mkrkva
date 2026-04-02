from fastapi import FastAPI

from app.api import deposits_router, health_router

app = FastAPI(
    title="Deposits API",
    description="API для подбора вкладов и расчета итоговой доходности",
    version="1.0.0",)

@app.get("/")
async def root():
    return {
        "message": "Deposits API is running",
        "docs": "/docs",
        "health": "/health",
        "catalog": "/api/deposits",
        "search": "/api/deposits/search",
        "calculate": "/api/deposits/calculate",
    }

app.include_router(health_router)
app.include_router(deposits_router)