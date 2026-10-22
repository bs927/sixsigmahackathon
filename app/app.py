from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
from qc import compute_qc_analysis

app = FastAPI(
    title="CPR Aerospace QC API",
    description="Process Capability and SPC Analysis API for Aerospace 3D Printing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CapabilityRequest(BaseModel):
    values: List[float]
    usl: float
    lsl: float
    subgroup_size: int = 5


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "CPR Aerospace QC API is running", "docs": "/docs"}


@app.post("/api/qc/capability")
async def api_capability(req: CapabilityRequest):
    """Compute process capability and SPC chart metrics."""
    try:
        df = pd.DataFrame({"Stress_Yield_MPa": values})
        result = compute_qc_analysis(df, value_col="Stress_Yield_MPa", subgroup_size=subgroup_size, usl=usl, lsl=lsl)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/qc/upload")
async def api_upload_csv(payload: dict):
    """Helper to evaluate CSV data passed as text or list."""
    path = payload.get("path")
    usl = payload.get("usl", 950.0)
    lsl = payload.get("lsl", 850.0)
    subgroup_size = payload.get("subgroup_size", 5)
    
    if path:
        try:
            df = pd.read_csv(path, comment='#')
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise HTTPException(status_code=400, detail="CSV contains no numeric columns.")
            col = 'Stress_Yield_MPa' if 'Stress_Yield_MPa' in df.columns else numeric_cols[0]
            result = compute_qc_analysis(df, value_col=col, subgroup_size=subgroup_size, usl=usl, lsl=lsl)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read dataset: {str(e)}")
        return {"status": "success", "dataset": path, "data": result}
    else:
        values = payload.get("values", [])
        df = pd.DataFrame({"Stress_Yield_MPa": values})
        try:
            result = compute_qc_analysis(df, value_col="Stress_Yield_MPa", subgroup_size=subgroup_size, usl=usl, lsl=lsl)
            return {"status": "success", "data": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/__docs__/")
async def docs_redirect():
    """Redirect to FastAPI interactive documentation."""
    return RedirectResponse(url="/docs")
