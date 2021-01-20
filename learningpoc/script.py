#Instructor1
from django.contrib.auth.models import User
user = User.objects.create_user('John', 'john@goodlearning.com', 'john123')
user.last_name = 'Bartlet'
user.save()

from user_management.models.lappusers import LappUser
luser=LappUser.objects.create(user=user,firstname='John',lastname='Bartlet',emailId='john@.goodlearning.com',
                        street1='7922', street2='5Th Avenue', city='Brooklyn', state='New York', country='USA',
                        zip_pin=100100, qualification='B.Tech',status='Active', isInstractor=True, isContentAdmin=False, isLearner=True)

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

quiz =  [
      {
        "question": "Data science is the process of diverse set of data through ?",
        "answers": {
          "a": "Organizing data",
          "b": "Processing data",
          "c": "Analysing data",
          "d": "All of the above"
        },
        "correctAnswer": "d"
      },
      {
        "question": "The modern conception of data science as an independent discipline is sometimes attributed to?",
        "answers": {
          "a": "William S.",
          "b": "John McCarthy",
          "c": "Arthur Samuel"
        },
        "correctAnswer": "a"
      },
      {
        "question": "Which of the following language is used in Data science?",
        "answers": {
          "a": "C",
          "b": "C++",
          "c": "R",
          "d": "Ruby"
        },
        "correctAnswer": "c"
      }
    ]
    
from content_management.services.course_service import courseService
course=courseService.updateOrCreate('Data Science',
                                    'Data science is an inter-disciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from many structural and unstructured data. Data science is related to data mining, machine learning and big data.',
                                    author=luser, quiz=quiz, price=18.99)

#Instructor2
user = User.objects.create_user('Jessica', 'jessica@goodlearning.com', 'jessica123')
user.last_name = 'Kovler'
user.save()

luser=LappUser.objects.create(user=user,firstname='Jessica',lastname='Kovler',emailId='jessica@.goodlearning.com',
                        street1='7922', street2='10Th Avenue', city='Durban', state='KwaZuku-Natal', country='South Africa',
                        zip_pin=121100, qualification='M.Tech',status='Active', isInstractor=True, isContentAdmin=False, isLearner=True)

quiz =  [
      {
        "question": "For tuples and list which is correct?",
        "answers": {
          "a": "List and tuples both are mutable.",
          "b": "List is mutable whereas tuples are immutable.",
          "c": "List and tuples both are immutable."
        },
        "correctAnswer": "b"
      },
      {
        "question": "What command is used to insert 6 in a list ‘‘L’’ at 3rd position ?",
        "answers": {
          "a": "L.insert(2,6)",
          "b": "L.insert(3,6)",
          "c": "L.append(2,6)"
        },
        "correctAnswer": "a"
      },
      {
        "question": "Which among them is incorrect for set s={100,101,102,103}",
        "answers": {
          "a": "Len(s)",
          "b": "Sum(s)",
          "c": "Print(s[3])"
        },
        "correctAnswer": "c"
      }
    ]

course=courseService.updateOrCreate('Python',
                                    'Python is a general-purpose interpreted, interactive, object-oriented, and high-level programming language. It was created by Guido van Rossum during 1985- 1990. Like Perl, Python source code is also available under the GNU General Public License (GPL). This tutorial gives enough understanding on Python programming language.',
                                    author=luser, quiz=quiz, price=17.99)


quiz =  [
      {
        "question": "What is the Django shortcut method to more easily render an html response?",
        "answers": {
          "a": "render_to_html",
          "b": "render_to_response",
          "c": "response_render"
        },
        "correctAnswer": "b"
      },
      {
        "question": "By using django.contrib.humanize, you can use the following filter in your template to display the number 3 as three.",
        "answers": {
          "a": "apnumber",
          "b": "intcomma",
          "c": "intword"
        },
        "correctAnswer": "a"
      },
      {
        "question": "What are the features available in Django web framework?",
        "answers": {
          "a": "CRUD",
          "b": "Templating",
          "c": "Form Handling",
          "d": "All of the above"
        },
        "correctAnswer": "d"
      }
    ]

course=courseService.updateOrCreate('Django',
                                    'Django is a web development framework that assists in building and maintaining quality web applications. Django helps eliminate repetitive tasks making the development process an easy and time saving experience. This tutorial gives a complete understanding of Django.',
                                    author=luser, quiz=quiz, price=10.99)
    

#Learner1
user = User.objects.create_user('Alan', 'alan@goodlearning.com', 'alan123')
user.last_name = 'Whiteside'
user.save()

luser=LappUser.objects.create(user=user,firstname='Alan',lastname='Whiteside',emailId='alan@.goodlearning.com',
                        street1='7922', street2='20Th Cross', city='Durban', state='KwaZulu-Natal', country='South Africa',
                        zip_pin=900100, qualification='Phd',status='Active', isInstractor=False, isContentAdmin=False, isLearner=True)

#Learner2
user = User.objects.create_user('Shirley', 'shirley@goodlearning.com', 'shirley123')
user.last_name = 'Williams'
user.save()

luser=LappUser.objects.create(user=user,firstname='Shirley',lastname='Williams',emailId='shirley@.goodlearning.com',
                        street1='9022', street2='5Th Street', city='Melbourne', state='Victoria', country='Australia',
                        zip_pin=700100, qualification='12th',status='Active', isInstractor=False, isContentAdmin=False, isLearner=True)


#Admin1

user = User.objects.create_user('Vishnu', 'vishnu@goodlearning.com', 'vishnu123')
user.last_name = 'Menon'
user.save()

luser=LappUser.objects.create(user=user,firstname='Vishnu',lastname='Menon',emailId='vishnu@.goodlearning.com',
                        street1='7807', street2='7th Spaces', city='Bangalore', state='Karnataka', country='India',
                        zip_pin=561001, qualification='B.Tech',status='Active', isInstractor=False, isContentAdmin=True, isLearner=False)


#Admin2
user = User.objects.create_user('Satrajit', 'satrajit@goodlearning.com', 'satrajit123')
user.last_name = 'Basu'
user.save()

luser=LappUser.objects.create(user=user,firstname='Satrajit',lastname='Basu',emailId='satrajit@.goodlearning.com',
                        street1='7807', street2='7th Spaces', city='Bangalore', state='Karnataka', country='India',
                        zip_pin=561001, qualification='M.Tech',status='Active', isInstractor=False, isContentAdmin=True, isLearner=False)

