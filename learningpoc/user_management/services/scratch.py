from django.contrib.auth.models import User
user = User.objects.create_user('adminuser', 'admin@testlearn.com', 'test1234')
user.last_name = 'superuser'
user.save()

from user_management.services.lappuser_service import lappUserService
luser=lappUserService.updateOrCreate( user_id=user.id, firstname='adminuser', lastname='superuser',
                                      emailId='admin@testlearn.com', street1='street1', street2='street2',
                                      city='city', state='state', country='country', zip_pin='zip_pin',
                                      qualification='Administrator', isInstractor=True,
                                      isContentAdmin=True, isLearner=True)



print (luser.__dict__)

luser=lappUserService.getByEmailId('admin@testlearn.com')
print (luser.__dict__)

luser=lappUserService.getById(luser.id)
print (luser.__dict__)

