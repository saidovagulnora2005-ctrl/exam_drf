from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.CharField(max_length=100)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Courses(models.Model):
    author_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=9)
    is_published = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Lessons(models.Model):
    course_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tasks(models.Model):
    lesson_id = models.ForeignKey(Lessons,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    task_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskSubmissions(models.Model):
    task_id = models.ForeignKey(Tasks,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    submission = models.TextField()
    grade = models.DecimalField(max_digits=9, decimal_places=2)
    feedback = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)


class Purchases(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=50)
    purchased_at = models.DateTimeField(auto_now_add=True)


class LessonProgress(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)


class Reviews(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




