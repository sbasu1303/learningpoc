from django.shortcuts import render


# Create your views here.

def show_index(request, context=None):
    return render(request, 'index.html', context)

def show_courses(request, context=None):
    return render(request, 'courses.html', context)

def show_course1(request, context=None):
    return render(request, 'course-single-01.html', context)

def show_course2(request, context=None):
    return render(request, 'course-single-02.html', context)
