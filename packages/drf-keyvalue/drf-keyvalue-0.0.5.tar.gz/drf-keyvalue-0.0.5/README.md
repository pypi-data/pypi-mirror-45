# drf-keyvalue

[![PyPI version](https://badge.fury.io/py/drf-keyvalue.svg)](https://badge.fury.io/py/drf-keyvalue)
![coverage](https://gitlab.com/gitlab-org/gitlab-ce/badges/master/coverage.svg?job=coverage)

> Store and retrieve data in a consistent way in a key-value store using Django Rest Framework serializers

## About

**Supported backends**

* Redis

## Installation

```
pip install drf-keyvalue
```

## Setup

**Add to settings.py **
```
INSTALLED_APPS = [
    'drf_keyvalue',
]
```

## Usage

For detailed usage, see the tests

```python

from drf_keyvalue.keyvalue import get_client
from .models import Todo, TodoSerializer
import redis
redis.StrictRedis(host='localhost', port=6379, db=0)
client = get_client('keyvalue.backends.RedisBackend', connection)
todo = Todo.objects.first()
client.set(TodoSerializer, todo)
client.get(todo)
client.delete(todo)
```

### Backend specifics:

#### `RedisBackend`

```python
import redis
connection = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client = get_client('drf_keyvalue.backends.RedisBackend', connection=connection)
```

# Development

## Updating pypi repo:

```shell
bumpversion patch # major, minor or patch
#push to gitlab:
git push origin master
```

