from __future__ import absolute_import

# Standard Library Imports Section:
import logging

# Third Party/Django Imports Section:
from django.core import exceptions as djexceptions
from django.db import IntegrityError

log = logging.getLogger(__name__)

class DSServicesError(Exception):
	code = 'service-error'

	def __str__(self):
		return "%s (%s)" % (self.code, self.args)

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self)

class DSServicesInvalidOperation(DSServicesError):
	code = 'invalid-operation'

class DSServicesValidationError(djexceptions.ValidationError, DSServicesError):
	GENERAL = 1
	INVALID_ARGUMENT = 2
	REQUIRED = 3
	NULL = 4

	@classmethod
	def null(cls, argname):
		return cls({argname: ["This field cannot be null."]}, cls.NULL)

	@classmethod
	def required(cls, argname):
		return cls({argname: ["This field is required."]}, cls.REQUIRED)

	@classmethod
	def arg(cls, argname, message):
		return cls({argname: [message]}, cls.INVALID_ARGUMENT)

	@classmethod
	def form(cls, form):
		raise cls(form.errors)

	def __repr__(self):
		return 'DSServicesValidationError(%s)' % self

	def __init__(self, *args, **kwargs):
		super(DSServicesValidationError, self).__init__(*args, **kwargs)
		self.code = 'Validation-Error'


class DSServicesObjectNotFound(DSServicesError):
	code = 'Object-Not-Found'

	def __init__(self, message=None, missingIds=None):
		if missingIds is None:
			missingIds = []
		super(DSServicesObjectNotFound, self).__init__(message, missingIds)
		self.missingIds = missingIds

class DSServicesAuthenticationError(DSServicesError):
	code = 'Auth-Error'

class DSServicesPermissionError(DSServicesError):
	code = 'Permission-Error'


class DSServicesIntegrityError(DSServicesError):
	code = 'Integrity-Error'

class DSServicesFatalError(DSServicesError):
	code = 'Fatal-Error'

class DSServicesInternalError(DSServicesError):
	code = 'Internal-Error'


def transform_exception(exc):
	if isinstance(exc, DSServicesError):
		return exc
	elif isinstance(exc, djexceptions.PermissionDenied):
		res = DSServicesPermissionError(*exc.args)
	elif isinstance(exc, djexceptions.ObjectDoesNotExist):
		res = DSServicesObjectNotFound(*exc.args)
	elif isinstance(exc, djexceptions.ValidationError):
		try:
			res = DSServicesValidationError(exc.message_dict)
		except AttributeError:
			res = DSServicesValidationError(exc.message)
	elif isinstance(exc, IntegrityError):
		res = DSServicesIntegrityError(*exc.args)
	else:
		res = DSServicesInternalError(*exc.args)
	res._innerException = exc
	return res
