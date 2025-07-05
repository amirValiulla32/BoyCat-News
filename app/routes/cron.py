# app/routes/cron.py
from fastapi import APIRouter, BackgroundTasks
from run_parser import run_parser_job

router = APIRouter()

@router.post("/cron/run-parser", status_code=202)
async def trigger_parser(background_tasks: BackgroundTasks):
    """
    Supabase cron (or any HTTP caller) hits this.
    We kick off run_parser_job() in the background and
    return immediately so the caller doesn’t time-out.
    """
    background_tasks.add_task(run_parser_job)
    return {"detail": "Parser started"}