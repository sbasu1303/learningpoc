from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from frontend.utils import get_courses
from crum import get_current_user
from content_management.services.course_service import courseService
from user_management.services.lappuser_service import lappUserService
from django.http import HttpResponse
import json

# Create your views here.

def show_index(request, context=None):
    items = courseService.getall()
    context = {
        "items" : items
    }
    return render(request, 'index.html', context)

def show_home(request, context=None):
    return render(request, 'home.html', context)

def show_login(request, context=None):
    if request.method == 'GET':
        return render(request, 'login.html', context)

    if request.method == 'POST':
        #to be removed
        logout(request)
        ##

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = None
        isPass = False

        ##No user associated with the session
        print(request.user)
        ##

        try:
            user = User.objects.get(email=username)
            isPass = user.check_password(password)
            u=authenticate(request,username=username, password=password)
        except:
            return HttpResponse("Sorry account not found or password is invalid")

        if user is not None and isPass:
            login(request, user)
            context = {
                'last_name': user.last_name
            }
            ##User is associated with the session
            print(request.user.__dict__)
            ##
            
            return render(request, 'home.html', context)
        else:
            return HttpResponse("Sorry account not found or password is invalid")

def show_courses(request, context=None):
    items = courseService.getall()
    context = {
        "items" : items
    }
    return render(request, 'courses.html', context)

def show_course1(request, context=None):
    c_name = request.GET.get("name")
    course=courseService.getByName(c_name)
    author = lappUserService.getByfullname(course.author)
    context = {
        "course" : course,
        "author" : author
    }
    return render(request, 'course-single-01.html', context)

def show_course2(request, context=None):
    if request.method == 'GET':
        c_name = request.GET.get("name")
        course = courseService.getByName(c_name)
        print(type(course.quiz))
        course.quiz = course.quiz.replace("'", '"')
        course.quiz = json.loads(course.quiz)
        context = {
            "quiz" : course.quiz,
            "course" : course

        }
        return render(request, 'course-single-02.html', context)
    else:
        return HttpResponse("Sorry account not found or password is invalid")

def check_quiz(request, context=None):
    pass
    data = request.POST
    print(data)
    return HttpResponse("Sorry account not found or password is invalid")


def show_instructors(request, context=None):
    return render(request, 'instructors.html', context)

def show_instructor1(request, context=None):
    return render(request, 'instructor-single.html', context)
