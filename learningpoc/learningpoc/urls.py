"""learningpoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from frontend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.show_index, name='home'),
    re_path(r'^index.html$', views.show_index, name='home'),
    re_path(r'^login.html$', views.show_login, name='login'),
    re_path(r'^courses.html$', views.show_courses, name='courses'),
    re_path(r'^course-single-01.html$', views.show_course1, name='course1'),
    re_path(r'^course-single-02.html$', views.show_course2, name='course2'),
    re_path(r'^check-quiz$', views.check_quiz, name='quiz'),
    re_path(r'^instructors.html$', views.show_instructors, name='instructors'),
    re_path(r'^instructor-single.html$', views.show_instructor1, name='instructor1'),
]
