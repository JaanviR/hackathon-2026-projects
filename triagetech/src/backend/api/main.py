from fastapi import FastAPI
from api.routes import triage, translate, clinics

app = FastAPI(title="TriageTech API")

app.include_router(triage.router, prefix="/triage", tags=["Triage"])
app.include_router(translate.router, prefix="/translate", tags=["Translation"])
app.include_router(clinics.router, prefix="/clinics", tags=["Clinics"])

@app.get("/")
async def root():
    return {"message": "Welcome to TriageTech API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
