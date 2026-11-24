from fastapi import FastAPI

app = FastAPI(
    title="Business Automation Labs CRM API",
    description="Multi-niche, multi-country lead-generation CRM API",
    version="0.1.0",
)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Business Automation Labs CRM API"}


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)