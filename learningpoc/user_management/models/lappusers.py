from __future__ import absolute_import
from __future__ import unicode_literals

# Third Party/Django Imports Section:
from django.contrib.auth.models import User
from django.db import models


class LappUserStatus(object):
    active = "ACTIVE"
    inactive = "INACTIVE"

LAPPUSERS_STATUS_CHOICE = (
    (LappUserStatus.active, "Active"),
    (LappUserStatus.inactive, "Inactive")
)

class UserType(object):
    learner = 'LEARNER'
    instractor = 'INSTRACTOR'
    contentAdmin = 'CONTENT_ADMIN'


class LappUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    firstname = models.CharField(max_length=254, null=False, blank=False, db_index=True)
    lastname = models.CharField(max_length=254, null=False, blank=False, db_index=True)
    profilePic = models.URLField(verbose_name="Profile picture url", null=True, blank=True)
    emailId = models.EmailField(null=False, blank=False, db_index=True)
    contactNumber = models.CharField(max_length=15, null=True, blank=True)
    alterContactNumber = models.CharField(max_length=15, null=True, blank=True)
    street1 = models.CharField(max_length=254, null=False, blank=False)
    street2 = models.CharField(max_length=254, null=False, blank=False)
    city = models.CharField(max_length=254, null=False, blank=False)
    state = models.CharField(max_length=254, null=False, blank=False)
    country = models.CharField(max_length=254, null=False, blank=False)
    zip_pin = models.CharField(max_length=254, null=False, blank=False)
    DOB = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    qualification = models.CharField(max_length=254, null=False, blank=False)
    status = models.CharField(max_length=50, choices=LAPPUSERS_STATUS_CHOICE ,null=False, blank=False, default=LappUserStatus.active)
    isInstractor = models.BooleanField(verbose_name="Is this user an instractor", default=False)
    isContentAdmin = models.BooleanField(verbose_name="Is this user a content admin", default=False)
    isLearner = models.BooleanField(verbose_name="Is this user a learner", default=True)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

    @property
    def fullName(self):
        return str(self)


