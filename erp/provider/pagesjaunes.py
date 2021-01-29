import os
import requests


BASE_URL = "https://api.pagesjaunes.fr"


def get_auth_token():
    client_id = os.environ.get("PAGESJAUNES_API_CLIENT_KEY")
    client_secret = os.environ.get("PAGESJAUNES_API_SECRET_KEY")
    if not client_id or not client_secret:
        raise RuntimeError("No valid pagesjaunes API credentials available")
    res = requests.post(
        f"{BASE_URL}/oauth/client_credential/accesstoken",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    json = res.json()
    return json["access_token"]


def search(what, where):
    try:
        auth_token = get_auth_token()
        print("auth_token", auth_token)
        res = requests.get(
            f"{BASE_URL}/v1/pros/search",
            headers={"Authorization": f"Bearer {auth_token}"},
            params={
                "what": what,
                "where": where,
            },
        )
        json = res.json()
        print(json)
    except requests.exceptions.RequestException as err:
        raise RuntimeError(f"pagesjaunes api error: {err}")
