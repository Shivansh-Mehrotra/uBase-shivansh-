from rest_framework import serializers
from .models import Student
import re
from rest_framework.exceptions import ValidationError

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'age', 'email', 'enrollment_date', 'father_name', 'mother_name',)
    #
    # def validate_first_name(self,value):
    #     if not re.match("^[A-Z a-z\s]+$", value):
    #         raise serializers.ValidationError("The first name field must contain only alphabetic characters and spaces.")
    #     return value
    #
    # def validate_last_name(self, value):
    #     if not re.match("^[A-Z a-z\s]+$", value):
    #         raise serializers.ValidationError("The last name field must contain only alphabetic characters and spaces.")
    #     return value
    #
    # def validate_father_name(self, value):
    #     if not re.match("^[A-Z a-z\s]+$", value):
    #         raise serializers.ValidationError("The father's name field must contain only alphabetic characters and spaces.")
    #     return value
    #
    # def validate_mother_name(self, value):
    #     if not re.match("^[A-Z a-z\s]+$", value):
    #         raise serializers.ValidationError("The mother's name field must contain only alphabetic characters and spaces.")
    #     return value


    def validate(self, data):
        pattern = re.compile("^[A-Za-z\s]+$")
        fields_to_validate = ['first_name', 'last_name', 'father_name', 'mother_name']

        for field in fields_to_validate:
            value = data.get(field, "")
            if not pattern.match(value):
                raise serializers.ValidationError({field: f"The {field.replace('_', ' ')} field must contain only alphabetic characters and spaces."})

        return data


    def validate_age(self,value):
        if not isinstance(value, int):
            raise ValidationError('Age must be an integer.')
        if value < 0:
            raise ValidationError('Age cannot be negative.')
        if value > 100:
            raise ValidationError('Age must be a realistic human age (<= 100).')
        return value
