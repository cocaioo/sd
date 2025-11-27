from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
from flask import request

app = Flask(__name__, template_folder='templates')
CORS(app)


def read_events(limit=200):
    """Read events from shared log.

    By default only server events are returned to avoid duplicate request/response
    pairs being shown (client + server). To include client events set the
    environment variable `RPC_SHOW_CLIENT_EVENTS=1` for the `monitor` service.
    """
    shared = os.environ.get('RPC_SHARED_PATH', '/shared')
    path = os.path.join(shared, 'events.log')
    events = []
    try:
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []

    # By default deduplicate identical events coming from client+server
    # (client.request + server.request produce the same payload). Set
    # `RPC_DISABLE_DEDUP=1` to disable deduplication for debugging.
    disable_dedup = os.environ.get('RPC_DISABLE_DEDUP', '0') == '1'

    if not disable_dedup:
        seen = set()
        filtered = []
        for e in events:
            try:
                payload = e.get('payload', {})
                # deterministic string representation of payload for comparison
                payload_key = json.dumps(payload, sort_keys=True, ensure_ascii=False)
            except Exception:
                payload_key = str(e.get('payload'))
            key = (e.get('type'), payload_key)
            if key in seen:
                continue
            seen.add(key)
            filtered.append(e)
        events = filtered

    # keep latest events
    return events[-limit:]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events')
def events_api():
    ev = read_events()
    return jsonify(ev)


@app.route('/control/clear', methods=['POST'])
def control_clear():
    """Truncate the shared events log. Returns JSON status."""
    shared = os.environ.get('RPC_SHARED_PATH', '/shared')
    path = os.path.join(shared, 'events.log')
    try:
        # ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').close()
        return jsonify({'status': 'ok', 'cleared': True})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


if __name__ == '__main__':
    # Optionally clear events log on monitor start (default enabled)
    clear_on_start = os.environ.get('RPC_CLEAR_ON_START', '1') != '0'
    if clear_on_start:
        try:
            shared = os.environ.get('RPC_SHARED_PATH', '/shared')
            path = os.path.join(shared, 'events.log')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').close()
            print('[MONITOR] Cleared events.log on startup')
        except Exception:
            pass

    app.run(host='0.0.0.0', port=5000, debug=False)
