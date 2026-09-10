#!/bin/python

import argparse
from instruqt import instruqt
from tabulate import tabulate


def aggregate_plays(plays):
    users = {}
    for play in plays:
        if play.get("user", {}).get("is_anonymous"):
            continue
        profile = play.get("user", {}).get("profile", {})
        email = (profile.get("email") or "").strip()
        if not email:
            continue
        if email not in users:
            users[email] = {
                "name": (profile.get("display_name") or "").strip() or email,
                "email": email,
                "total_time": 0,
                "last_activity_at": "",
                "tracks": {},
            }
        try:
            users[email]["total_time"] += int(play.get("time_spent") or 0)
        except (ValueError, TypeError):
            pass
        last_act = str(play.get("last_activity") or "")
        if last_act > users[email]["last_activity_at"]:
            users[email]["last_activity_at"] = last_act
        slug = ((play.get("track") or {}).get("slug") or "").strip()
        if not slug:
            continue
        completed_at = str(play.get("track_completed_at") or "").strip()
        completed = bool(completed_at)
        try:
            done = int(play.get("completed_challenges") or 0)
            total = int(play.get("total_challenges") or 0)
        except (ValueError, TypeError):
            done, total = 0, 0
        existing = users[email]["tracks"].get(slug)
        if existing is None:
            users[email]["tracks"][slug] = {
                "completed": completed,
                "completed_challenges": done,
                "total_challenges": total,
                "completed_at": completed_at,
            }
        else:
            if completed:
                existing["completed"] = True
                existing["completed_challenges"] = done
                existing["total_challenges"] = total
                if completed_at > existing["completed_at"]:
                    existing["completed_at"] = completed_at
            elif not existing["completed"] and done > existing["completed_challenges"]:
                existing["completed_challenges"] = done
                existing["total_challenges"] = total
    return users


def _completed_count(user):
    return sum(1 for t in user["tracks"].values() if t["completed"])


def _last_completed_track(user):
    best_slug, best_date = "", ""
    for slug, t in user["tracks"].items():
        if t["completed"] and t["completed_at"] > best_date:
            best_slug, best_date = slug, t["completed_at"]
    return best_slug or "—"


def _progress_icon(count, avg_rounded):
    if count > avg_rounded:
        return "🚀"
    if count < avg_rounded:
        return "🏎️💨"
    return "✅"


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
        if h and m:
            return f"{h}h {m:02d}m"
        return f"{h}h" if h else f"{m}m"

    @app.template_filter("format_datetime")
    def format_datetime(dt_str):
        if not dt_str:
            return "—"
        s = str(dt_str).replace("T", " ")
        return s[:16] if len(s) >= 16 else s

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

        users = aggregate_plays(plays)
        total_students = len(users)

        track_completions = {}
        for u in users.values():
            for slug, t in u["tracks"].items():
                track_completions.setdefault(slug, 0)
                if t["completed"]:
                    track_completions[slug] += 1

        track_summary = [
            {
                "slug": slug,
                "completed": count,
                "pct": f"{count / total_students * 100:.0f}%" if total_students else "0%",
            }
            for slug, count in sorted(track_completions.items())
        ]

        tracks_avg = sum(_completed_count(u) for u in users.values()) / total_students if total_students else 0
        avg_rounded = round(tracks_avg)

        user_rows = [
            {
                **u,
                "completed_count": _completed_count(u),
                "last_completed": _last_completed_track(u),
                "status_icon": _progress_icon(_completed_count(u), avg_rounded),
            }
            for u in sorted(users.values(), key=lambda x: x["name"].lower())
        ]

        return render_template(
            "activities.html",
            title=title,
            user_rows=user_rows,
            track_summary=track_summary,
            tracks_avg=f"{tracks_avg:.1f}",
            total_students=total_students,
            active_page="invites",
        )

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
