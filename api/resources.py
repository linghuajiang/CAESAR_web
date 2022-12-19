
"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage


@hirespy.app.route('/api/v1/', methods=["GET"])
def get_resources():
    """Return available resources."""
    # check login
    # if "username" not in flask.session:
    #     raise InvalidUsage(403)
    # in session
    context = {
        "datasets": "{}datasets/".format(flask.request.path),
        "url": flask.request.path
    }
    return flask.jsonify(**context)
