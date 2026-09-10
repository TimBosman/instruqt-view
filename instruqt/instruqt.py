#!/bin/python
from . import authentication, queries
import requests

class Instruqt:
    def __init__(self, team, conf_file="~/.config/instruqt/credentials"):
        self.api_key = authentication.read_api_key(conf_file)
        self.variables = {"teamSlug": team}

    def __reauthenticate(self):
        authentication.reroll_api_key()
        self.api_key = authentication.read_api_key()

    def request(self, body, url="https://play.instruqt.com/graphql", **kwargs):
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(url, headers=headers, json=body, **kwargs)
        if response.status_code != 200:
            self.__reauthenticate()
            headers["Authorization"] = f"Bearer {self.api_key}"
            response = requests.post(url, headers=headers, json=body, **kwargs)
            if response.status_code != 200:
                raise Exception(f"Request failed with status code {response.status_code}")
        return response.json()

    def get_invites(self, include_expired=False, include_upcoming=True):
        statuses = ["active"]
        if include_upcoming: statuses.append("upcoming")
        if include_expired: statuses.append("expired")
        body = {
            "query": queries.GET_INVITES,
            "variables": {
                **self.variables,
                "filters": {"statuses": statuses},
            }
        }
        return self.request(body).get("data").get("trackInvitesV2").get("items")
