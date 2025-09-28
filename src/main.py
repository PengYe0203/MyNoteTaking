import os
import sys
from dotenv import load_dotenv
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.routes.ai import bp as ai_bp
from src.models.note import Note

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')

# configure database to use repository-root `database/app.db`
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(ROOT_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Try MySQL first; fall back to SQLite if MySQL vars missing
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_port = os.getenv('MYSQL_PORT', '3306')
mysql_db = os.getenv('MYSQL_DB')

# Prefer a single DATABASE_URL (used by Heroku/Vercel/Planetscale). If present, use it.
database_url = os.getenv('DATABASE_URL')

if database_url:
    # DATABASE_URL is preferred for cloud deployments (Vercel/Planetscale)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
elif mysql_user and mysql_password and mysql_db:
    # 使用 pymysql 驱动
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4"
    )
else:
    # configure database to use repository-root `database/app.db`
    DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# IMPORTANT: creating tables automatically in production (Planetscale) is unsafe because
# Planetscale recommends using deploy requests / schema migration tooling for DDL.
# Only auto-create tables when in debug/development or when explicitly allowed.
AUTO_CREATE = os.getenv('AUTO_CREATE_TABLES', 'false').lower() in ('1', 'true', 'yes')
if app.debug or AUTO_CREATE:
    with app.app_context():
        db.create_all()


@app.after_request
def add_dev_no_cache_headers(response):
    # During development, avoid aggressive browser caching of index.html/js
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)