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
        "question": "Who invented JavaScript?",
        "answers": {
          "a": "Douglas Crockford",
          "b": "Sheryl Sandberg",
          "c": "Brendan Eich"
        },
        "correctAnswer": "c"
      },
      {
        "question": "Which one of these is a JavaScript package manager?",
        "answers": {
          "a": "Node.js",
          "b": "TypeScript",
          "c": "npm"
        },
        "correctAnswer": "c"
      },
      {
        "question": "Which tool can you use to ensure code quality?",
        "answers": {
          "a": "Angular",
          "b": "jQuery",
          "c": "RequireJS",
          "d": "ESLint"
        },
        "correctAnswer": "d"
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