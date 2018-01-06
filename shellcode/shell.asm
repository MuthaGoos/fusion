global _start

section .text


_start:
   xor eax, eax
   push eax
   push 0x68732f2f
   push 0x6e69622f
   mov ebx, esp     ; get ptr to /bin//sh
   push eax         ; optional
   push ebx         ; optional
   mov ecx, esp     ; if both removed, then need to xor this
   mov al, 0xb
   int 0x80
