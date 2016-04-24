# -*- coding: utf-8 -*-

import os
from pydrill.transport import Transport
from pydrill.client.result import ResultQuery, Result, Stats, Profiles
from pydrill.connection.requests_conn import RequestsHttpConnection
from pydrill.exceptions import QueryError, ConnectionError, TransportError


class PyDrill(object):
    """
    >>> drill = PyDrill(host='localhost', port=8047)
    >>> drill.is_active()
    True
    """
    # TODO: create better docs.

    def __init__(self, host=os.environ.get('PYDRILL_HOST', 'localhost'), port=os.environ.get('PYDRILL_PORT', 8047),
                 trasport_class=Transport, connection_class=RequestsHttpConnection, **kwargs):

        self.transport = trasport_class(host, port, connection_class=connection_class, **kwargs)

    def perform_request(self, method, url, params=None, body=None):
        return self.transport.perform_request(method, url, params, body)

    def is_active(self, timeout=2):
        """
        :param timeout: int
        :return: boolean
        """
        try:
            result = Result(*self.perform_request('HEAD', '/', params={'request_timeout': timeout}))
        except ConnectionError:
            return False
        except TransportError:
            return False

        if result.response.status_code == 200:
            return True

        return False

    def query(self, sql, timeout=10):
        """
        Submit a query and return results.

        :param sql: string
        :param timeout: int
        :return: pydrill.client.ResultQuery
        """
        if not sql:
            raise QueryError('No query passed to drill.')

        result = ResultQuery(*self.perform_request(**{
            'method': 'POST',
            'url': '/query.json',
            'body': {
                "queryType": "SQL",
                "query": sql
            },
            'params': {
                'request_timeout': timeout
            }
        }))

        return result

    def plan(self, sql, timeout=10):
        """
        :param sql: string
        :param timeout: int
        :return: pydrill.client.ResultQuery
        """
        sql = 'explain plan for ' + sql
        return self.query(sql, timeout)

    def stats(self, timeout=10):
        """
        Get Drillbit information, such as ports numbers.

        :param timeout: int
        :return: pydrill.client.Stats
        """
        result = Stats(*self.perform_request(**{
            'method': 'GET',
            'url': '/stats.json',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def metrics(self, timeout=10):
        """
        Get the current memory metrics.

        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/status/metrics',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def threads(self, timeout=10):
        """
        Get the status of threads.

        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/status/threads',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def options(self, timeout=10):
        """
        List the name, default, and data type of the system and session options.

        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/options.json',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def storage(self, timeout=10):
        """
        Get the list of storage plugin names and configurations.

        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/storage.json',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def storage_detail(self, name, timeout=10):
        """
        Get the definition of the named storage plugin.

        :param name: The assigned name in the storage plugin definition.
        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/storage/{0}.json'.format(name),
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def storage_enable(self, name, value=True, timeout=10):
        """
        Enable or disable the named storage plugin.

        :param name: The assigned name in the storage plugin definition.
        :param value: Either True (to enable) or False (to disable).
        :param timeout: int
        :return: pydrill.client.Result
        """
        value = 'true' if value else 'false'
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/storage/{0}/enable/{1}'.format(name, value),
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def storage_update(self, name, config, timeout=10):
        """
        Create or update a storage plugin configuration.

        :param name: The name of the storage plugin configuration to create or update.
        :param config: Overwrites the existing configuration if there is any, and therefore, must include all
        required attributes and definitions.
        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'POST',
            'url': '/storage/{0}.json'.format(name),
            'body': config,
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def storage_delete(self, name, timeout=10):
        """
        Delete a storage plugin configuration.

        :param name: The name of the storage plugin configuration to delete.
        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'DELETE',
            'url': '/storage/{0}.json'.format(name),
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def profiles(self, timeout=10):
        """
        Get the profiles of running and completed queries.

        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Profiles(*self.perform_request(**{
            'method': 'GET',
            'url': '/profiles.json',
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def profile(self, query_id, timeout=10):
        """
        Get the profile of the query that has the given queryid.

        :param query_id: The UUID of the query in standard UUID format that Drill assigns to each query.
        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/profiles/{0}.json'.format(query_id),
            'params': {
                'request_timeout': timeout
            }
        }))
        return result

    def profile_cancel(self, query_id, timeout=10):
        """
        Cancel the query that has the given queryid.

        :param query_id: The UUID of the query in standard UUID format that Drill assigns to each query.
        :param timeout: int
        :return: pydrill.client.Result
        """
        result = Result(*self.perform_request(**{
            'method': 'GET',
            'url': '/profiles/cancel/{0}'.format(query_id),
            'params': {
                'request_timeout': timeout
            }
        }))
        return result
