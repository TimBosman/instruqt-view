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

GET_ACTIVITY_REPORT = """query ActivityReportPage($teamSlug: String!, $inviteID: String!) {
  trackInvite(inviteID: $inviteID) {
    id
    type
    allowAnonymous
    allowedEmailAddressesOnly
    title
    publicTitle
    contentEdges {
      id
      __typename
    }
    claimsPage {
      totalItems
      items {
        id
        claimedAt
        playLimit
        playTTL
        user {
          id
          profile {
            display_name
            email
            __typename
          }
          details(teamSlug: $teamSlug) {
            firstName
            lastName
            email
            id
            companyName
            phoneNumber
            jobTitle
            jobLevel
            countryCode
            usState
            consent
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    plays {
      last_activity
      time_spent
      track_started_at
      track_completed_at
      completed_challenges
      total_challenges
      failed_challenge_attempts
      track {
        id
        slug
        __typename
      }
      participant {
        id
        __typename
      }
      user {
        id
        is_anonymous
        profile {
          email
          display_name
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}"""
