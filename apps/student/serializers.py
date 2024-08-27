from rest_framework import serializers
from .models import Student
import re
from rest_framework.exceptions import ValidationError

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'age', 'email', 'enrollment_date', 'father_name', 'mother_name',)

    def validate_name(value):
        pattern = re.compile(r'^[A-Za-z\s]+$')
        if not pattern.match(value):
            raise ValidationError('Name must contain only alphabetic characters and spaces.')
        return value

    def validate_age(self,value):
        if not isinstance(value, int):
            raise ValidationError('Age must be an integer.')
        if value < 0:
            raise ValidationError('Age cannot be negative.')
        if value > 100:
            raise ValidationError('Age must be a realistic human age (<= 100).')
        return value
