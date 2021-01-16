from django.shortcuts import render
from frontend.utils import get_courses
from content_management.services.course_service import courseService
from user_management.services.lappuser_service import lappUserService
import json

# Create your views here.

def show_index(request, context=None):
    items = courseService.getall()
    context = {
        "items" : items
    }
    return render(request, 'index.html', context)

def show_login(request, context=None):
    return render(request, 'login.html', context)

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
    c_name = "first course"
    course = courseService.getByName(c_name)
    print(type(course.quiz))
    course.quiz = course.quiz.replace("'", '"')
    course.quiz = json.loads(course.quiz)
    context = {
        "quiz" : course.quiz

    }
    return render(request, 'course-single-02.html', context)

def show_instructors(request, context=None):
    return render(request, 'instructors.html', context)

def show_instructor1(request, context=None):
    return render(request, 'instructor-single.html', context)
