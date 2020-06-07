# -*- coding: utf-8 -*-
from pydrill.exceptions import ImproperlyConfigured
import logging
import re

logger = logging.getLogger('pydrill')

drill_pandas_type_map = {
        'BIGINT': 'int64',
        'BINARY': 'object',
        'BIT':  'boolean',
        'DATE': 'datetime64',
        'FLOAT4': 'float32',
        'FLOAT8': 'float64',
        'INT': 'int32',
        'INTERVALDAY': 'object',
        'INTERVALYEAR': 'object',
        'SMALLINT': 'int32',
        'TIME': 'timedelta64',
        'TIMESTAMP': 'datetime64',
        'VARDECIMAL': 'object',
        'VARCHAR' : 'string'
        }

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class Result(object):
    def __init__(self, response, data, duration, *args, **kwargs):
        self.response = response
        self.duration = duration
        self.data = data


class ResultQuery(Result):
    """
    Class responsible for maintaining a information returned from Drill.

    It is iterable.
    """
    def __init__(self, response, data, duration, *args, **kwargs):
        super(ResultQuery, self).__init__(response, data, duration, *args, **kwargs)
        self.rows = data.get('rows', [])
        self.columns = data.get('columns', [])
        self.metadata = data.get('metadata', [])

    def __iter__(self):
        for row in self.rows:
            yield row

    def to_dataframe(self, dtype=None):
        if not PANDAS_AVAILABLE:
            raise ImproperlyConfigured("Please install pandas to use ResultQuery.to_dataframe().")

        if dtype:
            # the user has specified a single dtype for the entire dataframe
            return pd.DataFrame.from_dict(self.rows, dtype=dtype)

        df = pd.DataFrame.from_dict(self.rows)

        # The columns in df all have a dtype of object because Drill's HTTP API
        # always quotes the values in the JSON it returns, thereby providing
        # DataFrame.from_dict(...) with a dict of strings.  We now use the
        # metadata returned by Drill to correct this
        for i in range(len(self.columns)):
            # strip any precision information that might be in the metdata e.g. VARCHAR(10)
            m = re.sub(r'\(.*\)', '', self.metadata[i])

            if m in drill_pandas_type_map:
                logger.debug("Mapping column {} of type {} to dtype {}".format(self.columns[i], self.metadata[i], drill_pandas_type_map[m]))
                if m == 'BIT':
                    df[self.columns[i]] = df[self.columns[i]] == 'true'
                elif m == 'TIME': # m in ['TIME', 'INTERVAL']: # parsing of ISO-8601 intervals appears broken as of Pandas 1.0.3
                    df[self.columns[i]] = pd.to_timedelta(df[self.columns[i]])
                else:
                    df[self.columns[i]] = df[self.columns[i]].astype(drill_pandas_type_map[m])
            else:
                logger.warn("Could not map Drill column {} of type {} to a Pandas dtype".format(self.columns[i], m))

        return df


class Drillbit(object):
    def __init__(self, id, address, status, *args, **kwargs):
        self.id = id
        self.address = address
        self.status = status


class Stats(Result):
    def __init__(self, response, data, duration, *args, **kwargs):
        super(Stats, self).__init__(response, data, duration, *args, **kwargs)

        self.drillbits = []

        for metric in data:
            value, name = metric['value'], metric['name']

            if name == 'Number of Drill Bits':
                self.drillbits_number = value
            elif name.startswith('Bit #'):
                address, status = value.split()
                self.drillbits.append(Drillbit(id=name.split('#')[-1], address=address, status=status))
            elif name == 'Data Port Address':
                self.data_port_address = value
            elif name == 'User Port Address':
                self.user_port_address = value
            elif name == 'Control Port Address':
                self.control_port_address = value
            elif name == 'Maximum Direct Memory':
                self.max_direct_memory = value


class Profiles(Result):
    def __init__(self, response, data, duration, *args, **kwargs):
        super(Profiles, self).__init__(response, data, duration, *args, **kwargs)
        self.running_queries = data.get('runningQueries')
        self.finished_queries = data.get('finishedQueries')
