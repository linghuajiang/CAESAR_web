
"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage
from hirespy.serv.database import get_db
from datetime import datetime

DB_LOCK = hirespy.app.config['DB_LOCK']


@hirespy.app.route('/api/v1/stats/<type>/', methods=["POST"])
def stats_post(type):
    """Return available resources."""
    if type not in ["guest", "attr", "view"]:
        return
    context = {}
    conn = get_db()
    DB_LOCK.acquire()
    conn.execute(
        "UPDATE stats "
        "SET count = count + 1 "
        "WHERE name = ?",
        (type,)
    )
    conn.execute(
        "INSERT INTO ips (ip, type, time) "
        "VALUES (?, ?, ?)",
        (flask.request.remote_addr, type, datetime.now(),)
    )
    conn.commit()
    DB_LOCK.release()
    return flask.jsonify(**context)

@hirespy.app.route('/api/v1/stats/', methods=["GET"])
def stats_get():
    """Return available resources."""
    context = {
        "guest":0,
        "view":0
    }
    conn = get_db()
    DB_LOCK.acquire()
    context["view"] = conn.execute(
        "SELECT name, count "
        "FROM stats "
        "WHERE name = ?",
        ("view",)
    ).fetchone()['count']
    context["guest"] = conn.execute(
        "SELECT name, count "
        "FROM stats "
        "WHERE name = ?",
        ("guest",)
    ).fetchone()['count']
    context["attr"] = conn.execute(
        "SELECT name, count "
        "FROM stats "
        "WHERE name = ?",
        ("attr",)
    ).fetchone()['count']
    DB_LOCK.release()
    return flask.jsonify(**context)

@hirespy.app.route('/api/v1/plot/', methods=["GET"])
def stats_plot():
    """Return available resources."""
    context = {
        "dates":[],
        "guests":[],
        "views":[],
        "attrs":[]
    }
    conn = get_db()
    DB_LOCK.acquire()
    ips = conn.execute(
        "SELECT * "
        "FROM ips "
    ).fetchall()
    DB_LOCK.release()
    stats = {}
    for ip in ips:
        date = ip["time"][5:10]
        stats[date] = stats.get(date, {'guest':0, 'view':0, 'attr':0})
        stats[date][ip["type"]] += 1
    context['dates'] = list(stats.keys())
    context['dates'].sort()
    context['guests'] = [stats[date]['guest'] for date in stats]
    context['views'] = [stats[date]['view'] for date in stats]
    context['attrs'] = [stats[date]['attr'] for date in stats]

    return flask.jsonify(**context)