"""REST API error handler."""
import flask
import hirespy


MSG = {
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict"
}


class InvalidUsage(Exception):
    """Customized error class."""

    def __init__(self, status_code,
                 logname=None, postid=None):
        """Invalid usage object constructor."""
        Exception.__init__(self)
        self.status_code = status_code
        self.logname = logname
        self.postid = postid

    def to_dict(self):
        """Convert to dict."""
        info = dict()
        info['message'] = MSG[self.status_code]
        info['status_code'] = self.status_code
        if self.status_code == 409:
            info['logname'] = self.logname
            info['postid'] = self.postid
        return info


@hirespy.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Error handler."""
    response = flask.jsonify(error.to_dict())
    # response.status_code = error.status_code
    return response, error.status_code