<div align="center">
    <img src="https://app.truverifi.com/img/truverifi-logo.png" width="250">
    <h4>Python client library for truverifi</h4>
</div>

<p align="center">
    <a href="https://travis-ci.org/achillesrasquinha/truverifi">
      <img src="https://img.shields.io/travis/achillesrasquinha/truverifi.svg?style=flat-square">
    </a>
    <a href="https://coveralls.io/github/achillesrasquinha/truverifi">
      <img src="https://img.shields.io/coveralls/github/achillesrasquinha/truverifi.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/truverifi/">
      <img src="https://img.shields.io/pypi/v/truverifi.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/truverifi/">
      <img src="https://img.shields.io/pypi/l/truverifi.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/pipupgrade/">
		  <img src="https://img.shields.io/pypi/pyversions/truverifi.svg?style=flat-square">
	  </a>
    <a href="https://git.io/boilpy">
      <img src="https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square">
    </a>
</p>

### Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

#### Installation

```shell
$ pip install truverifi
```

#### Usage

##### Application Interface

```python
>>> import truverifi
>>> client = truverifi.API("<YOUR_API_KEY>")
>>> client.account()
{
  "balance": 2,
  "username": "example@test.com",
  "transactions": [
    {
      "id": 69,
      "amount": -1,
      "timestamp": "2018-07-07T19:30:00Z",
      "description": "Number change to: 111-222-3333"
    }
  ]
}

>>> client.line()

>>> zip, services = 12345, ["FACEBOOK", "TWITTER"]
>>> client.checkService(services, zip)
>>> client.lineChangeService(services, zip)

>>> client.lineExtend()
```

#### License

This repository has been released under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using <a href="https://git.io/boilpy">boilpy</a>.
</div>