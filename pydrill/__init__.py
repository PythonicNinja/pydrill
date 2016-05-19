import sys

version = '0.1.0'

VERSION = tuple(map(int, version.split('.')))
__version__ = VERSION
__versionstr__ = version


if (2, 7) <= sys.version_info < (3, 2):
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
    import logging
    logger = logging.getLogger('pydrill')
    logger.addHandler(logging.NullHandler())
