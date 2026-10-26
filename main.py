from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)


items = []


@app.post("/items", status_code=201)
def create_item(item: Item):
    new_item = {"id": len(items) + 1, **item.model_dump()}

    items.append(new_item)
    return new_item


@app.get("/items")
def get_items():
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item_id == item["id"]:
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item_id == item["id"]:
            items.pop(index)
            return

    raise HTTPException(status_code=404, detail="Item not found")
