
"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage
from hirespy.serv.database import get_db


DB_LOCK = hirespy.app.config['DB_LOCK']


@hirespy.app.route('/api/v1/datasets/', methods=["GET"])
def get_datasets():
    """Return available resources."""
    # check login
    # if "username" not in flask.session:
    #     raise InvalidUsage(403)
    # in session
    conn = get_db()
    DB_LOCK.acquire()
    datasets = conn.execute(
        "SELECT id, name, path "
        "FROM datasets ",
    ).fetchall()
    DB_LOCK.release()
    context = {
        "datasets": datasets,
        "url": flask.request.path
    }
    return flask.jsonify(**context)


@hirespy.app.route('/api/v1/datasets/new/', methods=["POST"])
def post_dataset():
    """Return a list of comments for one post."""

    # post comments
    name = flask.request.get_json().get("name")
    path = flask.request.get_json().get("path")
    conn = get_db()
    DB_LOCK.acquire()
    datasets = conn.execute(
        "INSERT INTO datasets (id, name, path) "
        "VALUES (NULL, ?, ?) ",
        (name, path,)
    )
    conn.commit()
    id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()["last_insert_rowid()"]
    DB_LOCK.release()
    context = {
        "id": id,
        "name": name,
        "path": path,
        "url": flask.request.path
    }
    return flask.jsonify(**context), 201

@hirespy.app.route('/api/v1/datasets/delete/<int:id>/', methods=["DELETE"])
def delete_dataset(id):
    """Delete likes on postid."""

    id = flask.request.get_json().get("id")

    conn = get_db()
    DB_LOCK.acquire()
    datasets = conn.execute(
        "DELETE FROM datasets "
        "WHERE id = ? ",
        (id,)
    )
    conn.commit()
    DB_LOCK.release()

    context = {}
    return flask.jsonify(**context), 204
