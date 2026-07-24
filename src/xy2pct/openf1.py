from __future__ import annotations

import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from . import apicreds

TOKEN_URL = "https://api.openf1.org/token"
DEFAULT_TIMEOUT_SECONDS = 15


def _get_access_token() -> str:
    payload = urlencode(
        {
            "username": apicreds.username,
            "password": apicreds.password,
        }
    ).encode("utf-8")
    request = Request(
        TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
        token_data = json.loads(response.read().decode("utf-8"))

    access_token = token_data.get("access_token")
    if not access_token:
        raise RuntimeError("OpenF1 token response did not contain an access token")

    apicreds.updateToken(access_token)
    return access_token


def _open_authenticated(url: str, access_token: str):
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    return urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS)


def get_json(url: str):
    """Fetch an OpenF1 endpoint using the cached credentials-backed token."""
    access_token = apicreds.token or _get_access_token()

    try:
        response = _open_authenticated(url, access_token)
    except HTTPError as exc:
        if exc.code != 401:
            raise
        response = _open_authenticated(url, _get_access_token())

    with response:
        return json.loads(response.read().decode("utf-8"))
