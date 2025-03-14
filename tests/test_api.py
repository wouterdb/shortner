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
    # Test the ShlinkClient!

    # check if the test url is already shortned on this server
    # and make sure this is not so
    

    # create a short link towards the test url
    

    # check if the test url is already shortned on this server
    # and make sure this is so
    

    # delete the link we created

    
    # check if the test url is already shortned on this server
    # and make sure this is not so