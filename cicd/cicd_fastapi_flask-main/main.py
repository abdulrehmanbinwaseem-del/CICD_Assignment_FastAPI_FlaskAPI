from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
tasks = []


class Task(BaseModel):
    title: str
    done: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    tasks.append(task.dict())
    return task
