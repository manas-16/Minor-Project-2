from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index,),

    path('t_login/', views.teacher_login,name='t_login'),
    path('t_dashboard/<int:id>/', views.teacher_dashboard,name='t_db'),
    path('t_sub_assign/<int:id>/<int:t_assign_id>/', views.teacher_subject_assign,name='t_subject_assignment_list'),
    path('t_assignment_submission/<int:a_id>/', views.teacher_assignment_submission,name="t_assign_submit" ),
    path('t_logout/', views.t_logout,name="t_logout"),
    path('t_assign_form/', views.teach_assign_create,name="create_assign"),
    path('t_s_view_assign/<int:assign_id>/<str:stud_id>/', views.assignment_viewer,name="view_submission" ),

    path('s_login/', views.student_login, name='s_login'),
    path('s_logout/', views.s_logout, name="s_logout"),
    path('s_dashboard/<str:id>/', views.student_dashboard, name='s_db'),
    path('s_sub_assign/<str:id>/<str:sub_id>', views.student_subject_assign, name='s_subject_assignment_list'),
    path('s_assign_form/<str:stud_id>/<int:assign_id>', views.stud_assign_submit, name="submit_assign"),

]