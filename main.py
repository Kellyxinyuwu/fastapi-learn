# import fastapi and use it to create a new app
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# extend the BaseModel to create a new class Item. Becuase the data is a todolist, so we need to define the text and is_done.
class Item(BaseModel):
    text: str = None
    is_done: bool = False


items = []

# define an app
@app.get("/") # app decorator and it defines a path for the http get method. path is / which is our root directory.
# when someone visits the @app.get(), this function root will be called.
def root():
    return {"Hello":"World"}


# a new endpoint for the app, called create item
# user can access this end point by sending a http post request to the item's path.
# accept the item as a input, query parameter.
@app.post("/items")
def create_item(item:Item):
    # once receive the item, add it to the items list.
    items.append(item)
    return items # or return items list by 'return items', or single item by 'return item'

@app.get("/items",response_model=List[Item])
def list_items(limit:int = 10):
    return items[0:limit]

@app.get("/items/{item_id}",response_model=Item) # like /items/1, /items/2, we can use it to query the item list.
# because what id we put would be passed as a parameter to the function. and use it as the index of the items list.
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")
# because if you do get, the server will be reset, so items will be empty, so make sure you do create_item first before get.













