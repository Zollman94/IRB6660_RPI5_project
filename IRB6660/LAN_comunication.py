import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 55000))
    data = s.recv(1024)
    print(f"Z robota přišlo: {data.decode('ascii')}")
    odpoved = "Nazdar robote!"
    s.sendall(odpoved.encode('ascii'))