from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('ask/', views.ask_question, name='ask_question'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('', views.forum_home, name='forum_home'),  # named URL 'forum_home'


]
