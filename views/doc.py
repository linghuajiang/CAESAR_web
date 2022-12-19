"""
Hirespy doc view.

URLs include:
/doc/
"""
import logging
import json
import flask
import hirespy


@hirespy.app.route('/doc/', methods=['GET'])
def doc():
    """Display / route."""
    return flask.render_template("doc.html")