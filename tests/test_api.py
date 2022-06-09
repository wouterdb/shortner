import requests


def test_create_list_delete(api_key: str):
    url = "https://api.rebrandly.com/v1/links"

    payload = {"destination": "https://inmana.com/"}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": api_key,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    link_id = response.json()["id"]


    url = "https://api.rebrandly.com/v1/links"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    assert link_id in [x["id"] for x in response.json()]


    url = f"https://api.rebrandly.com/v1/links/{link_id}"


    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }


    response = requests.delete(url, headers=headers)
    response.raise_for_status()

