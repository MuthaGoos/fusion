#include <stdio.h>

unsigned char shellcode[] = ""


void main()
{
  printf("Shellcode Length %d\n", sizeof(shellcode) -1);
  int (*ret)() = (int (*)())shellcode;
  ret();
}
