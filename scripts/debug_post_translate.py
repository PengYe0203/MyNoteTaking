import json
import traceback
import os
import sys

# Ensure project root is on sys.path so `src` imports resolve when running from scripts/
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.main import app

app.testing = True

client = app.test_client()

print('Fetching /api/notes to look for an existing note id...')
notes_resp = client.get('/api/notes')
notes = []
try:
    notes = notes_resp.get_json() or []
except Exception:
    pass

if notes and isinstance(notes, list) and len(notes) > 0:
    nid = notes[0].get('id')
    payload = {'note_id': nid, 'target': 'Chinese'}
    print(f'Found note id {nid}, POSTing note_id payload to /api/translate: {payload}')
else:
    payload = {'text': 'This is a test sentence to translate.', 'target': 'Chinese'}
    print('No notes found; POSTing text payload to /api/translate:', payload)

try:
    resp = client.post('/api/translate', json=payload)
    print('Status code:', resp.status_code)
    try:
        print('Response JSON:', resp.get_json())
    except Exception:
        print('Response text:', resp.get_data(as_text=True))
except Exception as e:
    print('Exception raised during request:')
    traceback.print_exc()
