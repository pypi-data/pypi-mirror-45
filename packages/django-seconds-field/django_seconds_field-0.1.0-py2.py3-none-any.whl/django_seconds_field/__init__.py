import datetime

from django.db.models import fields
from django.utils.translation import gettext_lazy as _


VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))


class SecondsField(fields.DurationField):
    description = _("Number of seconds")

    @staticmethod
    def get_internal_type():
        # DurationField uses BigIntegerField
        return 'IntegerField'

    @staticmethod
    def get_db_prep_value(value, connection, prepared=False):
        # Do not convert to miliseconds
        if value is None:
            return value
        return int(round(value.total_seconds()))

    @staticmethod
    def get_db_converters(connection):
        # Use always own converter
        return [SecondsField.convert_durationfield_value]

    @staticmethod
    def convert_durationfield_value(value, _expression, _connection, _context=None):
        if value is None:
            return value
        return datetime.timedelta(seconds=value)
