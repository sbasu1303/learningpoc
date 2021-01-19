from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
import json
import logging
from DSServices import DSRepo
from DSServices import repomethod
# Put Third Party/Django Imports Here:
from DSServices.exceptions import DSServicesError
from DSServices.messages import DSMessageList
# Data Socle Imports Section:
from user_management.messages import LappUserMessage
from user_management.models.lappusers import LappUser

logger = logging.getLogger(__name__)


class LappUserRepo(DSRepo):
    def _query(self):
        return LappUser.objects.all()

    @repomethod(LappUserMessage)
    def getById(self, lappuserId):
        return self._query().get(id=lappuserId)
    
    @repomethod(LappUserMessage)
    def getByFullname(self,fullname):
        names = fullname.split()
        res = self._query().get(firstname = names[0], lastname = names[1])
        print(res)
        return res

    @repomethod(LappUserMessage)
    def getByEmailId(self, emailId):
        lappuser = self._query().filter(emailId=emailId)
        if lappuser:
            return lappuser[0]


    @repomethod(DSMessageList(LappUserMessage))
    def getallInst(self):
        lappuser = self._query().filter(isInstractor=True)
        return lappuser

    @repomethod()
    def updateOrCreate(self, user_id, firstname, lastname, emailId, street1,street2, city, state,
                             country, zip_pin, qualification, isInstractor, isContentAdmin, isLearner):

        lappuser = self._query().filter(emailId=emailId)

        mandatory_fields = [user_id, firstname, lastname, emailId, street1,street2, city, state,
                             country, zip_pin, qualification]
        if not lappuser and not all(mandatory_fields):
            raise DSServicesError("Mandatory field for Course creation missing. - {}".format(mandatory_fields))

        if lappuser and len(lappuser) > 1:
            raise DSServicesError("More than one lappsuer with same emailid - {}".format(emailId))

        if not lappuser or (lappuser and len(lappuser) == 1):
            lappuser, created = LappUser.objects.update_or_create(user_id=user_id, firstname=firstname, lastname=lastname,
                                                                  emailId=emailId, street1=street1, street2=street2,
                                                                  city=city, state=state, country=country, zip_pin=zip_pin,
                                                                  qualification=qualification, isInstractor=isInstractor,
                                                                  isContentAdmin=isContentAdmin, isLearner=isLearner)

            logger.info("updateOrCreate done for lappuser: {}, created: {} ".format(emailId, created))

        elif lappuser and len(lappuser) > 1:
            raise DSServicesError("More than one lappuser with same emailId - {}".format(emailId))

        return lappuser