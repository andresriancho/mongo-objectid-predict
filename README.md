## Mongo ObjectId introduction

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

A potentially vulnerable REST API will look like this:

```http
GET /pet/5ae9b90a2c144b9def01ec37 HTTP/1.1
Host: vulnerable.com
X-API-Key: ...
```

And the code that handles that request (notice the lack of authorization):

```python
@route('/pet/{id}')
@is_authenticated
def handle_get_pet(id):
    return PetFromMongoORM.get(id)
```

## Predicting Mongo ObjectIds

The tool I created will predict Mongo ObjectIds given a valid initial value:

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

## Controlling the prediction process

There are two command line parameters which will control how many potential mongo
ObjectIds are generated: `--counter-diff` and `--per-counter`.

Counter diff will control the iteration over the last 3 bytes (the counter) of the
ObjectId. So, if the last 3 bytes from the base ObjectId were `000020`, you can control
how much to increment or decrement this value using `--counter-diff`. By default we set
it to `20`.

Per counter will control the first 4 bytes of the ObjectId: the epoch time. For each
newly generated counter (last 3 bytes) the tool will generate N `--per-counter` epoch
times.

It is important to know that ObjectIds are generated for all MongoDB tables: the counter
will be incremented for objects which are not the one queried by the application. This
means that depending on the way the application was developed, its load, etc. you might
need to play with `--counter-diff` and `--per-counter` until something interesting is
found.

The last parameter you can use is `--backward`. Instead of adding to the counter the tool
will decrease it. The same thing happens with the epoch counter.