from __future__ import absolute_import

# Standard Library Imports Section:
import logging
from functools import wraps

# Data Socle Imports Section:
from DSServices.exceptions import transform_exception


# Placeholder for stat collection
class Placeholder(object):
    def recordCount(*args, **kwargs):
        pass

    def recordTime(*args, **kwargs):
        pass


stats = Placeholder()

logger = logging.getLogger(__name__)


class DSServices_metrics():
    def __init__(self, service_name, method_name, enabled):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def servicemethod(required_transform=None):
    def _decorator(method):
        @wraps(method)
        def _wrappedmethod(instance, *args, **kwargs):
            try:
                if instance.log_requests:
                    logger.info("%s::%s, args=%r",
                                instance.service_name, method.__name__, args)

                with DSServices_metrics(instance.service_name, method.__name__, instance.log_metrics):
                    res = method(instance, *args, **kwargs)

                if res is not None and required_transform:
                    if hasattr(required_transform, 'convert_from'):
                        _required_transform = required_transform.convert_from
                    else:
                        _required_transform = required_transform
                    return _required_transform(res)
                else:
                    return res
            except Exception as e:
                if instance.log_errors:
                    logger.warning("ServiceException: %s::%s, args=%r => %r",
                                   instance.service_name, method.__name__, args, e)
                e = instance._handle_exception(e)
                if e:
                    raise e

        setattr(_wrappedmethod, '_required_transform', required_transform)
        return _wrappedmethod

    return _decorator

class DSServices(object):
    log_requests = True
    log_errors = True
    log_metrics = False

    @property
    def service_name(self):
        return self.__class__.__name__

    def _handle_exception(self, e):
        return transform_exception(e)


DSRepo = DSServices

repomethod = servicemethod
