import socket

def send_msq(sock, msq):

    total_sent_len = 0

    total_msq_len = len(msq)

    while total_sent_len < total_msq_len:

        sent_len = sock.send(msq[total_sent_len:])

        if sent_len == 0:
            raise RuntimeError('socket conneciton broken')

        total_sent_len += sent_len

def recv_msq(sock, chunk_len=1024):

    while True:

        received_chunk = sock.recv(chunk_len)

        if len(received_chunk) == 0:
            break

        yield received_chunk

def main ():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('127.0.0.1', 80))

    request_text = 'GET / HTTP/1.0\r\n\r\n'

    request_bytes = request_text.encode('ASCII')

    send_msq(client_socket, request_bytes)

    received_bytes = b''.join(recv_msq(client_socket))

    received_text = received_bytes.decode('ASCII')

    print(received_text)

    client_socket.close

if __name__ == '__main__':

    main()
