# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = basestring,  # noqa
    from urllib import quote_plus, urlencode  # noqa
    from urlparse import urlparse  # noqa
    from itertools import imap as map  # noqa
else:
    string_types = str, bytes  # noqa
    from urllib.parse import quote_plus, urlencode, urlparse  # noqa
    map = map  # noqa
