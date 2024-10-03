from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from typing import List
from uuid import uuid4

# Define data models for the to-do application
class ListSummary(BaseModel):
    id: str
    name: str
    item_count: int

    @staticmethod
    def from_doc(doc) -> "ListSummary":
        return ListSummary(
            id=str(doc["_id"]),
            name=doc["name"],
            item_count=doc["item_count"]
        )

class ToDoListItem(BaseModel):
    id: str
    label: str
    checked: bool

    @staticmethod
    def from_doc(item) -> "ToDoListItem":
        return ToDoListItem(
            id=str(item["_id"]),
            label=item["label"],
            checked=item["checked"]
        )

class ToDoList(BaseModel):
    id: str
    name: str
    items: List[ToDoListItem]

    @staticmethod
    def from_doc(doc) -> "ToDoList":
        return ToDoList(
            id=str(doc["_id"]),
            name=doc["name"],
            items=[ToDoListItem.from_doc(item) for item in doc["items"]]
        )

class ToDoDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def list_todo_lists(self):
        cursor = self.collection.find({}, projection={"name": 1, "item_count": {"$size": "$items"}})
        async for doc in cursor:
            yield ListSummary.from_doc(doc)

    async def create_todo_list(self, name: str) -> str:
        result = await self.collection.insert_one({"name": name, "items": []})
        return str(result.inserted_id)

    async def get_todo_list(self, list_id: str) -> ToDoList:
        doc = await self.collection.find_one({"_id": ObjectId(list_id)})
        return ToDoList.from_doc(doc)

    async def delete_todo_list(self, list_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(list_id)})
        return result.deleted_count == 1

    async def create_item(self, list_id: str, label: str) -> ToDoList:
        await self.collection.update_one(
            {"_id": ObjectId(list_id)},
            {"$push": {"items": {"_id": uuid4(), "label": label, "checked": False}}}
        )
        return await self.get_todo_list(list_id)

    async def update_item(self, list_id: str, item_id: str, checked: bool) -> ToDoList:
        await self.collection.update_one(
            {"_id": ObjectId(list_id), "items._id": ObjectId(item_id)},
            {"$set": {"items.$.checked": checked}}
        )
        return await self.get_todo_list(list_id)

    async def delete_item(self, list_id: str, item_id: str) -> ToDoList:
        await self.collection.update_one(
            {"_id": ObjectId(list_id)},
            {"$pull": {"items": {"_id": ObjectId(item_id)}}}
        )
        return await self.get_todo_list(list_id)
