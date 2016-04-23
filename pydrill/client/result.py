# -*- coding: utf-8 -*-


class ResultQuery(object):
    """
    Class responsible for maintaining a information returned from Drill.

    It is iterable.
    """
    # TODO: create better docs.

    def __init__(self, response, data, duration, metric=False):
        self.response = response
        self.duration = duration
        self.data = data

        if metric == True:
            self.keys = {}
            self.values = {}

            for metric in data:
                self.keys[ metric['name'] ] = metric['name']
                self.values[ metric['value'] ] = metric['value']

            self.number_of_drill_bits = data[0]['value']
            self.bit_0 = data[1]['value']
            self.data_port_address = data[2]['value']
            self.user_port_address = data[3]['value']
            self.control_port_address = data[4]['value']
            self.max_direct_memory = data[5]['value']
            self.rows = data

        else:
            self.rows = data.get('rows', [])
            self.columns = data.get('columns', [])

    def __iter__(self):
        for row in self.rows:
            yield row

