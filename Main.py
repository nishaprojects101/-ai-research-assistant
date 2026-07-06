# main.py
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from agents import run_research_pipeline, save_report

# ══════════════════════════════════════════════════════
# APP SETUP
# ══════════════════════════════════════════════════════

app = FastAPI(
    title="AI Research Assistant API",
    description="Multi-agent AI system that researches any topic and generates a professional report.",
    version="1.0.0"
)

# ══════════════════════════════════════════════════════
# CORS MIDDLEWARE
# This allows your frontend (HTML file) to talk to this backend
# Without this, browsers block cross-origin requests
# ══════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins (fine for development)
    allow_methods=["*"],      # allow all HTTP methods
    allow_headers=["*"],      # allow all headers
)

# ══════════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ══════════════════════════════════════════════════════

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic:     str
    summary:   str
    critique:  str
    report:    str
    filename:  str
    timestamp: str

# ══════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════

@app.get("/health")
def health_check():
    """Check if the API is running."""
    return {
        "status":  "healthy",
        "version": "1.0.0",
        "agents":  4
    }


@app.post("/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    """
    Main endpoint — runs full 4-agent pipeline.
    Takes a topic and returns a complete research report.
    """
    # Validate input
    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Topic cannot be empty"
        )

    if len(request.topic) > 200:
        raise HTTPException(
            status_code=400,
            detail="Topic too long — keep it under 200 characters"
        )

    try:
        print(f"\n📥 New research request: {request.topic}")

        # Run the 4-agent pipeline
        result = run_research_pipeline(request.topic)

        # Save report to file
        filename = save_report(result["topic"], result["report"])

        # Return structured response
        return ResearchResponse(
            topic=     result["topic"],
            summary=   result["summary"],
            critique=  result["critique"],
            report=    result["report"],
            filename=  filename,
            timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports")
def list_reports():
    """List all saved research reports."""
    try:
        # Find all .txt report files in current directory
        files = [f for f in os.listdir(".") if f.endswith("_report.txt")]
        files.sort(reverse=True)  # newest first

        return {
            "count":   len(files),
            "reports": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/{filename}")
def get_report(filename: str):
    """Get contents of a specific saved report."""
    try:
        # Security check — prevent directory traversal attacks
        if "/" in filename or "\\" in filename or ".." in filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid filename"
            )

        if not filename.endswith("_report.txt"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )

        if not os.path.exists(filename):
            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "filename": filename,
            "content":  content
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))