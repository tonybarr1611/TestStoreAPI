#!/usr/bin/env python3
import sys
import requests
from jsonschema import validate, ValidationError

BASE_URL = "https://fakestoreapi.com"

# Esquema para los productos (/products y /products/:id)
product_schema = {
    "type": "object",
    "required": ["id", "title", "price", "description", "category", "image", "rating"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string"},
        "rating": {
            "type": "object",
            "required": ["rate", "count"],
            "properties": {
                "rate": {"type": "number"},
                "count": {"type": "integer"}
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}

# Esquema para la lista de productos (/products)
products_list_schema = {
    "type": "array",
    "items": product_schema
}

# Esquema para los carritos (/carts)
cart_schema = {
    "type": "object",
    "required": ["id", "userId", "date", "products"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "date": {"type": "string"},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["productId", "quantity"],
                "properties": {
                    "productId": {"type": "integer"},
                    "quantity": {"type": "integer"}
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": True
}

carts_list_schema = {
    "type": "array",
    "items": cart_schema
}


def fetch_and_validate(path: str, schema: dict):
    url = BASE_URL + path
    print(f"> Comprobando {url} ...", end=" ")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        print("❌ ESTRUCTURA INCORRECTA")
        print(f"  Detalle: {e.message} en {'/'.join(str(x) for x in e.path)}")
        sys.exit(1)
    else:
        print("✔ OK")


def main():
    # 1) /products → lista
    fetch_and_validate("/products", products_list_schema)

    # 2) /products/:id → un producto (por ejemplo el 1)
    fetch_and_validate("/products/1", product_schema)

    # 3) /carts → lista de carritos
    fetch_and_validate("/carts", carts_list_schema)

    print("\nTodas las estructuras JSON son correctas.")


if __name__ == "__main__":
    main()
