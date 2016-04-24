# -*- coding: utf-8 -*-


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

    def __iter__(self):
        for row in self.rows:
            yield row


class Drillbit(object):
    def __init__(self, id, address, status, *args, **kwargs):
        self.id = id
        self.address = address
        self.status = status

    def __repr__(self):
        return u"#{} - {} ({})".format(self.id, self.address, self.status)


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
