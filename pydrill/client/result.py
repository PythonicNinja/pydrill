# -*- coding: utf-8 -*-
from pydrill.exceptions import ImproperlyConfigured
import logging
import re

logger = logging.getLogger('pydrill')

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

DRILL_PANDAS_TYPE_MAP = {
        'BIGINT': 'Int64',
        'BINARY': 'object',
        'BIT':  'bool',
        'DATE': 'datetime64[ns]',
        'FLOAT4': 'float32',
        'FLOAT8': 'float64',
        'INT': 'Int32',
        'INTERVALDAY': 'string' if pd.__version__ >= '1' else 'object',
        'INTERVALYEAR': 'string' if pd.__version__ >= '1' else 'object',
        'SMALLINT': 'Int32',
        'TIME': 'timedelta64[ns]',
        'TIMESTAMP': 'datetime64[ns]',
        'VARDECIMAL': 'object',
        'VARCHAR' : 'string' if pd.__version__ >= '1' else 'object'
        } if PANDAS_AVAILABLE else None


class Result(object):
    def __init__(self, response, data, duration, *args, **kwargs):
        self.response = response
        self.duration = duration
        self.data = data


class ResultQuery(Result):
    """
    Class responsible for maintaining information returned from Drill.

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
            return pd.DataFrame.from_dict(self.rows, dtype=dtype)[self.columns]

        df = pd.DataFrame.from_dict(self.rows)[self.columns]

        # The columns in df all have a dtype of object because Drill's HTTP API
        # always quotes the values in the JSON it returns, thereby providing
        # DataFrame.from_dict(...) with a dict of strings.  We now use the
        # metadata returned by Drill to correct this
        for i in range(len(self.columns)):
            col_name = self.columns[i]
            # strip any precision information that might be in the metdata e.g. VARCHAR(10)
            col_drill_type = re.sub(r'\(.*\)', '', self.metadata[i])

            if col_drill_type not in DRILL_PANDAS_TYPE_MAP:
                logger.warn('No known mapping of Drill column {} of type {} to a Pandas dtype'.format(col_name, m))
            else:
                col_dtype = DRILL_PANDAS_TYPE_MAP[col_drill_type]
                logger.debug('Mapping column {} of Drill type {} to dtype {}'.format(col_name, col_drill_type, col_dtype))

                # Pandas < 1.0.0 cannot handle null ints so we sometimes cannot cast to an int dtype
                can_cast = True

                if col_name == 'BIT':
                    df[col_name] = df[col_name] == 'true'
                elif col_name == 'TIME': # col_name in ['TIME', 'INTERVAL']: # parsing of ISO-8601 intervals appears broken as of Pandas 1.0.3
                    df[col_name] = pd.to_timedelta(df[col_name])
                elif col_name in ['FLOAT4', 'FLOAT8']:
                    df[col_name] = pd.to_numeric(df[col_name])
                elif col_name in ['BIGINT', 'INT', 'SMALLINT']:
                    df[col_name] = pd.to_numeric(df[col_name])
                    if pd.__version__ < '1' and df[col_name].isnull().values.any():
                        logger.warn('Column {} of Drill type {} contains nulls so cannot be converted to an integer dtype in Pandas < 1.0.0'.format(col_name, col_drill_type))
                        can_cast = False

                if can_cast:
                    df[col_name] = df[col_name].astype(col_dtype)

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
