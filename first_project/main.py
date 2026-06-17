from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")      # path
def home():
    return {"message" : "Hello World"}

@app.get("/about")      # path
def about():
    return {"message" : "Aboutus"}


products = []   # Temporary storage

class Product(BaseModel):   # model
    name: str
    price: float

@app.post("/products")
def create_product(product:Product):
    products.append(product)
    return {
        "message":"Product created successfully",
        "data": product
        }


@app.get("/products")
def get_prodects():
    return products