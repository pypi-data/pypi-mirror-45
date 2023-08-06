# pygrocy
[![Build Status](https://travis-ci.com/SebRut/python-qbo.svg?branch=master)](https://travis-ci.com/SebRut/python-qbo)
[![PyPI](https://img.shields.io/pypi/v/python-qbo.svg)](https://pypi.org/project/python-qbo/)
[![CodeFactor](https://www.codefactor.io/repository/github/sebrut/python-qbo/badge)](https://www.codefactor.io/repository/github/sebrut/python-qbo)

## Installation

`pip install python-qbo`

## Usage
Import the package: 
```python
from qbo import Qbo
```

Obtain a qbo instance:
```python
qbo = Qbo("https://{QBO_URL}/")
```

Get the name of the machine:
```python
print(qbo.name())
```

Get maintenance status:

```python
print(qbo.maintenance_status())
```