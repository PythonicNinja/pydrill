# -*- coding: utf-8 -*-


from pydrill.exceptions import ConnectionError, ConnectionTimeout, TransportError
from pydrill.serializer import Deserializer, JSONSerializer


class Transport(object):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connection.
    Main interface is the `perform_request` method.
    """

    def __init__(self, host, port, connection_class, serializers=None, default_mimetype='application/json',
                 max_retries=3, retry_on_status=(503, 504,), serializer=JSONSerializer(), deserializer=Deserializer(),
                 retry_on_timeout=False, send_get_body_as='GET', **kwargs):
        self.deserializer = deserializer
        self.port = port
        self.host = host
        self.connection = connection_class(host, port, **kwargs)
        self.retry_on_status = retry_on_status
        self.serializers = serializers
        self.retry_on_timeout = retry_on_timeout
        self.default_mimetype = default_mimetype
        self.max_retries = max_retries
        self.send_get_body_as = send_get_body_as
        self.serializer = serializer

    def perform_request(self, method, url, params=None, body=None):
        """
        Perform the actual request.
        Retrieve a connection.
        Pass all the information to it's perform_request method and return the data.

        :arg method: HTTP method to use
        :arg url: absolute url (without host) to target
        :arg params: dictionary of query parameters, will be handed over to the
            underlying :class:`~pydrill.Connection` class for serialization
        :arg body: body of the request, will be serializes using serializer and
            passed to the connection
        """
        if body is not None:
            body = self.serializer.dumps(body)

            # some clients or environments don't support sending GET with body
            if method in ('HEAD', 'GET') and self.send_get_body_as != 'GET':
                # send it as post instead
                if self.send_get_body_as == 'POST':
                    method = 'POST'

                # or as source parameter
                elif self.send_get_body_as == 'source':
                    if params is None:
                        params = {}
                    params['source'] = body
                    body = None

        if body is not None:
            try:
                body = body.encode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                # bytes/str - no need to re-encode
                pass

        ignore = ()
        timeout = None
        if params:
            timeout = params.pop('request_timeout', None)
            ignore = params.pop('ignore', ())
            if isinstance(ignore, int):
                ignore = (ignore,)

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                response, data, duration = connection.perform_request(method, url, params, body, ignore=ignore,
                                                                      timeout=timeout)
            except TransportError as e:
                retry = False
                if isinstance(e, ConnectionTimeout):
                    retry = self.retry_on_timeout
                elif isinstance(e, ConnectionError):
                    retry = True
                elif e.status_code in self.retry_on_status:
                    retry = True

                if retry:
                    if attempt == self.max_retries:
                        raise
                else:
                    raise
            else:
                if data:
                    data = self.deserializer.loads(data, mimetype=response.headers.get('Content-Type'))
                else:
                    data = {}
                return response, data, duration

    def get_connection(self):
        return self.connection
