from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Auto-generate tables if they don't exist (Useful for testing).
# Note: In production you would use Alembic or similar.
models.Base.metadata.create_all(bind=engine)

from routers import auth, employees, assets, assignments, dashboard, admins

app = FastAPI(
    title="AssetTrack Pro API",
    description="Professional Asset Management System API tailored for precision and atomic-scale design. Covers Admin, Employees, Assignments, Assets, Status, History, and Reporting endpoints.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply highly permissive CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"System Error: {str(exc)}"},
    )

# Registering Routers mapped exactly to 'api_design.txt' feature lists
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(dashboard.dashboard_router)
app.include_router(dashboard.reports_router)

# Superadmin Hub
app.include_router(admins.router)

@app.get("/", tags=["Health Check"])
def health_check():
    """
    Root Endpoint - Health Check
    
    Verifies the operational status of the AssetTrack Pro API.
    """
    return {"status": "ok", "message": "Welcome to AssetTrack Pro API"}
