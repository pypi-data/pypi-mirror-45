# lcu_connectorpy
A Python implementaion of [this](https://github.com/Pupix/lcu-connector) library.

## Download

Via pip:

```sh
pip install lcu-connectorpy
```

## Usage
```py
from lcu_connectorpy import Connector

conn = Connector()
conn.start()

print(conn.url, conn.auth, sep='\n')

>>> https://127.0.0.1:18633
>>> ("riot", "H9y4kOYVkmjWu_5mVIg1qQ")
```

See the [docs](https://zer0897.github.io/lcu_connectorpy/lcu_connectorpy/index.html) for more.
