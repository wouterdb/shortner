import urllib.parse

import requests

import inmanta_plugins.shortner


def test_list(shlink_url: str, api_key: str) -> None:
    # Test list call
    url = urllib.parse.urljoin(shlink_url, "rest/v3/short-urls")
    headers = {"Accept": "application/json", "X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("list", response.json())
    assert response.json()


def test_get_create_delete(
    test_url: str, shlink: inmanta_plugins.shortner.ShlinkClient
) -> None:

    # get, expect none
    assert not shlink.find_instance_for(test_url)

    # create
    created = shlink.create(test_url)
    assert created

    # get, expect one
    assert shlink.find_instance_for(test_url)

    # delete
    short_code = created["shortCode"]
    shlink.delete_instance(short_code)
