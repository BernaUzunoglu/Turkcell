import requests

baseUrl = "http://localhost:3000/category"

def getCategory():
    response = requests.get(baseUrl)
    return response.json()


def createCategory(category):
    response = requests.post(baseUrl,json=category)
    return response.json()


def updateCategory(id,category):
    response = requests.put(baseUrl+"/"+str(id),json=category)
    return response.json()

def updateCategoryByPatch(id,category):
    response = requests.patch(baseUrl+"/"+str(id),json=category)
    return response.json()

def deleteCategoty(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()

