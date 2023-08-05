# sentry-falcon

[![Travis CI build status (Linux)](https://travis-ci.org/jmagnusson/sentry-falcon.svg?branch=master)](https://travis-ci.org/jmagnusson/sentry-falcon)
[![PyPI version](https://img.shields.io/pypi/v/sentry-falcon.svg)](https://pypi.python.org/pypi/sentry-falcon/)
[![License](https://img.shields.io/pypi/l/sentry-falcon.svg)](https://pypi.python.org/pypi/sentry-falcon/)
[![Available as wheel](https://img.shields.io/pypi/wheel/sentry-falcon.svg)](https://pypi.python.org/pypi/sentry-falcon/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/sentry-falcon.svg)](https://pypi.python.org/pypi/sentry-falcon/)
[![PyPI status (alpha/beta/stable)](https://img.shields.io/pypi/status/sentry-falcon.svg)](https://pypi.python.org/pypi/sentry-falcon/)
[![Coverage Status](https://coveralls.io/repos/github/jmagnusson/sentry-falcon/badge.svg?branch=master)](https://coveralls.io/github/jmagnusson/sentry-falcon?branch=master)

[Falcon web framework](https://falconframework.org/) integration for the [Sentry SDK](https://docs.sentry.io/error-reporting/quickstart/?platform=python).

## Installation

```
pip install sentry-falcon
```

## Setup

```python
import sentry_sdk
import sentry_falcon

sentry_sdk.init(
    '__DSN__',
    integrations=[sentry_falcon.FalconIntegration()],
)
```

## Known limitations

- JSON request body will only be captured if the `falcon.Request.media` attribute has been accessed before sending of the Sentry event.
- Raw request bodies are not captured (the Falcon request stream can only be read once)
- User information must be captured manually (for example via Falcon middleware)
