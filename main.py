import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from celery_worker import run_analysis_task
from database import init_db, SessionLocal, AnalysisJob

app = FastAPI(title="Financial Document Analyzer with Queue")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    db = SessionLocal()

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    job = AnalysisJob(
        filename=file.filename,
        query=query,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    run_analysis_task.delay(job.id, query, file_path)

    db.close()

    return {
        "status": "submitted",
        "job_id": job.id
    }


@app.get("/result/{job_id}")
def get_result(job_id: str):
    db = SessionLocal()
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    db.close()

    if not job:
        return {"status": "error", "message": "Job not found"}

    return {
        "status": job.status,
        "result": job.result
    }

@app.get("/")
def root():
    return {"message": "Financial Document Analyzer with Async Queue is running"}