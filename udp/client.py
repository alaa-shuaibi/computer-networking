import socket, sys, time
from pg1lib import *

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST, PORT)

msg = bytes(sys.argv[3],'utf-8')
pubKey = getPubKey()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
except:
    print('Failed to create socket.')
    sys.exit()

start = time.perf_counter()
#print('Sending public key to server...')
sock.sendto(pubKey, ADDR)

#print('Received encrypted key from server...')
encryptedKey, server_ADDR = sock.recvfrom(4096)

#print('Decrypting server key...')
server_key = decrypt(encryptedKey)

#print('Calculating checksum for message...')
check_sum = checksum(msg)
#print('Checksum:' + str(check_sum))

#print('Encrypting message...')
encryptedMsg = encrypt(msg, server_key)

#print('Sending encrypted message...')
sock.sendto(encryptedMsg, ADDR)
#print('Sending checksum...')
sock.sendto(bytes(str(check_sum), 'utf-8'), ADDR)

#print('Waiting for confirmation...')
result, server_ADDR = sock.recvfrom(4096)
end = time.perf_counter()
print("Response Code: " + result.decode())

if int(result.decode()) == 1:
    total_time = end - start
    print('RTT: ' + str(total_time) + "s")

sock.close()