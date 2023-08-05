mongo-mq
===========

Simple job queue using mongodb


Usage
=====

A queue can be instantiated with a mongo collection and a consumer
identifier. The consumer identifier helps distinguish multiple queue
consumers that are taking jobs from the queue::

  >> from pymongo import MongoClient
  >> from mongomq import MongoQueue
  >> queue = MongoQueue(
  ...   MongoClient().test.doctest_queu,
  ...   consumer_id="consumer-1",
  ...   timeout=300,
  ...   max_attempts=3,
  ...   ttl=18000)

You can set ttl in seconds, after this time the job will be delete
from database (default 5 hours)

New jobs/items can be placed in the queue by passing a dictionary::

  >> queue.put({"foobar": 1})

A job ``priority`` key and integer value can be specified in the
dictionary which will cause the job to be processed before lower
priority items::

  >> queue.put({"foobar": 0}, priority=1})

An item can be fetched out by calling the ``next`` method on a queue.
This returns a Job object::

  >> job = queue.next()
  >> job.payload
  {"foobar": 1}
  >> job.status
  'started'


Inspired By
===========

- [0] https://github.com/kapilt/mongoqueue


Running Tests
=============

Unit tests can be run with

 $ python setup.py nosetests


Credits
=======

Zaytsev Dmitriy, maintainer
