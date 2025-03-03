import requests

baseUrl = "http://localhost:3000/category"

def getCategory():
    response = requests.get(baseUrl)
    return response.json()

def getCategoryById(id):
    response = requests.get(baseUrl+"/?id="+str(id))
    return response.json()


def getCategoryName(name):
    response = requests.get(baseUrl+"/?name="+str(name))
    if response.json():
        return True
    else:
        return False

def createCategory(category):
    isExists = getCategoryName(category.get("name"))
    if not isExists:
        response = requests.post(baseUrl, json=category)
        return response.json()
    else:
        print("Bu category mevcuttur!")


def updateCategory(id,category):
    response = requests.put(baseUrl+"/"+str(id),json=category)
    return response.json()

def updateCategoryByPatch(id,category):
    response = requests.patch(baseUrl+"/"+str(id),json=category)
    return response.json()

def deleteCategoty(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()
