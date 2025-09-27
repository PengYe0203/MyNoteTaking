from flask import Blueprint, request, jsonify, current_app
import os

bp = Blueprint('ai', __name__, url_prefix='/api/ai')


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
