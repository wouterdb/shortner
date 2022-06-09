# shortner Module

A small demo module to explain module development by making a URL shortner service

```
import shortner

shortner::ShortUrl(
    long_url="https://inmanta.com/",
    api_key="{api_key}",
)
```

## Running tests

1. Obtain a [rebrandly API key](https://developers.rebrandly.com/docs/api-key-authentication)
1. Setup a virtual env 

```bash
mkvirtualenv inmanta-test -p python3
pip install -r requirements.dev.txt
pip install -r requirements.txt

mkdir /tmp/env
export INMANTA_TEST_ENV=/tmp/env
export INMANTA_MODULE_REPO=git@github.com:inmanta/
export REBRANDLY_KEY=[PUT YOUR KEY HERE]
```

2. Run tests

```bash
pytest tests
```
