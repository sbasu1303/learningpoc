from __future__ import absolute_import

# Standard Library Imports Section:
import logging

# Third Party/Django Imports Section:
from protobuf_to_dict import dict_to_protobuf
from protobuf_to_dict import protobuf_to_dict
from six import with_metaclass

# Data Socle Imports Section:
from DSServices.attribs import DSBaseAttr
from DSServices.attribs import DSMessageAttr
from DSServices.attribs import ProtoAttr
from DSServices.attribs import repeated_aware_attr_op
from DSServices.exceptions import DSServicesValidationError

log = logging.getLogger(__name__)

def _message_attr_prep_to_dict(message, attr):
	attrval = getattr(message, attr.to_key)

	if attrval is None:
		return attrval

	if not isinstance(attr, DSMessageAttr):
		return attrval

	if attr.repeated:
		return [dict(v) for v in attrval]
	return dict(attrval)


def _init_defaults(target):
	for attr in target._schema.values():
		val = attr.default
		if val is not None:
			setattr(target, attr.to_key, repeated_aware_attr_op(attr, 'copy', val))


def _update_nested_json(json, path, value):
	"""update existing dict for given path and value

	The value is inserted in the json node obtained by traversing the specified path.
	The path could contain dot ('.') separated keys.
	The intermediary traversed nodes will be created if they do not exist.
	Otherwise their content will not be updated.
	The given value will be inserted in the final node.

	Args:
		json (dict): dict to be updated
		path (str):  path including keys to be traversed on each level
		value (object): value to be stored in given path

	Returns:
		dict: updated dict

	"""
	keys = path.split('.')
	iterator = json
	for key in keys[:-1]:
		iterator = iterator.setdefault(key, {})
	iterator.setdefault(keys[-1], value)
	return json


def _copy_message(target, source):
	if source is None:
		raise ValueError("Cannot copy from null source.")

	isdict = isinstance(source, dict)

	for attr in target._schema.values():
		try:
			if isdict:
				val = source[attr.to_key]
			else:
				val = getattr(source, attr.to_key)
		except (KeyError, AttributeError):
			val = attr.default

		if attr.required and val is None:
			raise DSServicesValidationError.required(attr.to_key)

		if val is not None:
			setattr(target, attr.to_key, repeated_aware_attr_op(attr, 'copy', val))
		else:
			setattr(target, attr.to_key, val)

	return target


def _convert_obj(target, source):
	"""Converting Django model instance to DSMessage

	Args:
		target (DSMessage): instance of derived class from DSMessage
		source (instance): instance of a Django model

	Returns:
		DSMessage: target

	"""
	if source is None:
		raise ValueError("Cannot convert null source.")

	isdict = isinstance(source, dict)

	for from_key, attr in target._from_schema.items():
		keys = from_key.split('.') if attr.from_json else [from_key]
		try:
			val = source[keys[0]] if isdict else getattr(source, keys[0])
			for key in keys[1:]:
				# if multiple keys exist then the data is in JSON format
				val = val[key]
		except (KeyError, AttributeError):
			val = attr.default
		if attr.required and val is None:
			raise DSServicesValidationError.required(from_key)

		setattr(target, attr.to_key, repeated_aware_attr_op(attr, 'convert_from', val))

	return target


class MessageMetaclass(type):
	def __init__(cls, name, bases, attrs):
		if bases == (object,) or name == 'ProtoMessage':
			return  # That's DSMessage class itself

		schema = {}
		from_schema = {}
		protobuf_class = getattr(cls, 'proto_class', None)
		if protobuf_class:
			attrs = {k:ProtoAttr() for k in [f.name for f in protobuf_class.DESCRIPTOR.fields]}

		for k, attr in attrs.items():
			if type(attr) == tuple:
				attr = attr[0]
			if not isinstance(attr, DSBaseAttr):
				continue

			from_key = attr.from_key if attr.from_key else k
			attr.from_key = from_key
			attr.to_key = k
			schema[k] = attr
			from_schema[from_key] = attr

			if not protobuf_class:
				attr.contribute_to_message_class(cls)

		for baseCls in bases:
			if not issubclass(baseCls, DSMessage):
				continue

			schema.update(getattr(baseCls, '_schema', {}))
			from_schema.update(getattr(baseCls, '_from_schema', {}))

		cls._schema = schema
		cls._from_schema = from_schema


class DSMessage(with_metaclass(MessageMetaclass, object)):
	def __init__(self, *args, **kwargs):
		"""Constructs a DSMessage.

		Usage:
			DSMessage(**kwargs) - Initialize attributes with **kwargs.

			DSMessage(<dict>) - Equivalent to DSMessage(**dict).

			DSMessage(<object>) - Copy attributes from object, raises a `ValueError` if
				the object does not have all attributes.

			DSMessage(<message_instance_of_same_type>) - Create a copy of the provided
				message if the message is the same type.
		"""
		if len(kwargs):
			if len(args):
				raise ValueError(
					"Cannot initialize with keyword and positional args at the same time.")
			msgObj = kwargs
		elif len(args) > 1:
			raise ValueError("Expected zero or one argument, received %d." % len(args))
		elif len(args) == 1:
			msgObj = args[0]
		else:
			msgObj = None

		if msgObj is None:
			_init_defaults(self)
		elif isinstance(msgObj, type(self)):
			_copy_message(self, msgObj)
		elif isinstance(msgObj, dict):
			for k in msgObj.keys():
				if k not in self._schema and not getattr(self, 'proto_instance', None):
					raise ValueError("Unexpected attr `%s`" % k)
			_copy_message(self, msgObj)
		else:
			_convert_obj(self, msgObj)

	@classmethod
	def convert_from(cls, msgObj):
		if msgObj is None:
			return None
		if isinstance(msgObj, cls):
			return msgObj

		return _convert_obj(cls(), msgObj)

	def to_dict(self):
		serialized_keys = {}

		for from_key, attr in self._from_schema.items():
			operation = 'convert_to_raw' if attr.from_json else 'convert_to'
			value = repeated_aware_attr_op(attr, operation, getattr(self, attr.to_key))
			if attr.from_json:
				_update_nested_json(serialized_keys, from_key, value)
			else:
				serialized_keys.update({from_key: value})

		return serialized_keys

	@staticmethod
	def apply_to(source, target):
		"""Converting DSMessage to Django model instance

		Args:
			source (DSMessage): instance of derived class from DSMessage
			target (instance): instance of a Django model

		Returns:
			instance: target

		"""
		serialized_keys = {}
		for from_key, attr in source._from_schema.items():
			if attr.readonly:
				continue
			operation = 'convert_to_raw' if attr.from_json else 'convert_to'
			value = repeated_aware_attr_op(attr, operation, getattr(source, attr.to_key))
			if attr.from_json:
				_update_nested_json(serialized_keys, from_key, value)
			else:
				serialized_keys.update({from_key: value})

		isdict = isinstance(target, dict)
		for key, value in serialized_keys.items():
			if isdict:
				target[key] = value
			else:
				setattr(target, key, value)

		return target

	def apply_update(self, target):
		self.__class__.apply_to(self, target)

	def __iter__(self):
		for attr in self._schema.values():
			yield (attr.to_key, _message_attr_prep_to_dict(self, attr))

	def __eq__(self, other):
		if not other or not isinstance(other, self.__class__):
			return False
		return dict(self) == dict(other)

	def __ne__(self, other):
		return not self.__eq__(other)


class DSMessageList(object):
	def __init__(self, message_cls):
		self.message_cls = message_cls

	def __call__(self, objs):
		return [self.message_cls(o) for o in objs]

	def convert_from(self, objs):
		return [self.message_cls.convert_from(o) for o in objs]


class ProtoMessageMetaclass(MessageMetaclass):
	# For enums/consts on proto.
	def __getattr__(self, name):
		if name != 'proto_class':
			return getattr(self.proto_class, name)
		return super(ProtoMessageMetaclass, self).__getattr__(name)


class ProtoMessage(with_metaclass(ProtoMessageMetaclass, DSMessage)):
	def __init__(self, *args, **kwargs):
		proto_instance = self.proto_class()

		args = list(args)

		if len(args) > 0:
			arg = args[0]
			if type(arg) == str:
				proto_instance = self.proto_class.FromString(arg)
				args = []
			elif isinstance(arg, ProtoMessage):
				proto_instance = arg.get_proto()
				args = []

		self._private = {
			'proto_instance': proto_instance,
			'cached_dict': None
		}
		return super(ProtoMessage, self).__init__(*args, **kwargs)

	def __getattr__(self, name):
		if name != '_private':
			return getattr(self._private['proto_instance'], name)
		else:
			return ProtoMessage._getattr_parent(self, name)

	@classmethod
	def convert_from(cls, obj):
		if obj is None:
			return None
		if isinstance(obj, cls):
			return obj

		return _convert_obj(cls(), obj)

	@staticmethod
	def apply_to(*args, **kwargs):
		raise Exception('not available on ProtoMessage right now')

	@classmethod
	def _getattr_parent(cls, self, name):
		if name in self.__dict__:
			return self.__dict__.get(name)
		else:
			raise AttributeError(name)

	def __setattr__(self, name, value):
		if name != '_private':
			if value is not None:
				self._private['proto_instance'] = dict_to_protobuf(
					self._private['proto_instance'],
					{name:value}
				)
				self._private['cached_dict'] = None
		else:
			super(ProtoMessage, self).__setattr__(name, value)

	def get_proto(self):
		return self._private['proto_instance']

	def __iter__(self):
		if not self._private['cached_dict']:
			self._private['cached_dict'] = protobuf_to_dict(self._private['proto_instance'])

		for key, value in self._private['cached_dict'].items():
			yield (key, value)
