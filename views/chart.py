"""
Hirespy console view.

URLs include:
/chart/
"""
import logging
import json
import flask
import hirespy
from hirespy.serv.database import get_db

DB_LOCK = hirespy.app.config['DB_LOCK']

@hirespy.app.route('/chart/', methods=['GET', 'POST'])
def chart():
    """Display / route."""
    # Add database info to context
    
    context = {
        "datasets": [],
        "region": "",
        "entered": False,
        "result": "Details will be shown here...",
        "userid": "",
        "port": "",
    }
    """
    conn = get_db()
    DB_LOCK.acquire()
    context["datasets"] = conn.execute(
        "SELECT id, name, path "
        "FROM datasets ",
    ).fetchall()
    DB_LOCK.release()

    # POST handler
    if flask.request.method == 'POST':
        if flask.request.content_length > 1024:
            flask.abort(413)
            return 1
        region = flask.request.form.get("region")
        d_type = flask.request.form.get("type")
        if not region:
            context["region"] = "Cannot be empty"
            return flask.render_template("index.html", **context)
        LOGGER.warning("Receiving type data: %s %s", d_type, region)
        nport, nid = MANAGER.add(region)
        context["region"] = region
        context["entered"] = True
        context["userid"] = str(nid)
        context["port"] = str(nport)
    """
    return flask.render_template("chart.html", **context)
