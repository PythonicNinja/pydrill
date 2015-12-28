# pydrill 
Python Driver for [Apache Drill](https://drill.apache.org/).

> Schema-free SQL Query Engine for Hadoop, NoSQL and Cloud Storage

```python
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
```
