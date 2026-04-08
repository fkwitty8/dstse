import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI(title="DSTSE UI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DECISION_ENGINE_URL = os.getenv("DECISION_ENGINE_URL", "http://localhost:5002")

# Point to static folder inside src
static_path = Path("src/static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def index():
    """Serve the main HTML page"""
    html_path = Path("src/static/index.html")
    if html_path.exists():
        return FileResponse(html_path)
    return {"error": "index.html not found"}

@app.get("/api/status")
async def get_status():
    """Get decision from decision engine"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{DECISION_ENGINE_URL}/health")
            return {
                "status": "connected",
                "decision_engine": response.json()
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Cannot connect to decision engine: {str(e)}"
        }

@app.post("/api/predict")
async def predict_lecture(request: Request):
    """Forward prediction request to decision engine"""
    try:
        data = await request.json()
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{DECISION_ENGINE_URL}/predict_decision",
                json=data
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Decision engine error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5003))
    uvicorn.run(app, host="0.0.0.0", port=port)