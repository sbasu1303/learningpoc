from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
# Data Socle Imports Section:
from DSServices.attribs import DSBooleanAttr
from DSServices.attribs import DSIntAttr
from DSServices.attribs import DSStrAttr
from DSServices.messages import DSMessage


class LappUserMessage(DSMessage):
    id = DSIntAttr(readonly=True)
    user_id = DSIntAttr(required=True),
    firstname = DSStrAttr(required=True),
    lastname = DSStrAttr(required=True),
    emailId = DSStrAttr(required=True),
    street1 = DSStrAttr(required=True),
    street2 = DSStrAttr(required=True),
    city = DSStrAttr(required=True),
    state = DSStrAttr(required=True),
    country = DSStrAttr(required=True),
    zip_pin = DSStrAttr(required=True),
    qualification = DSStrAttr(required=True),
    isInstractor = DSBooleanAttr(required=False),
    isContentAdmin = DSBooleanAttr(required=False),
    isLearner = DSBooleanAttr(required=False)