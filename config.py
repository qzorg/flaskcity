DEBUG=True
SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///sitedata.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SITE_NAME = "default"
MAX_SITES = "0"
MAX_SITES_PER_USER = "0"
MAX_SITE_TOTAL_SIZE = "0" #in megabytes

UPLOAD_FOLDER = 'static/usersites/'
ALLOWED_EXTENSIONS = set(['tar','tar.gz'])
