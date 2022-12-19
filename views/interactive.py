import json
import flask
import hirespy

@hirespy.app.route('/interactive', methods=['GET', 'POST'])
def test_interactive():
    """Display / route."""

    context = {}

    return flask.render_template("interactive.html", **context)
