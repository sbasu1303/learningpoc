from __future__ import absolute_import
from __future__ import unicode_literals
from DSServices.messages import DSMessageList

# Standard Library Imports Section:
import logging

# Data Socle Imports Section:
from content_management.messages import CourseMessage
from content_management.repo.course_repo import CourseRepo
from DSServices.services import DSServices
from DSServices.services import servicemethod

logger = logging.getLogger(__name__)

class CourseService(DSServices):
    def __init__(self):
        self.courseRepo = CourseRepo()
    
    @servicemethod(DSMessageList(CourseMessage))
    def getall(self):
        return self.courseRepo.all()

    @servicemethod(CourseMessage)
    def getById(self,courseId):
        return self.courseRepo.getById(courseId)

    @servicemethod(CourseMessage)
    def getByName(self, courseName):
        return self.courseRepo.getByName(courseName)

    @servicemethod()
    def updateOrCreate(self, course_name, course_description, price, content_hash='dummy', course_key= 'dummy', author=None,
                       adminApprover=None, approvedAt=None, status='Active', quiz={}):
        logger.info("updateOrCreate invoked for courseService with course_name = {}".format(course_name))
        return self.courseRepo.updateOrCreate(course_name, course_description, content_hash=content_hash, course_key=course_key, author=author,
                       adminApprover=adminApprover, approvedAt=approvedAt, status=status, quiz=quiz, price=price)

courseService = CourseService()
