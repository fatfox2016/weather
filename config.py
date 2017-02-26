import os

basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_TYPE = 'sqlalchemy'
