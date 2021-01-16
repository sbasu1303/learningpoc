from django.contrib.auth.models import User
user = User.objects.create_user('Vish1', 'vmenon1@testlearn.com', 'vish1234')
user.last_name = 'menon'
user.save()

from user_management.services.lappuser_service import lappUserService
luser=lappUserService.updateOrCreate( user_id=user.id, firstname='Vish1', lastname='menon',
                                      emailId='vmenon1@testlearn.com', street1='street1', street2='street2',
                                      city='city', state='state', country='country', zip_pin='zip_pin',
                                      qualification='qualification1', isInstractor=True,
                                      isContentAdmin=False, isLearner=True)
print (luser.__dict__)

luser=lappUserService.getByEmailId('vmenon1@testlearn.com')
print (luser.__dict__)

luser=lappUserService.getById(luser.id)
print (luser.__dict__)

