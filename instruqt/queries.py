#!/bin/python

GET_INVITES= """query TrackInvitesTableInvitesV2($teamSlug: String!, $filters: InviteFilters) {
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
}"""