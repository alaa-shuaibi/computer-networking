import socket, sys
from pg1lib import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1])
ADDR = (HOST, PORT)

pubKey = getPubKey()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
except:
    print('Failed to create socket.')
    sys.exit()

try:
    sock.bind(ADDR)
except:
    print('Failed to bind socket.')

while True:
    #print("Waiting to receive client's public key...")
    client_key, client_ADDR = sock.recvfrom(4096)

    #print("Encrypting key...")
    encryptedKey = encrypt(pubKey, client_key)
    #print('Sending encrypted key to client...')
    sock.sendto(encryptedKey, client_ADDR)

    #print('Waiting to receive encrypted message from client...')
    encrypted_msg, client_ADDR = sock.recvfrom(4096)
    #print('Waiting to receive checksum from client...')
    received_checksum, client_ADDR = sock.recvfrom(4096)

    #print('Decrypting the message...')
    msg = decrypt(encrypted_msg)
    actual_checksum = checksum(msg)
    
    print("Message: " + msg.decode())
    print("Recieved checksum: " + received_checksum.decode())
    print("Actual checksum: " + str(actual_checksum))

    #print('Sending confirmation...')
    if int(received_checksum.decode()) == int(actual_checksum):
        sock.sendto(bytes('1', 'utf-8'), client_ADDR)
    else:
        sock.sendto(bytes('0', 'utf-8'), client_ADDR)
