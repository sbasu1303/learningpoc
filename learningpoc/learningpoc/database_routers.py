from __future__ import absolute_import
from __future__ import unicode_literals

# Learning POC Imports Section:
from core_utilities.django_db_utils import db_locate
# Data Socle Imports Section:
from learningpoc.constants import DS_COURSE_DB_LABEL
from learningpoc.settings import DATABASE_APPS_MAPPING


class DSGenericDBRouter(object):
    def db_for_read(self, model, **hints):
        return db_locate(model, model._meta.app_label)

    def db_for_write(self, model, **hints):
        return db_locate(model, model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        db1 = DATABASE_APPS_MAPPING.get(obj1._meta.app_label, DS_COURSE_DB_LABEL)
        db2 = DATABASE_APPS_MAPPING.get(obj2._meta.app_label, DS_COURSE_DB_LABEL)
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if DATABASE_APPS_MAPPING.get(app_label, None):
            return DATABASE_APPS_MAPPING[app_label] == db
        else:
            return db == DS_COURSE_DB_LABEL