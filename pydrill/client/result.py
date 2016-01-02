# -*- coding: utf-8 -*-


class ResultQuery(object):
    """
    Class responsible for maintaining a information returned from Drill.

    It is iterable.
    """
    # TODO: create better docs.

    def __init__(self, response, data, duration):
        self.response = response
        self.duration = duration
        self.data = data
        self.rows = data.get('rows', [])
        self.columns = data.get('columns', [])

    def __iter__(self):
        for row in self.rows:
            yield row
