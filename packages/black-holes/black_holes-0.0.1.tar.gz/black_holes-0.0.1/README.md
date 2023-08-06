BlackHoles
---

Black Holes is a simple way to handle your projects secrets using a `database` or `Consul.io`.


+ [Installing BlackHoles](#install)
+ [Using BlackHoles](#usage)
    - [Plain Keys](#simple-usage)
    - [Encrypted Keys](#advanced-usage)
    
# Install

Installing from `Pip`

```bash
(pyenv) $ pip install blackhole
```
    

Installing from `sources`:

```bash
(pyenv) $ cd black_holes
(pyenv) $ python setup.py install
```

# Usage:

## simple usage

Plain `{'key': 'values'}` storage.

```python
from black_hole import SqliteBlackHole

# Create a new SqliteBlackHole instance
near_black_hole = SqliteBlackHole()

# Create a key called "key" with value "value"
near_black_hole.key = 'value'

# print key
print(near_black_hole.key)
```

##  Advanced usage:

Encrypted `{'key': 'values'}` storage.

```python
from black_hole import SqliteBlackHole

# Create a new SqliteBlackHole instance
near_black_hole = SqliteBlackHole()

# Encrypted key
near_black_hole.encrypted_key = 'it is a secret'

# Encrypted value
print(near_black_hole.key)

# Decrypted value
print(near_black_hole.decrypted_key)
```


_Made it with ❤ by __DTecDeal___