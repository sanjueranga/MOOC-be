from django.db import models
from django.contrib.auth.models import User
from userprofiles.models import Institution
import json

class Course(models.Model):
    course_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    offered_by = models.ForeignKey(Institution, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    duration = models.CharField(max_length=255)
    header_img = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=255)
    tags = models.TextField()  

    def set_tags(self, tags_list):
        self.tags = json.dumps(tags_list)

    def get_tags(self):
        return json.loads(self.tags)
    

class Role(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('course-creator', 'Course Creator'),
        ('non-editing-teacher', 'Non-editing Teacher'),
    ]
    label = models.CharField(max_length=100, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return self.label
    

class CourseTeachers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.username} - {self.course.title}"
    

class Permission(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label

class CoursePermissions(models.Model):
    ACCESS_LEVEL_CHOICES = [
        ('all', 'All'),
        ('teacher', 'Teacher'),
        ('course-creator', 'Course Creator'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='course-creator')

    def __str__(self):
        return f"{self.course.title} - {self.permission.label} - {self.get_access_level_display()}"
    

class Week(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True, null=True)
    introduction = models.CharField(max_length=255)
    week_number = models.IntegerField(blank=True, null=True)
    
 
    def save(self, *args, **kwargs):
        if not self.week_number:
            last_week = Week.objects.filter(course=self.course).order_by('-week_number').first()
            self.week_number = (last_week.week_number if last_week else 0) + 1
        super().save(*args, **kwargs)

class Video(models.Model):
    link = models.URLField()
    duration = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  

class Notes(models.Model):
    content = models.TextField()
    link = models.URLField(blank=True, null=True) 


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class CodingAssignment(models.Model):
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    points = models.IntegerField(default=1)


class Chapter(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    coding_assignment = models.ForeignKey(CodingAssignment, on_delete=models.CASCADE)


class ChapterContent(models.Model):
    topic = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    coding_assignment = models.ForeignKey(CodingAssignment, on_delete=models.CASCADE)




class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

class Payment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

class VideoProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class NotesProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class QuizProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)

class CodingAssignmentProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assignment = models.ForeignKey(CodingAssignment, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class CertificateTemplate(models.Model):
    template_name = models.CharField(max_length=255)
    template_link = models.URLField()

class Certificate(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    certificate_link = models.URLField()
    issue_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    certificate_number = models.CharField(max_length=255)