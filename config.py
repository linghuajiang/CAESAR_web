"""Hirespy development configuration."""
import os
import threading

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'jf\x9fX\xa4\xc9\x15\x7f/\xf6\
\xa1\x06\x9aPIh\xd9\xc74\x8f\tH\n\x8b'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
# UPLOAD_FOLDER = os.path.join(
#    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
#    'var', 'uploads'
#)
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/hirespy.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'hirespy.sqlite3'
)

# path
ROOT_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
)
LOG_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'log'
)
FILE_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'files'
)
SRC_FOLDER = os.path.join(
    # os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    # 'var', 'files', 'data'
    '/nfs/turbo/umms-drjieliu/nucleome_server'
)
DATA_FOLDER = os.path.join(
    # os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    # 'var', 'files', 'data'
    '/nfs/turbo/umms-drjieliu/nucleome_server', 'data'
)
SHEET_FOLDER = os.path.join(
    # os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    # 'var', 'files', 'sheet'
    '/home/lhjiang/web', 'data', 'sheets'
)
TOOLS_FOLDER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'tools'
)
TEMPLATE_FOLDER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'templates'
)
JSON_FOLDER = os.path.join(
    '/var/www/nucleome/', 'config'
)
AS_FOLDER = os.path.join(
    # os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    # 'var', 'files', 'data'
    '/nfs/turbo/umms-drjieliu/usr/lhjiang/nucleome_server', 'data'
)


# capacity
CAPACITY = 30

# port offset
OFFSET = 3000
HIC_OFFSET = 2900
AS_OFFSET = 3100
EQTL_OFFSET = 3300

# lock
LOCK = threading.Lock()
DB_LOCK = threading.Lock()
