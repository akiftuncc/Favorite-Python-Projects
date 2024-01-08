import socket
import threading

# Server configuration
HOST = 'localhost'
PORT1 = 5000  # Server 1 port
PORT2 = 5001  # Server 2 port

# Shared song list
song_list = ['song1', 'song2', 'song3']

# Server 1 handler
def server1_handler(conn):
    available_list = song_list[0:2]
    data = conn.recv(1024).decode()
    if data in available_list:
        conn.send(b'EXIST')
    else:
        conn.send(b'NOT_EXIST')

# Server 2 handler
def server2_handler(conn):
    available_list = song_list[1:3]
    data = conn.recv(1024).decode()
    if data in available_list:
        conn.send(b'EXIST')
    else:
        conn.send(b'NOT_EXIST')

# Start both servers
def start_servers():
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1.bind((HOST, PORT1))
    server2.bind((HOST, PORT2))
    server1.listen()
    server2.listen()
    print(f"Server 1 listening on {HOST}:{PORT1}")
    print(f"Server 2 listening on {HOST}:{PORT2}")

    while True:
        conn1, addr1 = server1.accept()
        print(f"Connected to client from {addr1}")
        threading.Thread(target=server1_handler, args=(conn1,), daemon=True).start()

        conn2, addr2 = server2.accept()
        print(f"Connected to client from {addr2}")
        threading.Thread(target=server2_handler, args=(conn2,), daemon=True).start()

        conn1.settimeout(1)  # Set a timeout for conn1
        conn2.settimeout(1)  # Set a timeout for conn2

start_servers()
