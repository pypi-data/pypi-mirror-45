# RegonAPI

> Python 3 API Client for Polish [REGON database](https://api.stat.gov.pl/Home/RegonApi)


![GitHub](https://img.shields.io/github/license/rolzwy7/RegonAPI.svg?color=black&style=flat-square)

---
<p align="center">
  <img src="https://rolzwy7.github.io/cdn/projects/RegonAPI/example_001.gif" alt="RegonAPI example"/>
</p>

## Table of Contents

- [Usage example](#usage-example)
<!-- - [Installation](#installation)
- [Features](#features)
- [Tests](#dependencies)
- [Documentation](#documentation)
- [FAQ](#faq) -->

---

## Usage example

```python
from RegonAPI import RegonAPI

# Regon API - WSDL file
WSDL = "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl.xsd"
# Regon API - Service URL
SERVICE_URL = "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc"
# Regon API - test key
API_KEY = "abcde12345abcde12345"

api = RegonAPI(wsdl=WSDL, service_url=SERVICE_URL)
api.authenticate(key=API_KEY)

print("Data status:", api.get_data_status())
```

---

<!-- ## Installation

### Pip

```
python -m pip install RegonAPI
```

## Features

## Tests

```
python -m pytest -v RegonAPI/test
```

## FAQ -->
