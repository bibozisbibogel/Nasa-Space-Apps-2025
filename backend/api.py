"""FastAPI backend for Launch Go/No-Go Advisor."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from decide import make_decision
from sites import LAUNCH_SITES

app = FastAPI(
    title="Launch Go/No-Go Advisor",
    description="AI-powered launch readiness assessment system",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LaunchRequest(BaseModel):
    """Request model for launch decision."""
    site_code: str
    launch_time: str  # ISO format datetime string


class LaunchResponse(BaseModel):
    """Response model for launch decision."""
    verdict: str
    risk_score: int
    why: str
    rule_citations: list[str]
    data: Optional[dict] = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "operational",
        "service": "Launch Go/No-Go Advisor",
        "version": "1.0.0"
    }


@app.get("/sites")
async def list_sites():
    """List available launch sites."""
    return {
        "sites": [
            {
                "code": code,
                "name": site["name"],
                "lat": site["lat"],
                "lon": site["lon"]
            }
            for code, site in LAUNCH_SITES.items()
        ]
    }


@app.post("/api/decide", response_model=LaunchResponse)
async def decide_launch(request: LaunchRequest):
    """
    Main endpoint: Determine GO/NO-GO for a launch.

    Example request:
    {
        "site_code": "KSC",
        "launch_time": "2025-10-05T20:00:00Z"
    }

    Returns decision with verdict, risk score, explanation, and rule citations.
    """
    try:
        # Parse launch time
        launch_time = datetime.fromisoformat(request.launch_time.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid launch_time format. Use ISO format: YYYY-MM-DDTHH:MM:SSZ"
        )

    # Validate site code
    if request.site_code not in LAUNCH_SITES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid site_code. Available sites: {', '.join(LAUNCH_SITES.keys())}"
        )

    # Make decision
    result = await make_decision(request.site_code, launch_time)

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
