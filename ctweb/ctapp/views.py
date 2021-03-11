from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import teacher,student,subject,teacher_assign,student_submission,assignment,Class

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    teachers = teacher_assign.objects.all()
    st = student.objects.all()
    subjects = subject.objects.all()
    context = {'name':"batman","teachers":teachers,"student":st,"sub":subjects}
    return HttpResponse(template.render(context, request))
