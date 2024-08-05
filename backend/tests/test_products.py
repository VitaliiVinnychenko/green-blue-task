from app.utils.enums.products import Category


def test_products_crud_api(client):
    # test POST /api/v1/products
    new_product = {
        "name": "MacBook",
        "price": 1000.0,
        "description": "best laptop",
        "category": Category.LAPTOP,
    }
    response = client.post("/api/v1/products", json=[new_product])
    assert response.status_code == 201
    assert len(response.json()) == 1
    created_product_obj = response.json()[0]
    product_id = created_product_obj["id"]
    for key in new_product.keys():
        assert created_product_obj[key] == new_product[key]

    # test POST /api/v1/products
    invalid_product = {
        "name": "MacBook",
        "price": 1000.0,
        "description": "best laptop",
        "category": "foo",  # issue is here
    }
    response = client.post("/api/v1/products", json=[invalid_product])
    assert response.status_code == 422

    # test GET /api/v1/products/{product_id}
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == created_product_obj

    # test GET /api/v1/products (is new product returned products list)
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert created_product_obj in response.json()

    # test PUT /api/v1/products/{product_id}
    update_product_req_body = {
        "name": "MacBook Pro",
        "price": 5000.0,
        "description": "best laptop",
        "category": None,
    }
    response = client.put(f"/api/v1/products/{product_id}", json=update_product_req_body)
    assert response.status_code == 200
    updated_product_obj = response.json()
    for key in update_product_req_body.keys():
        assert update_product_req_body[key] == updated_product_obj[key]

    # test DELETE /api/v1/products/{product_id}
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204

    # test GET /api/v1/products/{product_id} (not found)
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 404

    # test GET /api/v1/products (new product is not in returned products list)
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert updated_product_obj not in response.json()
