from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    enrollment_date = models.DateField()
    father_name=models.CharField(max_length=40)
    mother_name=models.CharField(max_length=40)

    def __str__(self):
        return self.first_name


class RequestResponseLogData(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=100)
    request_body = models.TextField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    status_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code}"
