from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
import json
import logging
# Data Socle Imports Section:
from content_management.messages import CourseMessage
from content_management.models.courses import Course
from DSServices import DSMessageList
from DSServices import DSRepo
from DSServices import repomethod
# Put Third Party/Django Imports Here:
from DSServices.exceptions import DSServicesError

logger = logging.getLogger(__name__)


class CourseRepo(DSRepo):
    def _query(self):
        return Course.objects.all()
    
    @repomethod(DSMessageList(CourseMessage))
    def all(self):
        return self._query()

    @repomethod(CourseMessage)
    def getById(self, courseId):
        return self._query().get(id=courseId)

    @repomethod(CourseMessage)
    def getByName(self, course_name):
        course = self._query().filter(courseName=course_name)
        if course:
            return course[0]

    @repomethod()
    def updateOrCreate(self, course_name, course_description, price, content_hash='dummy', course_key= 'dummy', author=None,
                       adminApprover=None, approvedAt=None, status='Active', quiz={}):

        course = self._query().filter(courseName=course_name)

        mandatory_fields = [course_name, course_description]
        if not course and not all(mandatory_fields):
            raise DSServicesError("Mandatory field for Course creation missing. - {}".format(mandatory_fields))

        if course and len(course) > 1:
            raise DSServicesError("More than one course with same name - {}".format(course_name))

        if not course or (course and len(course) == 1):
            course, created = Course.objects.update_or_create(courseName=course_name,courseDescription=course_description,
                                                              contentHash=content_hash,courseS3Key=course_key,
                                                              author=author,adminApprover=adminApprover,status=status,
                                                              quiz=quiz,price = price)

            logger.info("updateOrCreate done for course_name: {}, created: {} ".format(course_name, created))

        elif course and len(course) > 1:
            raise DSServicesError("More than one client with same name - {}".format(course_name))

        return course