import socket 

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 8000
UPSTREAM_ADD=('127.0.0.1',9000)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s: 
    s.bind((HOST,PORT))
    s.listen()
    print(f'Accepting new connections on {HOST}')
    while True: 
        conn, addr = s.accept()
        with conn:
            print(f'connected by address  : {addr}')
            data= conn.recv(4096)
            print(f'-> * {len(data)}')

            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as upstream_s:
                upstream_s.connect(UPSTREAM_ADD)
                print(f"Connected to upstream server! {UPSTREAM_ADD}")
                upstream_s.send(data)
                print(f"* -> {len(data)}")
                while True: 
                    res= upstream_s.recv(4096)
                    print(f"Recieving data from upstream")
                    if not res: 
                            break
                    conn.send(res) 
                    print(f"Sending data back to client")
