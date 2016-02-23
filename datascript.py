import socket
import binascii


address = ('172.69.8.4', 4370)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect(address)  
#s.send("POST /xmlrpc/common HTTP/1.1\r\n")

# def rev_data(sock):
#     buf = sock.recv(1024)
#     print binascii.b2a_hex(buf)



data = binascii.a2b_hex("5050827D08000000E80317FC00000000")

s.send(data)
rev = s.recv(1024)
rev = binascii.b2a_hex(rev)

print rev
s_data2 = rev[0:-3] +'1' + rev[-2:]
print s_data2
data = binascii.a2b_hex(s_data2)


s.send(data)
rev = s.recv(1024)
rev = binascii.b2a_hex(rev)

print rev




