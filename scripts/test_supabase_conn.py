import os
import sys
import time
from pathlib import Path

def main():
    # Try to load .env from the repository root if python-dotenv is available
    try:
        from dotenv import load_dotenv
        repo_root = Path(__file__).resolve().parents[1]
        env_path = repo_root / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=str(env_path))
    except Exception:
        # python-dotenv not available or failed; proceed, env may already be set
        pass

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print('DATABASE_URL is not set in environment or .env')
        sys.exit(2)

    print('Using DATABASE_URL:', database_url if '://' not in database_url or database_url.count('@')==0 else database_url.split('@')[0] + '@***')

    try:
        import psycopg2
        from psycopg2 import sql
    except Exception as e:
        print('psycopg2 not available:', e)
        sys.exit(3)

    try:
        # Try a quick connect and simple query
        print('Attempting to connect to Postgres...')
        # Set a short timeout
        conn = psycopg2.connect(dsn=database_url, connect_timeout=10)
        cur = conn.cursor()
        cur.execute('SELECT 1')
        r = cur.fetchone()
        print('Query result:', r)
        cur.close()
        conn.close()
        print('Connection test SUCCEEDED')
        sys.exit(0)
    except Exception as e:
        print('Connection test FAILED:')
        print(type(e).__name__ + ':', e)
        # If error suggests SSL required, hint to add ?sslmode=require
        if 'ssl' in str(e).lower() or 'certificate' in str(e).lower():
            print('\nHint: the server may require SSL. Try adding `?sslmode=require` to your DATABASE_URL.')
        sys.exit(4)

if __name__ == '__main__':
    main()
