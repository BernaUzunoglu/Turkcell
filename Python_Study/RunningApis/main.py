import requests

baseUrl = "http://localhost:3000/products"

def getProducts():
    response = requests.get(baseUrl)
    return response.json()

for product in getProducts():
    print(product.get("name"), "/", product.get("unitPrice"))

def getProductsByCategory(categoryId):
    response = requests.get(baseUrl+"/?categoryId="+str(categoryId))
    return response.json()

#for product in getProductsByCategory(6):
#    print(product.get("name"), "/", product.get("unitPrice"))

def createProduct(product):
    response = requests.post(baseUrl,json=product)
    return response.json()

productToCreate = {
    "suplierId": 2,
    "categoryId":6,
    "unitPrice" : 969,
    "name":"Kalem"
}

#createProduct(productToCreate)

def updateProduct(id,product):
    response = requests.put(baseUrl+"/"+str(id),json=product)
    return response.json()

def updateProductByPatch(id,product):
    response = requests.patch(baseUrl+"/"+str(id),json=product)
    return response.json()