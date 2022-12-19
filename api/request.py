
"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage
from hirespy.views.index import LOGGER, MANAGER


@hirespy.app.route('/api/v1/attribution/', methods=["POST"])
def attr_request():
    """Return available resources."""
    # check login
    # if "username" not in flask.session:
    #     raise InvalidUsage(403)
    # in session
    tissue_id = flask.request.get_json().get("type")
    region = flask.request.get_json().get("region")
    bg = flask.request.get_json().get("bg")
    LOGGER.warning("Receiving type data: %s %s", tissue_id, region)
    req = {
        "tissue_id": tissue_id,
        "region": region,
        "bg": bg
    }
    nport, nid = MANAGER.add(req)
    context = {
        "url": flask.request.path
    }
    context["userid"] = str(nid)
    context["port"] = str(nport)
    return flask.jsonify(**context)