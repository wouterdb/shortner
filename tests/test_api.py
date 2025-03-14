import requests
import inmanta_plugins.shortner
import urllib.parse


def test_create_list_delete(test_url: str, shlink_url:str, api_key: str) -> None:
    # list
    url = urllib.parse.urljoin(shlink_url, "rest/v3/short-urls")
    headers = {"Accept": "application/json", "X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("list", response.json())


    #create
    url = urllib.parse.urljoin(shlink_url, "rest/v3/short-urls")
    headers = {"Accept": "application/json", "X-Api-Key": api_key}
    body={
        "longUrl": test_url,
        "findIfExists": True,
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    created = response.json()
    print("create", response.json())

    # Find
    url = urllib.parse.urljoin(shlink_url, "rest/v3/short-urls")
    headers = {"Accept": "application/json", "X-Api-Key": api_key}
    # this matches sub strings, so needs another filter to prevent confusing
    # it.co and it.com
    body = {"searchTerm":test_url}
    response = requests.get(url, headers=headers, params=body)
    response.raise_for_status()
    print("find", response.json())

    # delete
    short_code = created["shortCode"]
    url = urllib.parse.urljoin(shlink_url, f"rest/v3/short-urls/{short_code}")
    headers = {"Accept": "application/json", "X-Api-Key": api_key}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()

