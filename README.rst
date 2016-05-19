===============================
pydrill
===============================

.. image:: https://img.shields.io/travis/PythonicNinja/pydrill.svg
        :target: https://travis-ci.org/PythonicNinja/pydrill

.. image:: https://img.shields.io/pypi/v/pydrill.svg
        :target: https://pypi.python.org/pypi/pydrill

.. image:: https://readthedocs.org/projects/pydrill/badge/?version=latest
        :target: https://readthedocs.org/projects/pydrill/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/PythonicNinja/pydrill/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/PythonicNinja/pydrill?branch=master


Python Driver for `Apache Drill <https://drill.apache.org/>`_.

*Schema-free SQL Query Engine for Hadoop, NoSQL and Cloud Storage*

* Free software: MIT license
* Documentation: https://pydrill.readthedocs.org.

Features
--------

* Python 2/3 compatibility,
* Support for all rest API calls inluding profiles/options/metrics `docs with full list <http://pydrill.readthedocs.io/en/latest/readme.html#supported-api-calls>`_.
* Mapping Results to internal python types,
* Compatibility with Pandas data frame,

Installation
------------
::

Version from https://pypi.python.org/pypi/pydrill::

    $ pip install pydrill

Latest version from git::

    $ pip install git+git://github.com/PythonicNinja/pydrill.git

Sample usage
------------
::

    from pydrill.client import PyDrill

    drill = PyDrill(host='localhost', port=8047)

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    yelp_reviews = drill.query('''
      SELECT * FROM
      `dfs.root`.`./Users/macbookair/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json`
      LIMIT 5
    ''')

    for result in yelp_reviews:
        print("%s: %s" %(result['type'], result['date']))


    # pandas dataframe

    df = yelp_reviews.to_dataframe()
    print(df[df['stars'] > 3])
