import socket
import struct

def send_msq(sock, msq):
    total_sent_len = 0
    total_msq_len = len(msq)
    while total_sent_len < total_msq_len:
        sent_len = sock.send(msq[total_sent_len:])
        if sent_len == 0:
            raise RuntimeError('socket connection broken')
        total_sent_len += sent_len

def recv_msq(sock, total_msq_size):
    total_recv_size = 0
    while total_recv_size < total_msq_size:
        received_chunk = sock.recv(total_msq_size - total_recv_size)
        if len(received_chunk) == 0:
            raise RuntimeError('socket connection broken')
        yield received_chunk
        total_recv_size += len(received_chunk)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,True)
    server_socket.bind(('127.0.0.1', 54321))
    server_socket.listen()
    print('starting server ...')
    client_socket, (client_address, client_port) = server_socket.accept()
    print(f'accepted from {client_address}:{client_port}')
    received_msq = b''.join(recv_msq(client_socket, total_msq_size=8))
    print(f'received: {received_msq}')
    (operand1, operand2) = struct.unpack('!ii', received_msq)
    print(f'operand1: {operand1}, operand2: {operand2}')
    result = operand1 + operand2
    print(f'result: {result}')
    result_msq = struct.pack('!q', result)
    send_msq(client_socket, result_msq)
    print(f'sent: {result_msq}')
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()

