import sys

VERSION = (0, 0, 0, 'dev')
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


if (2, 7) <= sys.version_info < (3, 2):
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
    import logging
    logger = logging.getLogger('pydrill')
    logger.addHandler(logging.NullHandler())
