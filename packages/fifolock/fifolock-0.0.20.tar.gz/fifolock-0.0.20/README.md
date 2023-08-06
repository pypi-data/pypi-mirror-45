# fifolock [![CircleCI](https://circleci.com/gh/michalc/fifolock.svg?style=svg)](https://circleci.com/gh/michalc/fifolock) [![Maintainability](https://api.codeclimate.com/v1/badges/9f7c8caf9b66ad2175e4/maintainability)](https://codeclimate.com/github/michalc/fifolock/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/9f7c8caf9b66ad2175e4/test_coverage)](https://codeclimate.com/github/michalc/fifolock/test_coverage)

A flexible low-level tool to make synchronisation primitives in asyncio Python. As the name suggests, locks are granted strictly in the order requested: first-in-first-out; and are not reentrant.


## Installation

```bash
pip install fifolock
```


## Recipes

### Mutex (exclusive) lock

```python
import asyncio
from fifolock import FifoLock


class Mutex(asyncio.Future):
    @staticmethod
    def is_compatible(holds):
        return not holds[Mutex]


lock = FifoLock()

async def access():
    async with lock(Mutex):
        # access resource
```

### Read/write (shared/exclusive) lock

```python
import asyncio
from fifolock import FifoLock


class Read(asyncio.Future):
    @staticmethod
    def is_compatible(holds):
        return not holds[Write]

class Write(asyncio.Future):
    @staticmethod
    def is_compatible(holds):
        return not holds[Read] and not holds[Write]


lock = FifoLock()

async def read():
    async with lock(Read):
        # shared access

async def write():
    async with lock(Write):
        # exclusive access
```

### Semaphore

```python
import asyncio
from fifolock import FifoLock


class SemaphoreBase(asyncio.Future):
    @classmethod
    def is_compatible(cls, holds):
        return holds[cls] < cls.size


lock = FifoLock()
Semaphore = type('Semaphore', (SemaphoreBase, ), {'size': 3})

async def access():
    async with lock(Semaphore):
        # at most 3 concurrent accesses
```


## Running tests

```bash
python setup.py test
```


## Design choices

Each mode of the lock is a subclass of `asyncio.Future`. This could be seen as a leak some of the internals of `FifoLock`, but it allows for clear client and internal code.

- Classes are hashable, so each can be a key in the `holds` dictionary passed to the `is_compatible` method. This allows the compatibility conditions to be read clearly in the client code, and the `holds` dictionary to be mutated clearly internally.

- An instance of it, created inside `FifoLock`, is _both_ the object awaited upon, and stored in a deque with a way of accessing its `is_compatible` method.

- The fact it's a class and not an instance of a class also makes clear it is to store no state, merely configuration.

A downside is that for configurable modes, such as for a semaphore, the client must dynamically create a class: this is not a frequently-used pattern.

The fact that the lock is _not_ reentrant is deliberate: the class of algorithms this is designed for does not require this. This would add unnecessary complexity, and presumably be slower.
