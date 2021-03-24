from django.forms import ModelForm
from .models import student
from .models import teacher

class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = '__all__'
        '''
        widgets = {
        'user' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'enrollment_number' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'name' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'college_name' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'sem' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'sec' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'branch' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'mobile_no' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        'email' : ModelForm.TextInput(attrs={'class': 'form-control'}),
        }
'''
class TeacherForm(ModelForm):
    class Meta:
        model = teacher
        fields = '__all__'
