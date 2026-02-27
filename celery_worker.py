from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst
from tasks import analyze_financial_document
from config import USE_MOCK
from database import SessionLocal, AnalysisJob
import json
import os

celery_app = Celery(
    "financial_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


def run_crew(query: str, file_path: str="data/sample.pdf"):
    """
    This is your original logic moved safely into the worker.
    """
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    return result


@celery_app.task
def run_analysis_task(job_id: str, query: str, file_path: str):
    db = SessionLocal()
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

    try:
        job.status = "processing"
        db.commit()

        if USE_MOCK:
            result = {
                "summary": "Mock analysis result.",
                "key_metrics": {
                    "Revenue": "$10M",
                    "Net Income": "$2M"
                },
                "risk_factors": ["Market risk"],
                "investment_insight": "Moderate growth outlook.",
                "confidence_level": "medium"
            }
        else:
            output = run_crew(query, file_path)

            try:
                result = json.loads(output)
            except Exception:
                result = {"raw_output": str(output)}

        job.status = "completed"
        job.result = json.dumps(result)
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.result = str(e)
        db.commit()

    finally:
        db.close()

        # Optional cleanup
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass