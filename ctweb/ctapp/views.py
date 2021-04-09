from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import teacher,student,subject,teacher_assign,student_submission,assignment,Class,Test
from django.contrib import auth
from django.shortcuts import redirect,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .forms import TeacherForm,UserForm,AssignCreateForm,AssignSubmitForm
from django.urls import reverse
import datetime

# Create your views here.
def index(request):
    template = loader.get_template('index.html')# change to index.html
    teachers = teacher_assign.objects.all()
    st = student.objects.all()
    subjects = subject.objects.all()
    tests = Test.objects.all()
    print(tests)
    context = {"teachers":teachers,"student":st,"sub":subjects,'Test':tests}
    return HttpResponse(template.render(context, request))



#teacher views
def teacher_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            tobj = teacher.objects.get(user=user)
            #print(id,username,password)
            #return HttpResponseRedirect('/t_dashboard/%d/' % tobj.id)
            url = reverse('teacher:t_db', kwargs={'id': tobj.id})
            return HttpResponseRedirect(url)
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/t_login')
    else:
        #form = TeacherForm()
        context = {}
        template = loader.get_template('teacher login.html')
        return HttpResponse(template.render(context, request))


def teacher_signup(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        form = TeacherForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            if form.is_valid():
                new_teacher = form.save(commit=False)
                new_teacher.user = user
                new_teacher.save()
                print(new_teacher)
    form = TeacherForm()
    uform = UserForm()
    context = {'form': form,'uform':uform}
    template = loader.get_template('student signup.html')
    return HttpResponse(template.render(context, request))




@login_required(login_url='t_login/')
def teacher_dashboard(request,id):
    template = loader.get_template('index.html')#update it!!!!!!!!
    current_teacher = teacher.objects.get(id=id)
    assigned_classes = get_classes(current_teacher)
    context = {'teacher':current_teacher,'class_list':assigned_classes}
    return HttpResponse(template.render(context, request))


@login_required(login_url='t_login/')
def teacher_subject_assign(request, id, t_assign_id):           # to list assignements given subject and class
    template = loader.get_template('index.html')
    current_teacher = teacher.objects.get(id=id)
    current_subject = t_assign_id.s_id
    current_class = t_assign_id.c_id
    assignment_list = get_assignment_teacher(current_subject,current_class,current_teacher)
    context = {'teacher':current_teacher,'assignement_list':assignment_list,"subject":subject}
    return HttpResponse(template.render(context, request))


@login_required(login_url='t_login/')
def teacher_assignment_submission(request,a_id):
    template = loader.get_template('index.html')
    student_submission_list = student_submission.objects.filter(a_id=a_id)
    current_teacher = a_id.t_id
    context = {'teacher':current_teacher,'submission_list':student_submission_list}
    return HttpResponse(template.render(context, request))


@login_required(login_url='t_login/')
def teach_assign_create(request,stud_id,assign_id):
    pass


@login_required(login_url='t_login/')
def assignment_viewer(request,id):
    submission = student_submission.objects.filter(id=id)
    template = loader.get_template('index.html')
    context = {'submission':submission}
    return HttpResponse(template.render(context,request))

def t_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/t_login')




#student views
def student_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username,password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            print("correct")
            auth.login(request,user)
            stud = student.objects.get(user=user)
            return HttpResponseRedirect('/s_dashboard/%s/' % stud.enrollment_number)
            #url = reverse('t_dash', kwargs={'id': id})
            #return HttpResponseRedirect(url)
        else:
            print("wrong")
            messages.info(request,"Invalid Credentials")
            return redirect('/s_login')
    else:
        context = {}
        template = loader.get_template('student login.html')
        return HttpResponse(template.render(context, request))


def student_signup(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        form = StudentForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            if form.is_valid():
                new_student = form.save(commit=False)
                new_student.user = user
                new_student.save()
                print(new_student)
    form = StudentForm()
    uform = UserForm()
    context = {'form': form,'uform':uform}
    template = loader.get_template('student signup.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def student_dashboard(request,id):
    template = loader.get_template('student dashboard.html')
    print(id)
    current_student = student.objects.get(enrollment_number=id)
    subjects = get_subjects(current_student)
    tests=get_tests(current_student)
    print(tests)
    now=current_datetime()
    if tests:
        context = {'student':current_student,'subject_list':subjects,'tests':tests,'error':'','cur_date':now}
        return HttpResponse(template.render(context, request))
    error='No tests assigned yet.'
    context = {'student':current_student,'subject_list':subjects,'error':error,'cur_date':now}
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def student_subject_assign(request,id,sub_id):           # to list assignements given subject and class
    template = loader.get_template('student_dashboard_subject_assignments.html')
    current_student = student.objects.get(enrollment_number=id)
    current_subject = subject.objects.get(subject_code=sub_id)
    assignment = get_assignments(current_student,current_subject)
    if assignment:
         context = {'student':current_student,'assignment_list':assignment,'subject':current_subject,'error':''}
    else:
        error="No teacher is assigned for this subject yet."
        context={'error':error,'student':current_student,'subject':current_subject}
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def stud_assign_submit(request,id,assign_id):
    current_student = student.objects.get(enrollment_number=id)
    assignment_current = assignment.objects.get(id=assign_id)
    if request.method=="POST":
        form = AssignSubmitForm(request.POST,request.FILES)
        #print(form.is_valid(),form.data)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.stud_id = current_student
            new_submission.a_id = assignment_current
            new_submission.save()
            print(new_submission,'successful!!!!!!!')
    template = loader.get_template('student_dashboard_assignment_upload.html')
    form = AssignSubmitForm()
    context = {'student':current_student,'assignment':assignment_current,'form':form}
    return HttpResponse(template.render(context, request))




@login_required(login_url='s_login/')
def s_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/s_login')



#Helper functions
def get_subjects(student):
    branch = student.branch
    sem = student.sem
    return subject.objects.filter(branch=branch).filter(sem=sem)


def get_classes(teacher):
    return teacher_assign.objects.filter(t_id=teacher)

def get_tests(student):
    try:
        curr_class = Class.objects.get(sem=student.sem,sec=student.sec,branch=student.branch)
        return Test.objects.filter(c_id=curr_class)
    except Test.DoesNotExist:
        return False

def get_assignments(student,subject):
    sem = student.sem
    sec = student.sec
    try:
        curr_class = Class.objects.filter(sem=sem).get(sec=sec)
        curr_teacher = teacher_assign.objects.filter(c_id=curr_class).get(s_id=subject)
        return assignment.objects.filter(c_id=curr_class).filter(s_id=subject)
    except assignment.DoesNotExist:
        return 'No assignments'.list()
    except teacher_assign.DoesNotExist:
        return False

def get_assignment_teacher(current_subject,current_class,current_teacher):
    try:
        return assignment.objects.filter(t_id=current_teacher).filter(c_id=current_class).filter(s_id=current_subject)
    except teacher_assign.DoesNotExist:
        return False

def current_datetime():
    now = datetime.datetime.now()
    return now



