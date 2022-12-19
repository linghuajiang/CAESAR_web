
"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage
from hirespy.serv.database import get_db


DB_LOCK = hirespy.app.config['DB_LOCK']


@hirespy.app.route('/api/v1/tissueurl/<string:name>/', methods=["GET"])
def get_tissue_url(name):
    """Return available resources."""
    # check login
    # if "username" not in flask.session:
    #     raise InvalidUsage(403)
    # in session
    conn = get_db()
    DB_LOCK.acquire()
    url = conn.execute(
        "SELECT url "
        "FROM datasets "
        "WHERE name = ?",
        (name,)
    ).fetchone()['url']
    DB_LOCK.release()
    context = {
        "tissueurl": url,
        "url": flask.request.path
    }
    return flask.jsonify(**context)