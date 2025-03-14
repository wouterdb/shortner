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
def shlink(api_key, shlink_url, test_url) -> inmanta_plugins.shortner.ShlinkClient:
    client = inmanta_plugins.shortner.ShlinkClient(
        api_key=api_key, server_url=shlink_url
    )
    existing = client.find_instance_for(test_url)
    if existing:
        print("Link found, deleting")
        client.delete_instance(existing["shortCode"])

    return client
