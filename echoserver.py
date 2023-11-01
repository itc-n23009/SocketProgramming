import socket

def send_msq(sock, msq):
    total_sent_len = 0
    total_msq_len = len(msq)
    while total_sent_len < total_msq_len:
        sent_len = sock.send(msq[total_sent_len:])
        if sent_len == 0:
            raise RuntimeError('socket connection broken')
        total_sent_len += sent_len

def recv_msq(sock, chunk_len=1024):
    while True:
        received_chunk = sock.recv(chunk_len)
        fi len(received_chunk) == 0:
            break
        yield received_chunk

def main():
    server_socket =socket.socket(socket.SOL_SOCKET, socket.SO_REUSERADDR, True)
    server_socket.bind(('127.0.0.1', 54321))
    server_socket.listen()
    print('starting server ...')
    client_socket, (client_address, client_port) = server_socket.accept()
    print(f'accepted from {client_address}:{client_port}')
    for received_msq in recv_msq(client_socket):
        send_msq(client_socket, received_msq)
        print(f'echo: {received_msq}')
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()
