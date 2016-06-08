# mycrk2 程序分析

## 1. 整体观察

### 文件类型
用file命令可以查看文件类型：

    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ file mycrk2
    mycrk2: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.26, BuildID[sha1]=6ed9a4682b747a820345f88e1a09f821b7471f68, stripped
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$

### 行为观察
这个程序输出一个等式，而且随着参数变化变化，随便试几个发现等式都不成立

    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 
    Your solution is 1 + 1 = 3
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 
    Your solution is 1 + 1 = 3
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2
    Your solution is 1 + 1 = 5
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2 3
    Your solution is 4 + 1 = 6
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2 3 4
    Your solution is 5 + 1 = 7
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2 3 5
    Your solution is 5 + 1 = 7
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2 3 6
    Your solution is 5 + 1 = 7
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 1 2 3 6 7
    Your solution is 6 + 1 = 8
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$

## 2, 阅读程序

### 多少个参数正确？

通过main函数很容易看到，如果argc不是3，则调用一个函数后退出（该函数打印一个不成立的等式argc + 1 = argc + 2)。如果是3，会做更多事情。

    9C sub_804869C     proc near               ; CODE XREF: main+28p
    .text:0804869C                                         ; main+234p ...
    .text:0804869C
    .text:0804869C arg_0           = dword ptr  8
    .text:0804869C arg_4           = dword ptr  0Ch
    .text:0804869C arg_8           = dword ptr  10h
    .text:0804869C
    .text:0804869C                 push    ebp
    .text:0804869D                 mov     ebp, esp
    .text:0804869F                 sub     esp, 18h
    .text:080486A2                 mov     eax, [ebp+arg_8]
    .text:080486A5                 mov     [esp+0Ch], eax
    .text:080486A9                 mov     eax, [ebp+arg_4]
    .text:080486AC                 mov     [esp+8], eax
    .text:080486B0                 mov     eax, [ebp+arg_0]
    .text:080486B3                 mov     [esp+4], eax
    .text:080486B7                 mov     dword ptr [esp], offset format ; "Your solution is %d + %d = %d\n"
    .text:080486BE                 call    _printf
    .text:080486C3                 leave
    .text:080486C4                 retn
    .text:080486C4 sub_804869C     endp

继续分析，发现程序对argv[1]和argv[2]分别做了处理

### argv[1]

复制argv[1]，在argv[1]的末尾加上两个和当前时间有关的字节：

    loc_8048838:                            ; CODE XREF: main+Ej
    .text:08048838                 mov     eax, [ebp+arg_4]
    .text:0804883B                 mov     eax, [eax+4]
    .text:0804883E                 mov     [esp+34h], eax
    .text:08048842                 mov     eax, [esp+34h]  ; 存放argv[1]
    .text:08048846                 mov     [esp], eax      ; s
    .text:08048849                 call    _strlen         ; strlen(argv[1])
    .text:0804884E                 mov     [esp+30h], eax  ; 存放strlen(argv[1])
    .text:08048852                 lea     eax, [esp+14h]
    .text:08048856                 mov     [esp], eax      ; timer
    .text:08048859                 call    _time
    .text:0804885E                 lea     eax, [esp+14h]  ; 存放当前时间
    .text:08048862                 mov     [esp], eax      ; timer
    .text:08048865                 call    _localtime
    .text:0804886A                 mov     [esp+2Ch], eax  ; 存放tm_struct
    .text:0804886E                 mov     eax, [esp+30h]
    .text:08048872                 add     eax, 2
    .text:08048875                 mov     [esp], eax      ; size
    .text:08048878                 call    _malloc         ; malloc(strlen(argv[1]) + 2)
    .text:0804887D                 mov     [esp+28h], eax  ; 存放分配的内存起始地址
    .text:08048881                 mov     eax, [esp+28h]
    .text:08048885                 mov     [esp+4Ch], eax
    .text:08048889                 mov     dword ptr [esp+48h], 0 ; 循环变量i=0
    .text:08048891                 jmp     short loc_80488B0
    .text:08048893 ; ---------------------------------------------------------------------------
    .text:08048893
    .text:08048893 loc_8048893:                            ; CODE XREF: main+BCj
    .text:08048893                 mov     edx, [esp+48h]
    .text:08048897                 mov     eax, [esp+34h]
    .text:0804889B                 add     eax, edx
    .text:0804889D                 movzx   edx, byte ptr [eax]
    .text:080488A0                 mov     eax, [esp+4Ch]  ; 分配内存起始地址
    .text:080488A4                 mov     [eax], dl       ; p[i] =argv[1][i] ,复制字符串
    .text:080488A6                 add     dword ptr [esp+4Ch], 1 ; 内存指针++
    .text:080488AB                 add     dword ptr [esp+48h], 1 ; i++
    .text:080488B0
    .text:080488B0 loc_80488B0:                            ; CODE XREF: main+90j
    .text:080488B0                 mov     eax, [esp+48h]
    .text:080488B4                 cmp     eax, [esp+30h]
    .text:080488B8                 setl    al
    .text:080488BB                 test    al, al          ; i < strlen(argv[1])
    .text:080488BD                 jnz     short loc_8048893
    .text:080488BF                 mov     eax, [esp+2Ch]
    .text:080488C3                 mov     eax, [eax+4]
    .text:080488C6                 and     eax, 0Fh
    .text:080488C9                 add     eax, 41h        ; tm->tm_min & 0xf + 0x41
    .text:080488CC                 mov     edx, eax
    .text:080488CE                 mov     eax, [esp+4Ch]
    .text:080488D2                 mov     [eax], dl
    .text:080488D4                 add     dword ptr [esp+4Ch], 1
    .text:080488D9                 mov     eax, [esp+2Ch]
    .text:080488DD                 mov     eax, [eax+8]
    .text:080488E0                 and     eax, 0Fh
    .text:080488E3                 add     eax, 42h        ; tm->tm_hour & 0xf + 0x42
    .text:080488E6                 mov     edx, eax
    .text:080488E8                 mov     eax, [esp+4Ch]
    .text:080488EC                 mov     [eax], dl
    .text:080488EE                 add     dword ptr [esp+4Ch], 1
       
时间结构，所以tm + 8是 tm_hour域, tm + 4 是tm_min

    struct tm {
        int tm_sec;    /* Seconds (0-60) */
        int tm_min;    /* Minutes (0-59) */
        int tm_hour;   /* Hours (0-23) */
        int tm_mday;   /* Day of the month (1-31) */
        int tm_mon;    /* Month (0-11) */
        int tm_year;   /* Year - 1900 */
        int tm_wday;   /* Day of the week (0-6, Sunday = 0) */
        int tm_yday;   /* Day in the year (0-365, 1 Jan = 0) */
        int tm_isdst;  /* Daylight saving time */
    };


### argv[2]

按8个字节一组处理三次，每次8个字符被解码为一个数字(函数0x8048710)，每次的结果被检查是否等于argv[1]扩充后的buffer经过函数0x80486c5之后的结果。如果三次都正确，这个argv[1]/argv[2]的组合认为是正确的。

这是0x8048710的函数处理：

     8048710 sub_8048710     proc near               ; CODE XREF: main+13Dp
    .text:08048710
    .text:08048710 var_20          = dword ptr -20h
    .text:08048710 var_1C          = dword ptr -1Ch
    .text:08048710 var_15          = byte ptr -15h
    .text:08048710 var_14          = dword ptr -14h
    .text:08048710 var_D           = byte ptr -0Dh
    .text:08048710 var_C           = dword ptr -0Ch
    .text:08048710 s               = dword ptr  8
    .text:08048710
    .text:08048710                 push    ebp
    .text:08048711                 mov     ebp, esp
    .text:08048713                 push    ebx
    .text:08048714                 sub     esp, 34h
    .text:08048717                 mov     eax, [ebp+s]
    .text:0804871A                 mov     [esp], eax      ; s
    .text:0804871D                 call    _strlen
    .text:08048722                 mov     [ebp+var_20], eax
    .text:08048725                 mov     [ebp+var_C], 0
    .text:0804872C                 mov     [ebp+var_D], 0
    .text:08048730                 mov     [ebp+var_14], 0 ; i=0
    .text:08048737                 jmp     loc_80487D5
    .text:0804873C ; ---------------------------------------------------------------------------
    .text:0804873C
    .text:0804873C loc_804873C:                            ; CODE XREF: sub_8048710+D0j
    .text:0804873C                 mov     [ebp+var_15], 0
    .text:08048740                 mov     [ebp+var_1C], 0 ; j=0
    .text:08048747                 jmp     short loc_8048784
    .text:08048749 ; ---------------------------------------------------------------------------
    .text:08048749
    .text:08048749 loc_8048749:                            ; CODE XREF: sub_8048710+7Dj
    .text:08048749                 mov     edx, [ebp+var_14]
    .text:0804874C                 mov     eax, [ebp+s]
    .text:0804874F                 add     eax, edx
    .text:08048751                 movzx   edx, byte ptr [eax] ; s[i]
    .text:08048754                 mov     eax, [ebp+var_1C]
    .text:08048757                 add     eax, 8048B4Fh   ; const[j]
    .text:0804875C                 movzx   eax, byte ptr [eax]
    .text:0804875F                 cmp     dl, al
    .text:08048761                 jnz     short loc_8048780
    .text:08048763                 mov     eax, 7
    .text:08048768                 sub     eax, [ebp+var_14]
    .text:0804876B                 shl     eax, 2
    .text:0804876E                 mov     edx, [ebp+var_1C]
    .text:08048771                 mov     ebx, edx
    .text:08048773                 mov     ecx, eax
    .text:08048775                 shl     ebx, cl
    .text:08048777                 mov     eax, ebx
    .text:08048779                 or      [ebp+var_C], eax
    .text:0804877C                 mov     [ebp+var_15], 1
    .text:08048780
    .text:08048780 loc_8048780:                            ; CODE XREF: sub_8048710+51j
    .text:08048780                 add     [ebp+var_1C], 1 ; j++
    .text:08048784
    .text:08048784 loc_8048784:                            ; CODE XREF: sub_8048710+37j
    .text:08048784                 cmp     [ebp+var_1C], 0Fh
    .text:08048788                 setbe   al
    .text:0804878B                 test    al, al          ; if (j <= 15)
    .text:0804878D                 jnz     short loc_8048749
    .text:0804878F                 movzx   eax, [ebp+var_15]
    .text:08048793                 xor     eax, 1
    .text:08048796                 test    al, al
    .text:08048798                 jz      short loc_80487C5
    .text:0804879A                 mov     edx, [ebp+var_14]
    .text:0804879D                 mov     eax, [ebp+s]
    .text:080487A0                 add     eax, edx
    .text:080487A2                 movzx   eax, byte ptr [eax]
    .text:080487A5                 movsx   edx, al
    .text:080487A8                 mov     eax, 7
    .text:080487AD                 sub     eax, [ebp+var_14]
    .text:080487B0                 shl     eax, 2
    .text:080487B3                 mov     ecx, eax
    .text:080487B5                 shl     edx, cl
    .text:080487B7                 mov     eax, [ebp+var_14]
    .text:080487BA                 imul    eax, 0FAB157h
    .text:080487C0                 xor     eax, edx
    .text:080487C2                 or      [ebp+var_C], eax
    .text:080487C5
    .text:080487C5 loc_80487C5:                            ; CODE XREF: sub_8048710+88j
    .text:080487C5                 cmp     [ebp+var_14], 6
    .text:080487C9                 jle     short loc_80487D1 ; i++
    .text:080487CB                 mov     [ebp+var_D], 1
    .text:080487CF                 jmp     short loc_80487E6
    .text:080487D1 ; ---------------------------------------------------------------------------
    .text:080487D1
    .text:080487D1 loc_80487D1:                            ; CODE XREF: sub_8048710+B9j
    .text:080487D1                 add     [ebp+var_14], 1 ; i++
    .text:080487D5
    .text:080487D5 loc_80487D5:                            ; CODE XREF: sub_8048710+27j
    .text:080487D5                 mov     eax, [ebp+var_14]
    .text:080487D8                 cmp     eax, [ebp+var_20]
    .text:080487DB                 setb    al
    .text:080487DE                 test    al, al          ; if (i<strlen(s))
    .text:080487E0                 jnz     loc_804873C
    .text:080487E6
    .text:080487E6 loc_80487E6:                            ; CODE XREF: sub_8048710+BFj
    .text:080487E6                 movzx   eax, [ebp+var_D]
    .text:080487EA                 xor     eax, 1
    .text:080487ED                 test    al, al
    .text:080487EF                 jz      short loc_80487F8
    .text:080487F1                 xor     [ebp+var_C], 9A9B9C9Dh
    .text:080487F8
    .text:080487F8 loc_80487F8:                            ; CODE XREF: sub_8048710+DFj
    .text:080487F8                 mov     eax, [ebp+var_C]
    .text:080487FB                 add     esp, 34h
    .text:080487FE                 pop     ebx
    .text:080487FF                 pop     ebp
    .text:08048800                 retn
    .text:08048800 sub_8048710     endp

这个一个两重循环，对8个字符一一检查，如果字符落到一个解码表中（0x8048b4f：0123456789AbCdEf)，则转换为数字，否则进行无意思的混淆处理。如果输入长度不是刚好8字节，也会做混淆让结果无意义。

对argv[1]扩充而来的buffer的处理函数，翻译成C就是：

    int gen_number_a(char *buffer, int len, int passn) {
        result = (passn * 0xef41) + 0x2cdc3
            counter = 0
            for (i=0; i < len, i++) {
                result += i * buffer[i];
            }
        return result
    }

## 3. keygen

Keygen的结构是：

1. argv[1] 作为用户名，扩充和时间有关的两个字节
2. 应用gen_number_a三次，pass从0-3，产生三个数字
3. 每个数字转换成16进制数，每个位通过解码表采用相应的字符，转换成为8位的hex，不足8位前面补0
4. argv[2]也就是这个用户的key是这个三个数字转换来的字符串拼接结果，

由于算法和时间相关，所以kegen得出来的结果同一分钟使用才有效。

程序里两次取时间，如果两次的时间间隔超过1分钟，也会得不出正确结果，这是为了防止调试。

    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ python solution.py zfx
    COMMAND: ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ date
    2016年 06月 07日 星期二 22:11:50 CST
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 4 + 29 = 33
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ ./mycrk2 zfx 0002d11d0003C05E0004Af9f
    Your solution is 3 + 24 = 30
    foxsen@foxsen-pc:~/汇编教案/crackme/level2/mycrk2$ 


