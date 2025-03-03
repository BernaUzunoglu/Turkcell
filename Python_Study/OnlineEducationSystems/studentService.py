import requests

baseUrl = "http://localhost:3000/student"


def getStudent():
    response = requests.get(baseUrl)
    return response.json()


def createStudent(student):
    response = requests.post(baseUrl,json=student)
    return response.json()


def updateStudent(id,student):
    response = requests.put(baseUrl+"/"+str(id),json=student)
    return response.json()

def updateStudentByPatch(id,student):
    response = requests.patch(baseUrl+"/"+str(id),json=student)
    return response.json()

def deleteStudent(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()