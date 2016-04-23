# -*- coding: utf-8 -*-

import logging

from ..exceptions import HTTP_EXCEPTIONS, TransportError

try:
    import simplejson as json
except ImportError:
    import json


logger = logging.getLogger('pydrill')

_tracer_already_configured = 'pydrill.trace' in logging.Logger.manager.loggerDict
tracer = logging.getLogger('pydrill.trace')
if not _tracer_already_configured:
    tracer.propagate = False


class Connection(object):
    """
    Class responsible for maintaining a connection to an Drill node.
    You can create custom connection class similar to :class:`~pydrill.RequestsHttpConnection`


    It's main interface (`perform_request`) is thread-safe.
    Responsible for logging.
    """
    transport_schema = 'http'

    def __init__(self, host='localhost', port=8047, url_prefix='', timeout=10, **kwargs):
        """
        :arg host: hostname of the node (default: localhost)
        :arg port: port to use (integer, default: 8047)
        :arg url_prefix: optional url prefix for pydrill
        :arg timeout: default timeout in seconds (float, default: 10)
        """
        self.host = '%s://%s:%s' % (self.transport_schema, host, port)
        if url_prefix:
            url_prefix = '/' + url_prefix.strip('/')
        self.url_prefix = url_prefix
        self.timeout = timeout

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.host)

    def _pretty_json(self, data):
        """
        pretty JSON in tracer curl logs

        :param data:
        :return:
        """
        try:
            return json.dumps(json.loads(data), sort_keys=True, indent=2, separators=(',', ': ')).replace("'",
                                                                                                          r'\u0027')
        except (ValueError, TypeError):
            # non-json data or a bulk request
            return data

    def log_request_success(self, method, full_url, path, body, status_code, response, duration):
        """ Log a successful API call.  """

        if body:
            body = body.decode('utf-8')

        logger.info(
            '%s %s [status:%s request:%.3fs]', method, full_url,
            status_code, duration
        )
        logger.debug('> %s', body)
        logger.debug('< %s', response)

        if tracer.isEnabledFor(logging.INFO):
            if self.url_prefix:
                path = path.replace(self.url_prefix, '', 1)
            tracer.info("curl -X%s 'http://localhost:8047%s' -d '%s'", method, path,
                        self._pretty_json(body) if body else '')

        if tracer.isEnabledFor(logging.DEBUG):
            tracer.debug('#[%s] (%.3fs)\n#%s', status_code, duration,
                         self._pretty_json(response).replace('\n', '\n#') if response else '')

    def log_request_fail(self, method, full_url, body, duration, status_code=None, exception=None):
        """
        Log an unsuccessful API call.
        """
        logger.warning(
            '%s %s [status:%s request:%.3fs]', method, full_url,
            status_code or 'N/A', duration, exc_info=exception is not None
        )

        if body:
            body = body.decode('utf-8')

        logger.debug('> %s', body)

    def _raise_error(self, status_code, raw_data):
        """
        Locate appropriate exception and raise it.
        """
        error_message = raw_data
        additional_info = None
        try:
            additional_info = json.loads(raw_data)
            error_message = additional_info.get('error', error_message)
            if isinstance(error_message, dict) and 'type' in error_message:
                error_message = error_message['type']
        except:
            pass

        raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        raise NotImplementedError
