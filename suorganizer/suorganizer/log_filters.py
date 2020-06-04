"""
On top of handlers and formatters, Python's logger allows
for the creation of filters, which selectively filter the
particular output of a logger.
In this module we define different filters for different
functions.
"""
from logging import Filter


class ManagementFilter(Filter):
    """
    In this class a filter is defined to filter out records from
    execute function so that SQL statements are not logged.
    """

    def filter(self, record):
        if (hasattr(record, 'funcName')
                and record.funcName == 'execute'):
            return False
        else:
            return True
