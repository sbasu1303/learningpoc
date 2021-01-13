from __future__ import absolute_import

# Standard Library Imports Section:
from decimal import ROUND_HALF_UP
from decimal import Decimal

# Data Socle Imports Section:
from DSServices.exceptions import DSServicesValidationError
from DSServices.utils import DatetimeConverter


def repeated_aware_attr_op(attr, op, val):
	attr_op = getattr(attr, op)
	if attr.repeated:
		if val is None:
			return []
		return [attr_op(v) for v in val]
	return attr_op(val)


class DSBaseAttr(object):

	def __init__(self, from_key=None, readonly=False, required=False, repeated=False, default=None, from_json=False):
		self.from_key = from_key
		self.to_key = None
		self.readonly = readonly
		self.required = required
		self.repeated = repeated
		self.default = self.convert_from(default) if default is not None else None
		self.from_json = from_json

	def copy(self, val):
		# Sub-classes implement only convert_from in most cases
		# using that to make copy type safe.
		return self.convert_from(val)

	def convert_from(self, val):
		return val

	def convert_to(self, val):
		return val

	def convert_to_raw(self, val):
		from DSServices.messages import DSMessage
		return dict(val) if isinstance(val, DSMessage) else val

	def contribute_to_message_class(self, message_cls):
		setattr(message_cls, self.to_key, None)


class DSRawAttr(DSBaseAttr):
	pass


class ProtoAttr(DSBaseAttr):
	pass


class DSIntAttr(DSBaseAttr):
	def convert_from(self, val):
		try:
			return int(val) if val is not None else None
		except (TypeError, ValueError):
			raise DSServicesValidationError("%s is not an integer" % val)


class DSStrAttr(DSBaseAttr):
	def convert_from(self, val):
		try:
			return str(val) if val is not None else None
		except UnicodeDecodeError as e :
			raise DSServicesValidationError(e.args)

class DSStrListAttr(DSBaseAttr):
	def convert_from(self, val):
		if not val:
			return []
		if type(val) != list:
			raise DSServicesValidationError('%s is not a list' % val)
		return [DSStrAttr().convert_from(v) for v in val]

	def copy(self, val):
		return self.convert_from(val)

class DSDateTimeAttr(DSBaseAttr):
	def convert_from(self, val):
		if val is None:
			return None

		try:
			return DatetimeConverter.convertForDateTime(val)
		except TypeError:
			raise DSServicesValidationError("Could not convert to datetime from: %s" % val)


class DSDateAttr(DSBaseAttr):
	def convert_from(self, val):
		if val is None:
			return None

		try:
			return DatetimeConverter.convertForDate(val)
		except TypeError:
			raise DSServicesValidationError("Could not convert to date from: %s" % val)


class DSBooleanAttr(DSBaseAttr):
	def convert_from(self, val):
		try:
			return bool(val) if val is not None else None
		except (TypeError, ValueError) as e:
			raise DSServicesValidationError(e.args)


class DSMessageAttr(DSBaseAttr):

	def __init__(self, message_cls, from_key=None, readonly=True, **kwargs):
		super(DSMessageAttr, self).__init__(from_key=from_key, readonly=readonly, **kwargs)
		self.message_cls = message_cls

	def convert_from(self, val):
		return self.message_cls.convert_from(val)

	def convert_to(self, val):
		raise NotImplementedError('Converting message to instance not implemented')

	def copy(self, val):
		return self.message_cls(val)


class DSSelfReferentialAttr(DSMessageAttr):
	def __init__(self, *args, **kwargs):
		super(DSSelfReferentialAttr, self).__init__(None, *args, **kwargs)

	def contribute_to_message_class(self, message_cls):
		self.message_cls = message_cls
		super(DSSelfReferentialAttr, self).contribute_to_message_class(message_cls)

class DSDecimalAttr(DSBaseAttr):
	def convert_from(self, val):
		if val is None:
			return None

		try:
			return Decimal(val).quantize(Decimal(str(0.0001)), rounding=ROUND_HALF_UP)
		except (TypeError, ValueError, ArithmeticError):
			raise DSServicesValidationError('%s is not a valid decimal' % val)
