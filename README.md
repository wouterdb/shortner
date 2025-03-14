# shortner Module

A small demo module to explain module development by making a URL shortner service

```
import shortner


server = shortner::ShlinkServer(
    url = "{server_url}",
    api_key = "{api_key}",
)

shortner::ShortUrl(
    long_url = "www.example.com",
    server = server,
)
```

## Running tests

1. Set up a [shlink server](https://shlink.io/documentation/) and get an API token
1. Setup a virtual env 

```bash
mkvirtualenv inmanta-test -p python3
pip install -r requirements.dev.txt  -r requirements.txt -e .

mkdir /tmp/env
SHLINK_KEY=[API KEY HERE]
SHLINK_URL=http://127.0.0.1:8080/ # server url
```

2. Run tests

```bash
pytest tests
```
