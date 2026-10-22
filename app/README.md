# CPR Aerospace QC — App Documentation (`app/README.md`)

This directory (`app/`) contains the complete FastAPI backend, static React frontend assets, core Six Sigma statistical engine (`qc.py`), and the four-script deployment contract.

---

## Directory Structure
```
app/
├── main.py             # FastAPI application and REST endpoints
├── qc.py               # Core statistical process control and capability engine
├── requirements.txt    # Python dependencies (numpy, pandas, scipy, fastapi, uvicorn)
├── testme.sh           # One-command startup script for local testing
├── manifestme.py       # Posit Connect manifest generation script
└── deployme.sh         # Posit Connect deployment script
```

---

## The Four-script Contract

1. **`testme.sh`**: Starts the FastAPI development server locally on `http://127.0.0.1:8000`.
   - Run: `bash app/testme.sh`
2. **`manifestme.py`**: Generates `manifest.json` for Posit Connect bundle deployment.
   - Run: `python app/manifestme.py`
3. **`deployme.sh`**: Publishes the application package directly to the course Posit Connect server using `rsconnect-python`.
   - Run: `bash app/deployme.sh`
4. **`README.md`**: This developer and user guide for the `app/` layer.

---

## Architecture & Integration
- **Separation of Concerns:** Statistical calculations reside entirely in `app/qc.py`. The FastAPI router in `app/main.py` handles HTTP requests, file uploads, and JSON serialization without performing any raw statistical arithmetic.
- **Frontend Integration:** Served statically from `app/frontend/` (copied from `demos/fastapi/`), communicating asynchronously with `/api/analyze`.
