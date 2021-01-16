from django.contrib.auth.models import User
user = User.objects.create_user('Mak', 'mak@testlearn.com', 'vish123')
user.last_name = 'mak'
user.save()

from user_management.models.lappusers import LappUser
luser=LappUser.objects.create(user=user,firstname='Mak',lastname='menon',emailId='mak@datasocle.com',
                        street1='abc', street2='bca', city='dba', state='pal', country='India',
                        zip_pin=100100, qualification='btech',status='Active',isInstractor=True)


quiz =  [
        {
            "question" : "What is Apache ?",
            "option1"  : "option1",
            "option2"  : "option2",
            "option3"  : "option3",
            "answer"   : "option1"
        },
        {
            "question" : "What is Python ?",
            "option1"  : "option1",
            "option2"  : "option2",
            "option3"  : "option3",
            "answer"   : "option2"
        },
        {
            "question" : "What is Pyspark?",
            "option1"  : "option1",
            "option2"  : "option2",
            "option3"  : "option3",
            "answer"   : "option1"
        },
        {
            "question" : "What is Spark ?",
            "option1"  : "option1",
            "option2"  : "option2",
            "option3"  : "option3",
            "answer"   : "option1"
        },
        {
            "question" : "How is Apache streaming done ?",
            "option1"  : "option1",
            "option2"  : "option2",
            "option3"  : "option3",
            "answer"   : "option1"
        }
    ]
    
from content_management.services.course_service import courseService
course=courseService.updateOrCreate('first course',
                                    'first course has a lot of description',
                                    author=luser,
                                    quiz=quiz,price=10.00)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getById(1)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getByName('first course')
print(course.__dict__)