#!/bin/python

from instruqt import instruqt
import json

if __name__ == "__main__":
    connection = instruqt.Instruqt(team="elastic-ilt")
    invites = connection.get_invites()
    for invite in invites:
        print(invite.get("publicTitle"))

