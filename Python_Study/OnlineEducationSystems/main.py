import categoryService
import courseService
import lessonService
import studentService
import enrollmentService
import paymentService


category1 = {
    "name": "Programlama",
    "description": "Yazılım geliştirme ile ilgili kurslar."
  }
category2 ={
    "name": "Veritabanı",
    "description": "Veritabanı yönetimi ve SQL ile ilgili kurslar."
  }
categoryUpdate={"name":"Yazılm Geliştirme"}

for category in categoryService.getCategory():
    print(category.get("name") + " - "+ category.get("description"))
# categoryService.createCategory(category2)
#categoryService.updateCategoryByPatch("e300",categoryUpdate)
#categoryService.deleteCategoty("e300")

course1 = {
    "title": "Python Programlama",
    "description": "Python ile temel ve ileri seviye programlama.",
    "category_id": "4e8e",
    "price": 199.99,
    "created_at": "2023-10-01T10:00:00Z"
  }
course2 =   {
    "title": "MySQL ile Veritabanı Yönetimi",
    "description": "MySQL ile veritabanı tasarımı ve yönetimi.",
    "category_id": "fea8",
    "price": 149.99,
    "created_at": "2023-10-02T11:30:00Z"
  }

for course in courseService.getCourse():
    print(course.get("title") + " - ", course.get("price"))
#courseService.createCourse(course2)
#courseUpdate ={"price": 155}
#courseService.updateCourseByPatch("4fe9",courseUpdate)
#courseService.deleteCourse("4fe9")

lesson1 = {
    "title": "Python'a Giriş",
    "content": "Python dilinin temel özellikleri.",
    "video_url": "https://example.com/python-giris",
    "course_id": 1
  }
lesson2 = {
    "title": "MySQL Temel Sorgular",
    "content": "SELECT, INSERT, UPDATE ve DELETE sorguları.",
    "video_url": "https://example.com/mysql-temel-sorgular",
    "course_id": 2
  }

for lesson in lessonService.getLessons():
    print(lesson.get("title") + " - "+ lesson.get("content"))
#lessonService.createLesson(lesson2)
lessonUpdate ={"title": "Güncellenmiş ders adı"}
#lessonService.updateLessonByPatch("8ae1",lessonUpdate)
#lessonService.deleteLesson("8ae1")


student1 = {
    "name": "Ahmet Yılmaz",
    "email": "ahmet@example.com",
    "password": "hashed_password_123"
  }
student2 = {
    "name": "Ayşe Demir",
    "email": "ayse@example.com",
    "password": "hashed_password_456"
  }

for student in studentService.getStudent():
    print(student.get("name"))
#studentService.createStudent(student2)
studentUpdate ={"name": "Berna Uzunoğlu"}
#studentService.updateStudentByPatch("105a",studentUpdate)
#studentService.deleteStudent("6133")

print("------------ Enrollment İşlemleri ------------")

enrollment1 = {
    "student_id": 1,
    "course_id": 1,
    "status": "Devam Ediyor",
    "enrolled_at": "2023-10-05T09:15:00Z"
  }
enrollment2 = {
    "student_id": 2,
    "course_id": 2,
    "status": "Tamamlandı",
    "enrolled_at": "2023-10-06T14:20:00Z"
  }

for enrollment in enrollmentService.getEnrollment():
    print(enrollment)
#enrollmentService.createEnrollment(enrollment2)
enrollmentUpdate ={"title": "Güncellenmiş ders adı"}
#enrollmentService.updateLessonByPatch("8ae1",enrollmentUpdate)
#enrollmentService.deleteLesson("8ae1")


print("------------ Payment İşlemleri ------------")

payment1 = {
    "student_id": 1,
    "course_id": 1,
    "amount": 199.99,
    "status": "Başarılı",
    "transaction_id": "txn_123456",
    "paid_at": "2023-10-05T09:30:00Z"
  }
payment2 = {
    "student_id": 2,
    "course_id": 2,
    "amount": 149.99,
    "status": "Başarılı",
    "transaction_id": "txn_654321",
    "paid_at": "2023-10-06T14:45:00Z"
  }

for payment in paymentService.getLessons():
    print(lesson.get("title") + " - "+ lesson.get("content"))
#lessonService.createLesson(lesson2)
lessonUpdate ={"title": "Güncellenmiş ders adı"}
#lessonService.updateLessonByPatch("8ae1",lessonUpdate)
#lessonService.deleteLesson("8ae1")