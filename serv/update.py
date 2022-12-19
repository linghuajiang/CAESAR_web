"""Database update module."""
import hirespy
from hirespy.serv.database import get_db

DB_LOCK = hirespy.app.config['DB_LOCK']

def update(progress, msg, port):
    # database progress
    with hirespy.app.app_context():
        conn = get_db()
        DB_LOCK.acquire()
        conn.execute(
            "UPDATE requests "
            "SET progress = ?, msg = ? "
            "WHERE port = ?",
            (progress, msg, port,))
        DB_LOCK.release()
