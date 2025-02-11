import requests

baseUrl = "http://localhost:3000/lesson"


def getLessons():
    response = requests.get(baseUrl)
    return response.json()

def getLessonByCourse(courseId):
    response = requests.get(baseUrl+"/?categoryId="+str(courseId))
    return response.json()


def createLesson(lesson):
    response = requests.post(baseUrl,json=lesson)
    return response.json()


def updateLesson(id,lesson):
    response = requests.put(baseUrl+"/"+str(id),json=lesson)
    return response.json()

def updateLessonByPatch(id,lesson):
    response = requests.patch(baseUrl+"/"+str(id),json=lesson)
    return response.json()

def deleteLesson(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()