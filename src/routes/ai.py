from flask import Blueprint, request, jsonify, current_app
import os

bp = Blueprint('ai', __name__, url_prefix='/ai')


@bp.route('/chat', methods=['POST'])
def chat():
    """Proxy a simple chat request to OpenAI using model 'gpt-4.1'.
    Expects JSON: {"prompt": "..."}
    Returns JSON: {"reply": "..."} or {"error": "..."}
    """
    data = request.get_json() or {}
    prompt = data.get('prompt')
    if not prompt or not isinstance(prompt, str):
        return jsonify({'error': 'Missing or invalid prompt'}), 400

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return jsonify({'error': 'OpenAI API key not configured on server'}), 500

    # Import here to keep dependency optional until runtime
    try:
        import openai
    except Exception as e:
        current_app.logger.error('OpenAI package not available: %s', e)
        return jsonify({'error': 'OpenAI client library not installed on server'}), 500

    try:
        openai.api_key = api_key
        # Simple completion-style call; adjust per OpenAI SDK version if needed
        resp = openai.ChatCompletion.create(
            model='gpt-4.1',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=512,
        )
        # Navigate the response safely
        reply = None
        if isinstance(resp, dict):
            choices = resp.get('choices')
            if choices and isinstance(choices, list):
                first = choices[0]
                reply = first.get('message', {}).get('content') if isinstance(first, dict) else None
        # Fallback string representation
        if not reply:
            reply = str(resp)

        return jsonify({'reply': reply})
    except Exception as e:
        current_app.logger.exception('OpenAI request failed')
        return jsonify({'error': 'OpenAI request failed', 'detail': str(e)}), 500


@bp.route('/translate', methods=['POST'])
def translate():
    """Translate a note or arbitrary text.
    JSON body options:
      - note_id: integer (optional) — translate content of the note with this id
      - text: string (optional) — direct text to translate
      - target: string (optional) — target language or style (default: 'Chinese')
    Returns: { translation: '...' }
    """
    data = request.get_json() or {}
    note_id = data.get('note_id')
    text = data.get('text')
    target = data.get('target', 'Chinese')

    if not text and not note_id:
        return jsonify({'error': 'Provide either note_id or text to translate'}), 400

    # Lazily import models to avoid circular imports at module load time
    try:
        from src.models.note import Note
        from src.models.user import db
    except Exception as e:
        current_app.logger.exception('Failed to import Note model')
        return jsonify({'error': 'Server configuration error', 'detail': str(e)}), 500

    if note_id:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        text = note.content

    # Build a concise prompt for translation
    system_prompt = f"You are a helpful translator. Translate the user's text into {target}. Preserve meaning and formatting. Return only the translated text without commentary."
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': text}
    ]

    # Use the project's LLM wrapper if available
    try:
        from src import llm as llm_module
        translated = llm_module.call_llm_model(llm_module.model, messages)
    except Exception as e:
        # Detect common content-filtering / policy errors surfaced by LLM clients
        msg = str(e)
        current_app.logger.exception('LLM translate failed')
        if 'content_filter' in msg or 'ResponsibleAIPolicyViolation' in msg or 'content_filter_result' in msg:
            # Return unprocessable entity so frontend can show a friendly message
            return jsonify({'error': 'Translation blocked by model content filter', 'detail': msg}), 422
        # Fallback: internal server error for other exceptions
        return jsonify({'error': 'Translation failed', 'detail': msg}), 500

    return jsonify({'translation': translated})
