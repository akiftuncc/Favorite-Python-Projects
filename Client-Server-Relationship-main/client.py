import socket

# Server configuration
SERVER1_HOST = 'localhost'
SERVER1_PORT = 5000
SERVER2_HOST = 'localhost'
SERVER2_PORT = 5001

# Function to send song existence request to servers
def check_song_existence(song_name):
    check_server = input("to server1 press '1', to server2 press '2'")
    # Server 1
    if check_server == "1":
        server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server1.connect((SERVER1_HOST, SERVER1_PORT))
        print("Sending song name to server 1...")
        server1.send(song_name.encode())
        print("Receiving response from server 1...")
        response1 = server1.recv(1024).decode()
        print("Response received from server 1:", response1)
        server1.close()
        return response1

    # Server 2
    elif check_server == "2":
        server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server2.connect((SERVER2_HOST, SERVER2_PORT))
        print("Sending song name to server 2...")
        server2.send(song_name.encode())
        print("Receiving response from server 2...")
        response2 = server2.recv(1024).decode()
        print("Response received from server 2:", response2)
        server2.close()
        return response2

    else:
        print("wrong Key!")
        return 0




# Function to download or stream the song from a server
def download_song(server_host, server_port, song_name):
    download_input = input("To download press '1' \t To skip press any key:")
    if download_input == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((server_host, server_port))
        server.send(song_name.encode())
        response = server.recv(1024)
        print(f"{song_name} is downloaded.")
        server.close()
    else:
        print("Download Skipped.")




song_name = input("Enter the name of the song: ")

# Check song existence on both servers
response1 = check_song_existence(song_name)

if response1 == 'EXIST':
    # Server 1 has the song
    download_song(SERVER1_HOST, SERVER1_PORT, song_name)
else:
    print("The song does not exist on any server.")

while True:
    song_name = input("Enter the name of the song (or 'q' to quit): ")
    if song_name == 'q':
        break

    # Check song existence on both servers
    response1 = check_song_existence(song_name)

    if response1 == 'EXIST':
        # Server 1 has the song
        download_song(SERVER1_HOST, SERVER1_PORT, song_name)
    else:
        print("The song does not exist on any server.")