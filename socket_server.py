# from socketio import SocketIO, emit
# # from flask_socketio import SocketIO, emit
# from flask import request

# socket_conn = None

# connections = { }

# def init_socket(server):
#     socket_conn = SocketIO(server, cors_allowed_origins="*")
#     return socket_conn

# def send_event(event_name, data, to):
#     if not socket_conn:
#         print("Sockets are not connected")
#         return 
#     emit(event_name, data, to)


# @socket_conn.on("connect")
# def handle_connect():
#     user_id = request.args.get("user_id")
#     connections["userId"] = request.sid
#     print("Client connected")
#     # emit("server_message", {"message": "Connected to the server"})

# @socket_conn.on("disconnect")
# def handle_disconnect():
#     if connections["userId"]:
#         del connections["userId"]
#     print("Client disconnected")
#     # socketio.emit("server_message", {"message": "Client disconnected"})



from flask_socketio import SocketIO, emit
from flask import request
import socket
from flask import g


socket_conn = None  
connections = {} 

def get_ipv4():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipv4 = s.getsockname()[0]
    except socket.error:
        ipv4 = "Not available"
    finally:
        s.close()
    return ipv4
 
def init_socket(server):
    global socket_conn  
    socket_conn = SocketIO(server, cors_allowed_origins="*")  
    register_socket_events(socket_conn)  
    return socket_conn

def send_event(event_name, data, to=None):
    if not socket_conn:
        print("Sockets are not connected")
        return 
    if to:
        session_id = connections.get(to)  
        if session_id:
            socket_conn.emit(event_name, data, room=session_id)
        else:
            print(f"User {to} is not connected.")
    else:
        socket_conn.emit(event_name, data)

def register_socket_events(socket_conn):
    @socket_conn.on("connect")
    def handle_connect():
        user_id = request.args.get("user_id")
        
        
        print(f"User {user_id} connected") 
        
        if user_id:
            connections[user_id] = request.sid  
            print(f"User {user_id} connected with SID {request.sid}")

    @socket_conn.on("disconnect")
    def handle_disconnect():
        user_id = next((key for key, value in connections.items() if value == request.sid), None)
        if user_id:
            del connections[user_id]
            print(f"User {user_id} disconnected")  




