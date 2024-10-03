from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os

# Import DAL (Data Access Layer)
from src.dal import ToDoDAL, ListSummary, ToDoList

MONGODB_URI = os.getenv("MONGODB_URI", "your_default_mongodb_uri")
COLLECTION_NAME = "todo_lists"

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.get_default_database()
    app.todo_dal = ToDoDAL(db[COLLECTION_NAME])
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

class NewList(BaseModel):
    name: str

class NewListResponse(BaseModel):
    id: str
    name: str

@app.get("/api/lists", response_model=list[ListSummary])
async def get_all_lists():
    return [list_summary async for list_summary in app.todo_dal.list_todo_lists()]

@app.post("/api/lists", response_model=NewListResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList):
    response_id = await app.todo_dal.create_todo_list(new_list.name)
    return NewListResponse(id=response_id, name=new_list.name)

@app.get("/api/lists/{list_id}", response_model=ToDoList)
async def get_todo_list(list_id: str):
    todo_list = await app.todo_dal.get_todo_list(list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="List not found")
    return todo_list

@app.delete("/api/lists/{list_id}", response_model=bool)
async def delete_todo_list(list_id: str):
    success = await app.todo_dal.delete_todo_list(list_id)
    if not success:
        raise HTTPException(status_code=404, detail="List not found")
    return success

@app.post("/api/lists/{list_id}/items", response_model=ToDoList, status_code=status.HTTP_201_CREATED)
async def create_item(list_id: str, label: str):
    return await app.todo_dal.create_item(list_id, label)

@app.patch("/api/lists/{list_id}/items/{item_id}", response_model=ToDoList)
async def update_item(list_id: str, item_id: str, checked: bool):
    return await app.todo_dal.update_item(list_id, item_id, checked)

@app.delete("/api/lists/{list_id}/items/{item_id}", response_model=ToDoList)
async def delete_item(list_id: str, item_id: str):
    return await app.todo_dal.delete_item(list_id, item_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001, reload=True)
