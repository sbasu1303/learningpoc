from __future__ import absolute_import

# Standard Library Imports Section:
import datetime
import re

# Data Socle Imports Section:
from DSServices.exceptions import DSServicesValidationError


def require_message(message_cls, arg_name, arg_value):
	if arg_value is None:
		return

	if not isinstance(arg_value, message_cls):
		raise DSServicesValidationError.arg(
			arg_name, u"Argument must be of type `%s`" % message_cls.__name__)

def require_message_list(message_cls, arg_name, arg_value):
	if arg_value is None:
		return

	if not isinstance(arg_value, list):
		raise DSServicesValidationError.arg(
			arg_name, u"Argument must be a list of type `%s`" % message_cls.__name__)

	[require_message(message_cls, arg_name, a) for a in arg_value]


class DatetimeConverter(object):

	datePatternMatchers = [
		re.compile(r"(?P<year>\d{2,4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}).?"),
		re.compile(r"(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{2,4}).?")
	]

	timePatternMatchers = [
		re.compile(r"(?P<year>\d{2,4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})[T| ](?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2}).?")
	]

	@classmethod
	def convertForDate(cls, val):
		if val is None:
			return val
		# Checking datetime.datetime first
		# because issubclass(datetime.datetime, datetime.date) = True
		if isinstance(val, datetime.datetime):
			return val.date()
		if isinstance(val, datetime.date):
			return val
		if isinstance(val, str):
			if val.strip() == '':
				return None
			date = cls._convertDateFromString(val)
			if date:
				return date

		raise TypeError

	@classmethod
	def convertForDateTime(cls, val):
		if val is None or isinstance(val, datetime.datetime):
			return val
		if isinstance(val, datetime.date):
			return datetime.datetime(val.year, val.month, val.day)
		if isinstance(val, str):
			if val.strip() == '':
				return None
			time = cls._convertTimeFromString(val)
			if time:
				return time
			date = cls._convertDateFromString(val)
			if date:
				return datetime.datetime(date.year, date.month, date.day)

		raise TypeError

	@classmethod
	def _convertDateFromString(cls, val):
		matched = None
		for pattern in cls.datePatternMatchers:
			matched = pattern.match(val)
			if matched:
				break
		if matched:
			matched = matched.groupdict()
			year, month, day = int(matched['year']), int(matched['month']), int(matched['day'])
			if year < 100:
				year += 1900
			return datetime.date(year, month, day)

	@classmethod
	def _convertTimeFromString(cls, val):
		matched = None
		for pattern in cls.timePatternMatchers:
			matched = pattern.match(val)
			if matched:
				break
		if matched:
			matched = matched.groupdict()
			year, month, day = int(matched['year']), int(matched['month']), int(matched['day'])
			hour, minute, second = int(matched['hour']), int(matched['minute']), int(matched['second'])
			if year < 100:
				year += 1900
			return datetime.datetime(
				year, month, day,
				hour, minute, second
			)
