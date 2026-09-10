#!/bin/python

from instruqt import instruqt
import json
from tabulate import tabulate

def select_invite(max_int):
    invite_index = input("Select an invite by its index: ")
    if not invite_index.isdigit():
        print("Invalid input. Please enter an integer.")
        invite_index = select_invite(max_int)
    if int(invite_index) > max_int:
        print(f"Invalid input. Please enter an integer between 0 and {max_int}.")
        invite_index = select_invite(max_int)
    return int(invite_index)

if __name__ == "__main__":
    connection = instruqt.Instruqt(team="elastic-ilt")
    invites = connection.get_invites()
    test = [[invite.get("publicTitle"), invite.get("expiresAt"), invite.get("status"), len(invite.get("contentEdges"))] for invite in invites]
    print(tabulate(test, headers=["Public Title", "Expires At", "Status", "Number of tracks"], showindex=True))
    selected_invite = select_invite(len(invites) - 1)
    invite_id = invites[selected_invite].get("id")
    print(connection.get_activity_report(invite_id))
