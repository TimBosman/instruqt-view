#!/bin/python
from . import authentication
import requests

class Instruqt:
    def __init__(self, team, conf_file="~/.config/instruqt/credentials"):
        self.api_key = authentication.read_api_key(conf_file)
        self.variables = {"teamSlug": team}

    def request(self, body, url="https://play.instruqt.com/graphql", **kwargs):
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        return requests.post(url, headers=headers, json=body, **kwargs).json()

    def get_invites(self, include_expired=False, include_upcoming=True):
        body = {
            "query": """query TrackInvitesTableInvitesV2($teamSlug: String!, $filters: InviteFilters) {
  trackInvitesV2(teamSlug: $teamSlug, filters: $filters) {
    items {
      id shareMethod publicTitle title
      contentEdges { id type index refID node {
        ... on Track { id title __typename }
        ... on Lab { id title: name refs { id name type __typename } __typename }
        __typename
      } __typename }
      inviteLimit claimCount expiresAt created playLimit type status startsAt
      authors { id user { id profile { avatar display_name __typename } __typename } __typename }
      __typename
    }
    totalItems __typename
  }
  team(teamSlug: $teamSlug) {
    id features { hot_start invite_level_hot_starts instructor_track_invite_creation __typename } __typename
  }
}""",
        }
        body["variables"] = {
            **self.variables,
            "filters": {"statuses": (
                ["active", "upcoming", "expired"] if include_expired and include_upcoming
                else ["active", "upcoming"] if include_upcoming
                else ["active", "expired"] if include_expired
                else ["active"]
            )},
        }
        return self.request(body).get("data").get("trackInvitesV2").get("items")
