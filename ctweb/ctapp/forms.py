from django.forms import ModelForm
from .models import student
from .models import teacher,assignment,student_submission,Test,student_testsubmission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = ["enrollment_number", "name", "college_name", "email", 'sem', 'sec','branch','mobile_no']
        
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

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['username'].help_text=' '
      self.fields['password1'].help_text=' '
      self.fields['password2'].help_text=' '
    class Meta:
        model = User
        fields = ('username','password1', 'password2')
        

class TeacherForm(ModelForm):
    class Meta:
        model = teacher
        fields = ["name", "college_name", "email", 'branch','mobile_no']


class AssignSubmitForm(ModelForm):
    class Meta:
        model = student_submission
        fields = ["file"]


class AssignCreateForm(ModelForm):
    class Meta:
        model = assignment
        fields = ["topic","last_date","assignfile"]


class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = ["topic","link","date","starttime","endtime"]




