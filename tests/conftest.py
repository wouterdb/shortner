import os

import pytest

import inmanta_plugins.shortner


@pytest.fixture
def api_key() -> str:
    return os.environ["SHLINK_KEY"]

@pytest.fixture
def shlink_url() -> str:
    return os.environ["SHLINK_URL"]



@pytest.fixture
def test_url() -> str:
    """The url to use in testing, will be cleaned up"""
    return "https://inmanta.com/"


@pytest.fixture
def rebrandly(api_key, test_url) -> inmanta_plugins.shortner.RebrandlyClient:
    client = inmanta_plugins.shortner.RebrandlyClient(api_key=api_key)
    existing = client.find_instance_for(test_url)
    if existing:
        print("Link found, deleting")
        client.delete_instance(existing["id"])
    
    return client