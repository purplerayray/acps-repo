import socket
import os

if os.path.isfile('vehicles.db'):
    pass
else:
    import database
    db_obj = database.CreateDatabase()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5434
host = 'localhost'
s.bind((host, port))
print("Server has been created")
s.listen(3)

while True:
    print(f'listening for connections on port {port}...')
    conn, addr = s.accept()
    print("\nConnected to client ", addr)
    conn.send(str.encode('<<Successfully connected to server>>\n'))

    while True:
        client_request = bytes.decode(conn.recv(1824))

        if client_request == 'send_database':
            conn.send(str.encode('vehicles.db'))

        elif client_request == 'end_connection':
            print(f'Disconnecting from client {addr}\n')
            conn.send(str.encode('disconnected from server...'))
            break

        else:
            print(f'Connection Error with {addr}\n')
            break
    conn.close()
