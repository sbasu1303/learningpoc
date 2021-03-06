from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from frontend.utils import get_courses
from crum import get_current_user
from content_management.services.course_service import courseService
from user_management.services.lappuser_service import lappUserService
from user_management.models.lappusers import LappUser
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect
import json

# Create your views here.

def show_index(request, context=None):
    items = courseService.getall()
    insts = lappUserService.getallInst()
    last_name = ''
    user = request.user
    if request.user.is_anonymous == False:
        last_name = request.user.last_name
        lappuser = lappUserService.getByEmailId(user.email)
        user = lappuser
    context = {
        'last_name': last_name,
        'items' : items,
        'user': user,
        'instructors':insts
    }
    return render(request, 'index.html', context)

# def show_home(request, context=None):
#     user = request.user
#     items = courseService.getall()
#     insts = lappUserService.getallInst()
#     lappuser = lappUserService.getByEmailId(request.user.email)
#     print(lappuser)
#     context = {
#         'last_name': request.user.last_name,
#         'courses': items,
#         'user': lappuser,
#         'instructors':insts
#     }
#     return render(request, 'home.html', context)




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
            # items = courseService.getall()
            # insts = lappUserService.getallInst()
            # lappuser = lappUserService.getByEmailId(user.email)
            # print(lappuser)
            # context = {
            #     'last_name': user.last_name,
            #     'courses': items,
            #     'user': lappuser,
            #     'instructors':insts
            # }
            # ##User is associated with the session
            # print(request.user.__dict__)
            ##
            
            response = redirect('/index.html')
            return response
        else:
            return HttpResponse("Sorry account not found or password is invalid")



def show_courses(request, context=None):
    if request.method == "GET":
        items = courseService.getall()
        print(request.user)
        if request.user.is_anonymous == False:
            lappuser = lappUserService.getByEmailId(request.user.email)
            print(lappuser)
            #print(lappuser.isInstractor,"tttt")
            context = {
                "items" : items,
                "user" : lappuser
            }
            return render(request, 'courses.html', context)
        else:
            context = {
                "items" : items,
                "user" : request.user
            }
            return render(request, 'courses.html', context)

    else:
        c_name = request.POST.get("course")
        c_status = request.POST.get("status")
        courseService.updateStatus(c_name,c_status)
        items = courseService.getall()
        print(items)
        lappuser = lappUserService.getByEmailId(request.user.email)
        context = {
            "items" : items,
            "user" : lappuser
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
        # print(type(course.quiz))
        print(course.quiz)
        course.quiz = course.quiz.replace("'", '"')
        course.quiz = json.loads(course.quiz)
        context = {
            "quiz" : course.quiz,
            "course" : course

        }
        return render(request, 'course-single-02.html', context)
    else:
        return HttpResponse("Sorry account not found or password is invalid")


def show_instructors(request, context=None):

    insts = lappUserService.getallInst()
    context = {
        "instructors" : insts
    }
    return render(request, 'instructors.html', context)

def show_instructor1(request, context=None):
    if request.method == "GET":
        email = request.GET.get("emailId")
        inst = lappUserService.getByEmailId(email)
        context = {
        "instructor" : inst
        }
        return render(request, 'instructor-single.html', context)

def add_course(request, context=None):
    if request.method == 'POST' and request.user.is_anonymous == False:

        print(request.POST);
        print(request.FILES);
        myfile = request.FILES['video']
        myimage = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(request.POST.get("course_name")+".mov", myfile)
        imagename = fs.save(request.POST.get("course_name")+".jpg", myimage)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)


        q_list = [];
        if int(request.POST.get("number")) > 1:
            for i in range(1,int(request.POST.get("number"))):
                try :
                    q = request.POST.get("question " + str(i))
                    opt1 = request.POST.get("option1 " + str(i));
                    opt2 = request.POST.get("option2 " + str(i));
                    opt3 = request.POST.get("option3 " + str(i));
                    ans = request.POST.get("answer " + str(i));
                    print(q,opt1,opt2,opt3,ans)

                    if ans == opt1:
                        ans = "a"
                    elif ans == opt2:
                        ans = "b"
                    else:
                        ans = "c"

                    quest = {}
                    quest["question"] = q
                    quest["correctAnswer"] = ans
                    options = {}
                    options["a"] = opt1
                    options["b"] = opt2
                    options["c"] = opt3
                    quest["answers"] = options

                    q_list.append(quest)

                except :
                    print("deleted")

        print(q_list)
        luser = LappUser.objects.get(emailId = request.user.email)
        course=courseService.updateOrCreate(request.POST.get("course_name"),
                                    request.POST.get("description"),
                                    author=luser,
                                    quiz=q_list,price=float(request.POST.get("price")))

        response = redirect('/course-single-01.html?name='+request.POST.get("course_name"))
        return response

    else:
        return render(request, 'add-course.html', context)

def logout_user(request,context=None):
    if request.method == "GET":
        logout(request)
        response = redirect('/index.html')
        return response

def error404(request,context=None):

    #return render(request, 'coming-soon.html', context)
    return HttpResponse("This page does not exist.")

def error500(request,context=None):
    #return render(request, 'faq.html', context)
    return HttpResponse("There was some error, please try again.")










