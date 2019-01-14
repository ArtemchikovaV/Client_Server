import socket

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 10001))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                if "get" in data.decode("utf8"):
                    conn.send(b"ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n")
                   # print("send information")
                else:
                    conn.send(b"ok\n\n")
                    print(data.decode("utf8"))


        #conn.sendall(b"sendall")
