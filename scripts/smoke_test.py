import importlib
import json
import sys
from pprint import pprint


def run():
    try:
        main = importlib.import_module('src.main')
    except Exception as e:
        print('Failed to import src.main:', e)
        sys.exit(2)

    app = getattr(main, 'app', None)
    if app is None:
        print('src.main does not expose `app`')
        sys.exit(2)

    client = app.test_client()

    note_payload = {
        'title': 'Smoke test note',
        'content': 'This note was created by an automated smoke test.'
    }

    print('POST /api/notes -> creating note...')
    resp = client.post('/api/notes', json=note_payload)
    print('Status code:', resp.status_code)
    try:
        data = resp.get_json()
    except Exception:
        data = resp.data.decode('utf-8')
    print('Response body:')
    pprint(data)

    if resp.status_code != 201:
        print('Create failed; aborting smoke test')
        sys.exit(3)

    note_id = data.get('id')
    if not note_id:
        print('Response did not include id; aborting')
        sys.exit(3)

    print(f'GET /api/notes/{note_id} -> verifying...')
    resp2 = client.get(f'/api/notes/{note_id}')
    print('Status code:', resp2.status_code)
    try:
        data2 = resp2.get_json()
    except Exception:
        data2 = resp2.data.decode('utf-8')
    print('Fetched note:')
    pprint(data2)

    # Basic content check
    if resp2.status_code == 200 and data2.get('title') == note_payload['title'] and data2.get('content') == note_payload['content']:
        print('Smoke test PASSED: create and read succeeded')
        sys.exit(0)
    else:
        print('Smoke test FAILED: content mismatch or GET failed')
        sys.exit(4)


if __name__ == '__main__':
    run()
