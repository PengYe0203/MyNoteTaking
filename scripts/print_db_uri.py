import importlib.util
import os
from pathlib import Path
import traceback

ROOT = Path(r"E:/projects/Software engineering/NoteTaker/note-taking-app-updated-PengYe0203")
ENV = ROOT / '.env'

def read_env(path):
    d = {}
    if not path.exists():
        return d
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            k,v = line.split('=',1)
            d[k]=v
    return d

print('os.environ MYSQL_USER=', os.environ.get('MYSQL_USER'))
print('os.environ MYSQL_DB=', os.environ.get('MYSQL_DB'))
print('os.environ MYSQL_HOST=', os.environ.get('MYSQL_HOST'))
print('os.environ MYSQL_PORT=', os.environ.get('MYSQL_PORT'))

print('\nChecking pymysql installed:')
print(importlib.util.find_spec('pymysql') is not None)

print('\nParsing .env at', ENV)
env = read_env(ENV)
for k in ('MYSQL_USER','MYSQL_PASSWORD','MYSQL_HOST','MYSQL_PORT','MYSQL_DB'):
    print(f"{k} -> {env.get(k)}")

u = env.get('MYSQL_USER')
p = env.get('MYSQL_PASSWORD')
h = env.get('MYSQL_HOST','localhost')
port = env.get('MYSQL_PORT','3306')
db = env.get('MYSQL_DB')
if u and p and db:
    uri = f"mysql+pymysql://{u}:{p}@{h}:{port}/{db}?charset=utf8mb4"
else:
    uri = 'sqlite'
print('\nConstructed URI from .env:')
print(uri)

# Also show what main.py would pick up via os.getenv at runtime
print('\nRuntime os.getenv values:')
print('RUNTIME MYSQL_USER=', os.getenv('MYSQL_USER'))
print('RUNTIME MYSQL_PASSWORD=', os.getenv('MYSQL_PASSWORD'))
print('RUNTIME MYSQL_DB=', os.getenv('MYSQL_DB'))
print('\nDone')

print('\nNow importing Flask app from src.main to see what it actually configures...')
try:
    # Import app; src/main.py sets up load_dotenv and app.config
    import importlib
    # Ensure project root is on sys.path so `import src.main` works
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    main = importlib.import_module('src.main')
    app = getattr(main, 'app', None)
    if app is None:
        print('Could not find app in src.main')
    else:
        print('app.config["SQLALCHEMY_DATABASE_URI"] =', app.config.get('SQLALCHEMY_DATABASE_URI'))
        # try to inspect the db engine (db is imported from src.models.user)
        try:
            from src.models.user import db
            with app.app_context():
                try:
                    print('db.engine.url =', db.engine.url)
                except Exception as e:
                    print('Error reading db.engine.url:', e)
        except Exception as e:
            print('Error importing db from src.models.user:', e)
except Exception:
    print('Exception while importing src.main:')
    traceback.print_exc()
