from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
# Data Socle Imports Section:
from DSServices.attribs import DSDecimalAttr, DSIntAttr, DSStrListAttr
from DSServices.attribs import DSStrAttr
from DSServices.messages import DSMessage


class CourseMessage(DSMessage):
	id = DSIntAttr(readonly=True)
	courseName = DSStrAttr(required=True),
	courseDescription = DSStrAttr(required=True),
	contentHash = DSStrAttr(required=False),
	courseS3Key = DSStrAttr(required=False),
	status = DSStrAttr(required=False),
	quiz = DSStrAttr(required=True),
	price = DSDecimalAttr(required=True),
	author = DSStrAttr(required=True)