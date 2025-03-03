import requests

baseUrl = "http://localhost:3000/enrollment"


def getEnrollment():
    response = requests.get(baseUrl)
    return response.json()

def getEnrollmentByStudent(studentId):
    response = requests.get(baseUrl+"/?student_id="+str(studentId))
    return response.json()

def getEnrollmentByCourse(courseId):
    response = requests.get(baseUrl+"/?course_id="+str(courseId))
    return response.json()

def createEnrollment(enrollment):
    response = requests.post(baseUrl,json=enrollment)
    return response.json()


def updateEnrollment(id,enrollment):
    response = requests.put(baseUrl+"/"+str(id),json=enrollment)
    return response.json()

def updateEnrollmentByPatch(id,enrollment):
    response = requests.patch(baseUrl+"/"+str(id),json=enrollment)
    return response.json()

def deleteEnrollment(id):
    response = requests.delete(baseUrl+"/"+str(id))
    return response.json()