**Odpalanie**
```bash
./Nukleo_shutter/venv/Scripts/python.exe ./Nukleo_shutter/main.py
```



Message sent should like this b'V' where V is the value of the shutter between 0 and 100

If you close the stream (i.e., the socket) that is communicating with the Nucleo, the Nucleo will detect that the stream was closed. When a socket is closed, 
the other end of the connection will receive an end-of-file (EOF) indication. This allows the Nucleo to detect that the connection has been terminated.


**TODO** kod w pythonie na nukleo powinien byc asyncrhoniczny i caly czas czekac na polaczenie tcp_ip = 0.0.0.0 znaczy w teori ze na wszystkich ip i na tym jednym ustalonym porcie
jezeli jest polaczony to czeka na wiadomosc od apki na wartosc w tym samym formacie co wysyla jak jest rozloczony to dziala normalnie 

```TCP_IP = '0.0.0.0'
TCP_PORT = 55151
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

print("Waiting for a connection...")
while True:
    conn, addr = server_socket.accept()
    print(f"Connection from: {addr}")
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"Received data: {data}")
        # Process the data
    conn.close()
    print("Connection closed, waiting for a new connection...")
```

Tak nie wyswietla wartosci swiatla ale no to nie jest konieczne do kontrolowanie nim 
