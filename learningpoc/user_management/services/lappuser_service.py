from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
import logging
from DSServices.services import DSServices
from DSServices.services import servicemethod
# Data Socle Imports Section:
from user_management.messages import LappUserMessage
from user_management.repo.lappuser_repo import LappUserRepo

logger = logging.getLogger(__name__)

class LappUserService(DSServices):
    def __init__(self):
        self.lappUserRepo = LappUserRepo()

    @servicemethod(LappUserMessage)
    def getById(self,courseId):
        return self.lappUserRepo.getById(courseId)

    @servicemethod(LappUserMessage)
    def getByEmailId(self, emailId):
        return self.lappUserRepo.getByEmailId(emailId)

    @servicemethod()
    def updateOrCreate(self, user_id, firstname, lastname, emailId, street1,street2, city, state,
                             country, zip_pin, qualification, isInstractor=False, isContentAdmin=False, isLearner=True):
        logger.info("updateOrCreate invoked for lappUserService with emailId = {}".format(emailId))
        return self.lappUserRepo.updateOrCreate(user_id, firstname, lastname, emailId, street1,street2, city, state,
                             country, zip_pin, qualification, isInstractor, isContentAdmin, isLearner)

lappUserService = LappUserService()
