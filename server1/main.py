from fastapi import FastAPI, HTTPException
import uvicorn
import json
from pydantic import BaseModel
from pathlib import Path
app = FastAPI()

DB_PATH = Path('db/shopping_list.json')
DB_DEPLOYMENT = '/app/db/shopping_list.json'
class Item(BaseModel):
    id : int
    name : str
    quantity : int


def create_json_file_if_not_exist(file_name:Path):
    if not file_name.exists():
        with open(file_name, 'x') as file:
            json.dump([], file)


def load_json_file(file_name:str):
    create_json_file_if_not_exist(file_name)
    with open(file_name, 'r') as file:
        return json.load(file)


def save_data(file_name:str, data):
    with open(file_name, 'w') as file:
        json.dump(data, file,indent=2)


@app.get('/items')
def get_all_items():
    return load_json_file(DB_PATH)

@app.post('/items')
def add_item(name:str, quantity:int):
    items = load_json_file(DB_PATH)
    item_id = len(items) + 1
    item = Item(id=item_id, name=name, quantity=quantity)
    items.append(item.model_dump())
    save_data(DB_PATH, items)
    return {'message':'good'}


if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)
