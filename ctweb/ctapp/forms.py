from django.forms import ModelForm
from .models import student
from .models import teacher

class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = '__all__'

class TeacherForm(ModelForm):
    class Meta:
        model = teacher
        fields = '__all__'
