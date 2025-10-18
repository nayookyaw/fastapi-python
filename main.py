from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "message": "Hello, FastAPI"}

@app.get("/item/{item_id}/{query}")
def read_item(item_id: int, query: str | None):
    return { "message": "item has been retrieved", 
            "data" : {
                "item_id": item_id, "query": query
            }
        }