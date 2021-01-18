from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'testing@testlearn.com', 'test1234')
user.last_name = 'user'
user.save()

from user_management.services.lappuser_service import lappUserService
luser=lappUserService.updateOrCreate( user_id=user.id, firstname='testuser', lastname='user',
                                      emailId='testing@testlearn.com', street1='street1', street2='street2',
                                      city='city', state='state', country='country', zip_pin='zip_pin',
                                      qualification='qualification1', isInstractor=True,
                                      isContentAdmin=False, isLearner=True)
print (luser.__dict__)

luser=lappUserService.getByEmailId('testing@testlearn.com')
print (luser.__dict__)

luser=lappUserService.getById(luser.id)
print (luser.__dict__)

