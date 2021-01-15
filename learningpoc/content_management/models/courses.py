from __future__ import absolute_import
from __future__ import unicode_literals

# Third Party/Django Imports Section:
from django.db import models

# Learning POC Imports Section:
from user_management.models import LappUser


class CourseStatus(object):
    active = "ACTIVE"
    created = "CREATED"
    underReview = "UNDER_REVIEW"
    rejected = "REJECTED"
    deleted = "DELETED"

COURSE_STATUS_CHOICE = (
    (CourseStatus.active, 'Active'),
    (CourseStatus.underReview, 'Under Review'),
    (CourseStatus.created, 'Created'),
    (CourseStatus.rejected, 'Rejected'),
    (CourseStatus.deleted, 'Deleted')
)


class Course(models.Model):
    courseName = models.CharField(max_length=254, null=False, blank=False, db_index=True)
    courseDescription = models.TextField(verbose_name="Course Description", null=False, blank=False, db_index=True)
    contentHash = models.CharField(max_length=128, null=False, blank=False)
    courseS3Key = models.CharField(max_length=254, null=False, blank=False)
    author = models.ForeignKey(to=LappUser, on_delete=models.CASCADE, null=False, blank=False, related_name='author')
    adminApprover = models.ForeignKey(to=LappUser, null=True, blank=True, related_name='approver', on_delete=models.CASCADE)
    approvedAt = models.DateTimeField(verbose_name="Course approval date time", null=True, blank=True)
    status = models.CharField(max_length=50, choices=COURSE_STATUS_CHOICE)
    quiz = models.JSONField(verbose_name="Quiz content with multi-choice with answers")

    class Meta:
        app_label = 'content_management'
