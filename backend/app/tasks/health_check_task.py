import time

from app.tasks.celery_app import celery_app


@celery_app.task(name="health_check_task")
def health_check_task(name: str) -> str:
    time.sleep(2)  # simulate work
    return f"Hello {name}, your Celery task ran successfully!"