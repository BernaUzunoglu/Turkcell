
##  API Kullanımı
### 1 **/products - GET**
Tüm ürünleri listelemek için kullanılır.

**Request:**
```http
GET /products
```

**Response:**
```json
[
    {"product_id": 1, "name": "Chai", "category": "Beverages"},
    {"product_id": 2, "name": "Chang", "category": "Beverages"}
]
```

### 2 **/predict - POST**
Belirli bir ürün için satış tahmini yapar.

**Request:**
```http
POST /predict
```
**Body:**
```json
{
    "product_id": 1,
    "date": "2025-04-01",
    "customer_id": 123
}
```

**Response:**
```json
{"predicted_sales": 150}
```

---
