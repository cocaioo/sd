from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, template_folder='templates')
CORS(app)


def read_events(limit=200):
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
    # keep latest events
    return events[-limit:]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events')
def events_api():
    ev = read_events()
    return jsonify(ev)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
