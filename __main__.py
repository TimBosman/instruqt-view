#!/bin/python

import argparse
from instruqt import instruqt
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


def run_cli():
    connection = instruqt.Instruqt(team="elastic-ilt")
    invites = connection.get_invites()
    rows = [[invite.get("publicTitle"), invite.get("expiresAt"), invite.get("status"), len(invite.get("contentEdges"))] for invite in invites]
    print(tabulate(rows, headers=["Public Title", "Expires At", "Status", "Number of tracks"], showindex=True))
    selected_invite = select_invite(len(invites) - 1)
    invite_id = invites[selected_invite].get("id")
    activities = connection.get_activity_report(invite_id).get("plays")
    rows = [[a.get("user").get("profile").get("display_name"), a.get("time_spent"), a.get("track").get("slug"), a.get("completed_challenges"), a.get("total_challenges")] for a in activities]
    print(tabulate(rows, headers=["Display Name", "Time Spent", "Track Title", "Completed Challenges", "Total Challenges"], showindex=True))


def run_ui():
    from flask import Flask, render_template

    app = Flask(__name__, template_folder="templates", static_folder="static")
    connection = instruqt.Instruqt(team="elastic-ilt")

    @app.template_filter("format_duration")
    def format_duration(seconds):
        if not seconds:
            return "—"
        seconds = int(seconds)
        h, m = divmod(seconds // 60, 60)
        return f"{h}h {m}m" if h else f"{m}m"

    @app.route("/")
    def index():
        invites = connection.get_invites()
        return render_template("invites.html", invites=invites, active_page="invites")

    @app.route("/activities/<invite_id>")
    def activities(invite_id):
        invites = connection.get_invites()
        invite = next((inv for inv in invites if inv.get("id") == invite_id), None)
        title = invite.get("publicTitle") if invite else invite_id
        plays = connection.get_activity_report(invite_id).get("plays")
        return render_template("activities.html", title=title, activities=plays, active_page="invites")

    app.run(debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instruqt View")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ui", action="store_true", help="Launch the Flask web UI")
    group.add_argument("--cli", action="store_true", help="Run in CLI mode (default)")
    args = parser.parse_args()

    if args.ui:
        run_ui()
    else:
        run_cli()
