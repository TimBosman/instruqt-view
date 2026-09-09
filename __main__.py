#!/bin/python

from instruqt import instruqt
import json
from tabulate import tabulate

if __name__ == "__main__":
    connection = instruqt.Instruqt(team="elastic-ilt")
    invites = connection.get_invites()
    print(invites)
    test = [[invite.get("publicTitle"), invite.get("expiresAt"), invite.get("status"), len(invite.get("contentEdges"))] for invite in invites]
    print(tabulate(test, headers=["Public Title", "Expires At", "Status", "Number of tracks"], showindex=True))

