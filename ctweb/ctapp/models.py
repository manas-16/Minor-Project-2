from django.db import models

# Create your models here.
SEMESTER_CHOICES = [("1", 1),("2", 2),("3", 3),("4", 4),("5", 5),("6", 6),("7", 7),("8", 8),]
BRANCH_CHOICES = [("IT","IT"),("CS", "CS"),("EC", "EC"),("MECH", "MECH"),("EE", "EE"),("EX", "EX"),("CIVIL", "CIVIL"),]
SEC_CHOICES = [('A','A'),('B','B'),('C','C')]
CLG_CHOICES = [('LNCT','LNCT'),('LNCTS','LNCTS'),('LNCTE','LNCTE')]
# Create your models here.

class student(models.Model):
    enrollment_number = models.CharField(max_length = 12,primary_key = True)
    name = models.CharField(max_length = 30)
    college_name = models.CharField(max_length = 10,choices = CLG_CHOICES,default = 'LNCT')
    sem = models.CharField(max_length = 20,choices = SEMESTER_CHOICES,default = '6')
    sec = models.CharField(max_length = 1,choices = SEC_CHOICES,default = 'A')
    branch= models.CharField(max_length = 20,choices = BRANCH_CHOICES,default = 'IT')
    mobile_no = models.CharField(max_length=10)
    email = models.CharField(max_length=30)

    def __str__(self):
        return str(self.enrollment_number)+" - "+ str(self.name)


class teacher(models.Model):
    name = models.CharField(max_length=30)
    college_name = models.CharField(max_length = 10,choices = CLG_CHOICES,default = 'LNCT')
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='IT')
    mobile_no = models.CharField(max_length=10)
    email = models.CharField(max_length=30)

    def __str__(self):
        return  self.name


class subject(models.Model):
    subject_code = models.CharField(max_length = 8,primary_key = True)
    name = models.CharField(max_length = 30)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='IT')
    sem = models.CharField(max_length = 20,choices = SEMESTER_CHOICES,default = '6')

    def __str__(self):
        return str(self.subject_code)+" "+ str(self.name)


class Class(models.Model):
    sem = models.CharField(max_length = 20,choices = SEMESTER_CHOICES,default = '6')
    sec = models.CharField(max_length = 1,choices = SEC_CHOICES,default = 'A')
    branch= models.CharField(max_length = 20,choices = BRANCH_CHOICES,default = 'IT')

    def __str__(self):
        return str(self.sem)+" "+str(self.sec)+" - "+str(self.branch)


class teacher_assign(models.Model):
    c_id  = models.ForeignKey(Class,on_delete=models.CASCADE)       #class id
    s_id = models.ForeignKey(subject,on_delete=models.CASCADE)  #subject id
    t_id = models.ForeignKey(teacher,on_delete=models.CASCADE)  #teacher id
    def __str__(self):
        t_name = str(teacher.objects.get(pk=self.t_id)['name'])     #get name of teacher
        s_name = str(subject.objects.get(pk=self.s_id)['name'])     #get subject name
        sem_sec = str(Class.objects.get(pk=self.c_id)['sem'])+str(Class.objects.get(pk=self.c_id)['sec'])
        return sem_sec+" - "+s_name+' - ' + t_name

class assignment(models.Model):
    c_id  = models.ForeignKey(Class,on_delete=models.CASCADE)       #class id
    s_id = models.ForeignKey(subject,on_delete=models.CASCADE)  #subject id
    t_id = models.ForeignKey(teacher,on_delete=models.CASCADE)  #teacher id
    topic = models.CharField(max_length=50)
    last_date = models.DateField()

    def __str__(self):
        s_name = str(subject.objects.get(pk=self.s_id)['name'])     #get subject name
        sem_sec = str(Class.objects.get(pk=self.c_id)['sem'])+str(Class.objects.get(pk=self.c_id)['sec'])
        return sem_sec+" - "+s_name+' - ' + str(self.topic)


#to get separate folder for each assignment
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/sem_sec_subject_topic/<filename>
    folder = str(instance.a_id.c_id.sem) + "_" + str(instance.a_id.c_id.sec) + "_" + str(instance.a_id.s_id.name) + "_"+str(instance.a_id.topic)
    return 'class_{0}/{1}'.format(folder, filename)



class student_submission(models.Model):
    a_id = models.ForeignKey(assignment,on_delete=models.CASCADE)
    stud_id = models.ForeignKey(student,on_delete=models.CASCADE)
    file = models.FileField(upload_to =user_directory_path)

    def __str__(self):
        s_name = str(subject.objects.get(pk=assignment.objects.get(pk=self.a_id)['s_id'])['name'])  #subject name
        topic = str(assignment.objects.get(pk=self.a_id)['topic'])  #topic name
        sem_sec = str(Class.objects.get(pk=self.assignment.objects.get(pk=self.a_id)['c_id'])['sem'])+str(Class.objects.get(pk=self.assignment.objects.get(pk=self.a_id)['c_id'])['sec'])
        return str(self.stud_id)+" - "+sem_sec+" - "+ s_name + " - "+ "topic"













