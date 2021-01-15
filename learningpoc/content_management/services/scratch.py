from django.contrib.auth.models import User
user = User.objects.create_user('Vish', 'vmenon@testlearn.com', 'vish123')
user.last_name = 'menon'
user.save()

from user_management.models.lappusers import LappUser
luser=LappUser.objects.create(user=user,firstname='Vish',lastname='menon',emailId='vmenon@datasocle.com',
                        street1='abc', street2='bca', city='dba', state='pal', country='India',
                        zip_pin=100100, qualification='btech',status='Active',isInstractor=True)


quiz = {'dummy':'dummy'}
from content_management.services.course_service import courseService
course=courseService.updateOrCreate('first course',
                                    'first course has a lot of description',
                                    author=luser,
                                    quiz=quiz)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getById(1)
print(course.__dict__)

from content_management.services.course_service import courseService
course=courseService.getByName('first course')
print(course.__dict__)