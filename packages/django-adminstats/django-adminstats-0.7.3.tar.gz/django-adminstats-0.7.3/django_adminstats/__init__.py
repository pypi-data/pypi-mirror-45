import enum

default_app_config = 'django_adminstats.apps.Config'

VERSION = '0.7.3'


class Step(enum.Enum):
    DAY = 'd'
    MONTH = 'm'
    YEAR = 'y'
