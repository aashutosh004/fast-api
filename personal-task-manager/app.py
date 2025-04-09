from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks_db: List[dict] = []

class Task_Create(BaseModel):
    title: str
    description: str
    owner: str

class Task_Response(Task_Create):
    id: int
    is_completed: bool

@app.get("/")
def home():
    return {"message": "Welcome to Task Manager"}

@app.post("/addtask", response_model=Task_Response)
def add_task(task: Task_Create):
    task_dict = task.model_dump()
    task_dict['id'] = len(tasks_db) + 1
    task_dict['is_completed'] = False
    tasks_db.append(task_dict)
    return task_dict

@app.get("/gettasks", response_model=List[Task_Response])
def get_all_tasks():
    return tasks_db

@app.get("/gettask/{owner}", response_model=List[Task_Response])
def get_task_by_owner(owner: str):
    owner_tasks = [task for task in tasks_db if task['owner'] == owner]
    if not owner_tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this owner")
    return owner_tasks

@app.put("/tasks/{task_id}", response_model=Task_Response)
def update_task(task_id: int, updated_task: Task_Create):
    for index, task in enumerate(tasks_db):
        if task['id'] == task_id:
            task_dict = updated_task.model_dump()
            task_dict['id'] = task_id
            task_dict['is_completed'] = task['is_completed']
            tasks_db[index] = task_dict
            return task_dict
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.put("/completetask/{task_id}", response_model=Task_Response)
def complete_task(task_id: int):
    for task in tasks_db:
        if task['id'] == task_id:
            task['is_completed'] = True
            return task
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/tasks/{task_id}", response_model=Task_Response)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task['id'] == task_id:
            deleted_task = tasks_db.pop(index)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task Not Found")