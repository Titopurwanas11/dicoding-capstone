from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.api.hr_endpoints import router as hr_router
from app.api.jobs_endpoints import router as jobs_router

app = FastAPI(title="CV Summarizer & Job Matching System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(hr_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok"}
