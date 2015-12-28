===============================
pydrill
===============================

.. image:: https://img.shields.io/pypi/v/pydrill.svg
        :target: https://pypi.python.org/pypi/pydrill

.. image:: https://img.shields.io/travis/PythonicNinja/pydrill.svg
        :target: https://travis-ci.org/PythonicNinja/pydrill

.. image:: https://readthedocs.org/projects/pydrill/badge/?version=latest
        :target: https://readthedocs.org/projects/pydrill/?badge=latest
        :alt: Documentation Status


Python Driver for `Apache Drill <https://drill.apache.org/>`_.

*Schema-free SQL Query Engine for Hadoop, NoSQL and Cloud Storage*

* Free software: MIT license
* Documentation: https://pydrill.readthedocs.org.

Features
--------

* Python 2/3 compatibility,
* Mapping Results to internal python types,
* Compatibility with Pandas data frame,

Sample usage
------------
::

    from pydrill.client import PyDrill
    
    drill = PyDrill(host='localhost', port=8047)
    
    print drill.is_active()
    
    yelp_reviews = drill.query('''
      SELECT * FROM
      `dfs.root`.`./Users/macbookair/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json`
      LIMIT 5
    ''')
    
    for result in yelp_reviews:
        print result['type'], result['date']
