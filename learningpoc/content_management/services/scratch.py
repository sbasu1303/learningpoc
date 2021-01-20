from django.contrib.auth.models import User
user = User.objects.create_user('John', 'john@goodlearning.com', 'john123')
user.last_name = 'Bartlet'
user.save()

from user_management.models.lappusers import LappUser
luser=LappUser.objects.create(user=user,firstname='John',lastname='Bartlet',emailId='john@.goodlearning.com',
                        street1='7922', street2='5Th Avenue', city='Brooklyn', state='New York', country='USA',
                        zip_pin=100100, qualification='B.Tech',status='Active',isInstractor=True)

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
course=courseService.updateOrCreate('JavaScript',
                                    'JavaScript (JS) is a lightweight, interpreted, or just-in-time compiled programming language with first-class functions. While it is most well-known as the scripting language for Web pages, many non-browser environments also use it, such as Node.js, Apache CouchDB and Adobe Acrobat.',
                                    author=luser, quiz=quiz, price=12.99)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getById(1)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getByName('first course')
print(course.__dict__)