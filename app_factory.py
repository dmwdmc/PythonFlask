import logging
import os
from datetime import timedelta

from flask import Flask, request
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from auth import bp as auth_bp
from auth.models import User
from book import bp as book_bp
from dbs import db
from middleware.auth_middleware import init_auth_middleware
from permission import bp as permission_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 20
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
    app.secret_key = 'your_secret_key'
    
    # Babel configuration
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['zh', 'en']
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

    db.init_app(app)
    Migrate(app, db)
    CSRFProtect(app)
    
    # Initialize Babel
    babel = Babel()
    def get_locale():
        # Try to get locale from request args, then from session, then default to zh
        locale = request.args.get('lang')
        if locale and locale in app.config['BABEL_SUPPORTED_LOCALES']:
            return locale
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'zh'

    babel.init_app(app, locale_selector=get_locale)
    @app.context_processor
    def inject_locale():
        return {'get_locale': get_locale}

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(permission_bp)

    # Initialize authentication middleware
    init_auth_middleware(app)
    return app