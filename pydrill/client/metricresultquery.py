# -*- coding: utf-8 -*-


class MetricResultQuery(object):
    """
    Class responsible for maintaining a information returned from Drill.

    Returns a query object containing the raw data from Drill as well as individual
    fields.

    Current fields returned:
    1.  Number of Drill Bits
    2.  Bit #0
    3.  Data Port Address
    4.  User Port Address
    5.  Control Port Address
    6.  Maximum Direct Memory

    """
    # TODO: create better docs.

    def __init__(self, response, data, duration):
        self.response = response
        self.duration = duration
        self.data = data
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

    def __iter__(self):
        return self.data.__iter__()
