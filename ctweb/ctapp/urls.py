from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.index, name='index'),

    path('t_login/', views.teacher_login,name='t_login'),
    path('t_signup/', views.teacher_signup,name='t_signup'),
    path('t_logout/', views.t_logout, name="t_logout"),

    path('t_dashboard/',include(([
        path('<int:id>/', views.teacher_dashboard,name='t_db'),#classes assigned
        path('t_sub_assign/<int:id>/<str:sub_id>/<int:class_id>', views.teacher_subject_assign,name='t_subject_assignment_list'),#list of assign
        path('t_assignment_submission/<int:a_id>/', views.teacher_assignment_submission,name="t_assign_submit" ),#list of submission
        path('t_assign_form/', views.teach_assign_create,name="create_assign"),#create new assignment
        path('t_s_view_assign/<int:assign_id>/<str:stud_id>/', views.assignment_viewer,name="view_submission" ),#view uploaded assignment
        ],'teacherapp'),namespace='teacher')),

    path('s_login/', views.student_login, name='s_login'),
    path('s_signup/', views.student_signup, name='s_signup'),
    path('s_logout/', views.s_logout, name="s_logout"),

    path('s_dashboard/',include(([
        path('<str:id>/', views.student_dashboard, name='s_db'),
        path('s_sub_assign/<str:id>/<str:sub_id>', views.student_subject_assign, name='s_subject_assignment_list'),
        path('s_assign_form/<str:id>/<int:assign_id>', views.stud_assign_submit, name='submit_assign'),
        path('s_download_assign/<str:id>/<int:assign_id>', views.stud_assign_download, name='download_assign'),
    ],'studentapp'),namespace='student')),
]




