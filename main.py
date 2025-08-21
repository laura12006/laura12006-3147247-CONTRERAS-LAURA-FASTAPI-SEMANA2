from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API with Pydantic")

# Tu primer modelo de datos
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto


# Lista temporal para guardar productos
products = []

# Endpoint GET (como antes)
@app.get("/")
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

# NUEVO: Endpoint POST con Pydantic
@app.post("/products")
def create_product(product: Product) -> dict:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return {"message": "Product created", "product": product_dict}

# Endpoint para ver todos los productos
@app.get("/products")
def get_products() -> dict:
    return {"products": products, "total": len(products)}

@app.get("/")
def hello_world():
    return {"message": "¡Mi primera API FastAPI!"}

@app.get("/info")
def info():
    return {"api": "FastAPI", "week": 1, "status": "running"}

# NUEVO: Endpoint personalizado (solo si hay tiempo)
@app.get("/greeting/")
@app.get("/greeting/{name}")
def greet_user(name: str = "Daniela"):
    return {"greeting": f"¡Hola {name}!"}

@app.get("/my-profile")
def my_profile():
    return {
        "name": "Daniela",           # Cambiar por tu nombre
        "bootcamp": "FastAPI",
        "week": 1,
        "date": "14-08-2025",
        "likes_fastapi": True              # ¿Te gustó FastAPI?
    }
from typing import List, Dict

# Lista de strings
@app.get("/fruits")
def get_fruits() -> List[str]:
    return ["apple", "banana", "orange"]

# Lista de números
@app.get("/numbers")
def get_numbers() -> List[int]:
    return [1, 2, 3, 4, 5]

# Diccionario con estructura conocida
@app.get("/user/{user_id}")
def get_user(user_id: int) -> Dict[str, str]:
    return {
        "id": str(user_id),
        "name": "Demo User",
        "email": "demo@example.com"
    }
# Endpoint con múltiples parámetros
@app.get("/calculate")
@app.get("/calculate/{num1}/{num2}")
def calculate(num1: int, num2: int) -> dict:
    result = num1 + num2
    return {"result": result, "operation": "sum"}
from typing import Optional

class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None  # campo opcional
    active: bool = True

@app.post("/users")
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}

# Agregar a tu main.py existente

# Parámetro de ruta simple
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}

# Múltiples parámetros de ruta
@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }

# Query parameters opcionales
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}


    # Agregar estos modelos después de tu modelo Product

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Product retrieved successfully"

class ProductListResponse(BaseModel):
    products: list
    total: int
    message: str = "List retrieved successfully"

# Actualizar endpoints para usar response models
@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(
        id=product_dict["id"],
        name=product_dict["name"],
        price=product_dict["price"],
        available=product_dict["available"],
        message="Product created successfully"
    )


app = FastAPI(title="My Enhanced API - Week 2")

# Modelos de datos
class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved"

# Almacenamiento temporal
products = []

# Endpoints básicos
@app.get("/")
def hello_world() -> dict:
    return {"message": "Week 2 API with Pydantic and Type Hints!"}

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(**product_dict, message="Product created")

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]

    return {"results": results, "total": len(results)}

