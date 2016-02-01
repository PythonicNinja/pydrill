# -*- coding: utf-8 -*-

from pydrill.transport import Transport
from pydrill.client.result import ResultQuery
from pydrill.exceptions import QueryError
from pydrill.connection.requests_conn import RequestsHttpConnection


class PyDrill(object):
    """
    >>> drill = PyDrill(host='localhost', port=8047)
    >>> drill.is_active()
    True
    """
    # TODO: create better docs.

    def __init__(self, host='localhost', port=8047, trasport_class=Transport, connection_class=RequestsHttpConnection, **kwargs):

        self.transport = Transport(host, port, connection_class=connection_class, **kwargs)

    def perform_request(self, method, url, params=None, body=None):
        return ResultQuery(*self.transport.perform_request(method, url, params, body))

    def is_active(self, timeout=2):
        """
        Returns True if the Drill is up, False otherwise.
        """
        result = self.perform_request('HEAD', '/', params={'request_timeout': timeout})
        if result.response.status_code == 200:
            return True
        return False

    def query(self, sql, timeout=10):
        """
        :param sql: string
        :return: pydrill.client.ResultQuery
        """
        if not sql:
            raise QueryError('No query passed to drill.')

        result = self.perform_request(**{
            'method': 'POST',
            'url': '/query.json',
            'body': {
                "queryType": "SQL",
                "query": sql
            },
            'params': {
                'request_timeout': timeout
            }
        })

        return result

    def plan(self, sql):
        """
        :param sql: string
        :return: pydrill.client.ResultQuery
        """
        sql = 'explain plan for ' + sql
        return self.query(sql)
