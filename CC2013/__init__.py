import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.mail import Mail
from flask.ext.babel import Babel

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from momentjs import momentjs


# Create flask app, and initialize extensions
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
mail = Mail(app)
babel = Babel(app)

app.jinja_env.globals['momentjs'] = momentjs


import CC2013.views  # import after app, to add all routes


# Log files
if not app.debug:
    import logging

    if not os.environ.get('HEROKU'):
        # Log files
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/cc2013.log', 'a', 1024 * 1024, 10)
        fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        file_handler.setFormatter(logging.Formatter(fmt))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('CC2013 startup')

    # Log email
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER,
                               ADMINS,
                               'CC2013 failure',
                               credentials)
    mail_handler.setLevel(logging.ERROR)
    #app.logger.addHandler(mail_handler)

if os.environ.get('HEROKU'):
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # Log stdout
    from logging import StreamHandler
    stream_handler = StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('CC2013 startup')
