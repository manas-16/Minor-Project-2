from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import teacher,student,subject,teacher_assign,student_submission,assignment,Class
from django.contrib import auth
from django.shortcuts import redirect,HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    teachers = teacher_assign.objects.all()
    st = student.objects.all()
    subjects = subject.objects.all()
    context = {'name':"batman","teachers":teachers,"student":st,"sub":subjects}
    return HttpResponse(template.render(context, request))


def teacher_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            id = teacher.objects.get(user=user)
            return HttpResponseRedirect('/t_dash/%s/' % id)
            #url = reverse('t_dash', kwargs={'id': id})
            #return HttpResponseRedirect(url)
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/t_login')
    else:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))


def teacher_dashboard(request,id):
    template = loader.get_template('index.html')
    current_teacher = teacher.objects.get(id=id)
    assigned_classes = get_classes(current_teacher)
    context = {'teacher':current_teacher,'class_list':assigned_classes}
    return HttpResponse(template.render(context, request))


def teacher_d_subject(request, id, t_assign_id):           # to list assignements given subject and class
    template = loader.get_template('index.html')
    current_teacher = teacher.objects.get(id=id)
    current_subject = t_assign_id.s_id
    current_class = t_assign_id.c_id
    assignment_list = get_assignment_teacher(current_subject,current_class,current_teacher)
    context = {'teacher':current_teacher,'assignement_list':assignment_list,"subject":subject}
    return HttpResponse(template.render(context, request))




def student_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            id = student.objects.get(user=user)
            return HttpResponseRedirect('/s_dash/%s/' % id)
            #url = reverse('t_dash', kwargs={'id': id})
            #return HttpResponseRedirect(url)
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/s_login')
    else:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))


def student_dashboard(request,id):
    template = loader.get_template('index.html')
    current_student = student.objects.get(enrollment_number=id)
    subjects = get_subjects(current_student)
    context = {'student':current_student,'subject_list':subjects}
    return HttpResponse(template.render(context, request))


def student_d_subject(request,id,sub_id):           # to list assignements given subject and class
    template = loader.get_template('index.html')
    current_student = student.objects.get(enrollment_number=id)
    current_subject = subject.objects.get(subject_code=sub_id)
    assignment = get_assignments(current_student,current_subject)
    context = {'student':current_student,'assignement_list':assignment,"subject":subject}
    return HttpResponse(template.render(context, request))








#Helper functions
def get_subjects(student):
    branch = student.branch
    sem = student.sem
    return subject.objects.filter(branch=branch).filter(sem=sem)


def get_classes(teacher):
    return teacher_assign.objects.filter(t_id=teacher)

def get_assignments(student,subject):
    sem = student.sem
    sec = student.sec
    curr_class = Class.objects.filter(sem=sem).filter(sec=sec)
    curr_teacher = teacher_assign.objects.filter(c_id=curr_class).filter(s_id=subject)
    return assignment.objects.filter(c_id=curr_class).filter(s_id=subject).filter(t_id=curr_teacher)


def get_assignment_teacher(current_subject,current_class,current_teacher):
    return assignment.objects.filter(t_id=current_teacher).filter(c_id=current_class).filter(s_id=current_subject)



