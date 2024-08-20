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
        return self.name
