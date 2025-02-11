import requests

baseUrl = "http://localhost:3000/course"



def getCourse():
    response = requests.get(baseUrl)
    return response.json()

def getCourseByCategory(categoryId):
    response = requests.get(baseUrl+"/?categoryId="+str(categoryId))
    return response.json()


def createCourse(course):
    response = requests.post(baseUrl,json=course)
    return response.json()


def updateCourse(id,course):
    response = requests.put(baseUrl+"/"+str(id),json=course)
    return response.json()

def updateCourseByPatch(id,course):
    response = requests.patch(baseUrl+"/"+str(id),json=course)
    return response.json()

def deleteCourse(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()