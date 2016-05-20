=====
Usage
=====

To use pydrill in a project::

    from pydrill.client import PyDrill

    drill = PyDrill(host='localhost', port=8047)

You can also initialize via environment variables such as::

    PYDRILL_HOST
    PYDRILL_PORT



To enable specific storage plugin you can::

    drill.storage_enable('mongo')

You can view all queries which were executed or are running::

    drill.profiles()


To check if Drill is running::

    if drill.is_active():
        your_code


Query involves only providing sql::


    employees = drill.query('''
      SELECT * FROM cp.`employee.json` LIMIT 5
    ''')

    for employee in employees:
        print result

If you feel like building sql queries is not nicest thing ever you should try pydrill_dsl https://pypi.python.org/pypi/pydrill_dsl

Support for pandas::

    # pandas dataframe
    df = employees.to_dataframe()
    print(df[df['salary'] > 20000])

Supported api calls
-------------------
.. autoclass:: pydrill.client.PyDrill
    :members:
    :undoc-members:




