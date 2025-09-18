# socket_manager.py
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # global socketio instance

def init_socketio(app):
    """Initialize socketio with Flask app"""
    socketio.init_app(app)
    return socketio


def emit_update(event_data):
    """Safe emit function (called from anywhere in project)"""
    try:
        socketio.emit("update", event_data, namespace="/", broadcast=True)
    except Exception as e:
        print(f"[SOCKET ERROR] {e}")
