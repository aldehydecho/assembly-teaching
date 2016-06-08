# IDA Pro反汇编的结果

以下是IDA Pro 输出的main函数：

     S U B R O U T I N E =======================================
     .text:080483C4
     .text:080483C4 ; Attributes: bp-based frame
     .text:080483C4
     .text:080483C4 ; int __cdecl main(int argc, const char **argv, const char **envp)
     .text:080483C4                 public main
     .text:080483C4 main            proc near               ; DATA XREF: _start+17o
     .text:080483C4
     .text:080483C4 var_10          = dword ptr -10h
     .text:080483C4 var_C           = dword ptr -0Ch
     .text:080483C4 var_8           = dword ptr -8
     .text:080483C4 var_4           = dword ptr -4
     .text:080483C4 argc            = dword ptr  8
     .text:080483C4 argv            = dword ptr  0Ch
     .text:080483C4 envp            = dword ptr  10h
     .text:080483C4
     .text:080483C4                 push    ebp
     .text:080483C5                 mov     ebp, esp
     .text:080483C7                 sub     esp, 18h
     .text:080483CA                 and     esp, 0FFFFFFF0h
     .text:080483CD                 mov     eax, 0
     .text:080483D2                 sub     esp, eax
     .text:080483D4                 mov     [ebp+var_4], 11E67h
     .text:080483DB                 mov     [ebp+var_8], 5B1270h
     .text:080483E2                 mov     [ebp+var_10], 6
     .text:080483E9                 sub     esp, 0Ch
     .text:080483EC                 push    offset format   ; "Type cd-key: "
     .text:080483F1                 call    _printf
     .text:080483F6                 add     esp, 10h
     .text:080483F9                 sub     esp, 8
     .text:080483FC                 lea     eax, [ebp+var_C]
     .text:080483FF                 push    eax
     .text:08048400                 push    offset aD       ; "%d"
     .text:08048405                 call    _scanf
     .text:0804840A                 add     esp, 10h
     .text:0804840D                 mov     eax, [ebp+var_8]
     .text:08048410                 cmp     eax, [ebp+var_C]
     .text:08048413                 jnz     short loc_8048432
     .text:08048415                 mov     edx, [ebp+var_10]
     .text:08048418                 lea     eax, [ebp+var_4]
     .text:0804841B                 xor     [eax], edx
     .text:0804841D                 sub     esp, 8
     .text:08048420                 push    [ebp+var_4]
     .text:08048423                 push    offset aD_0     ; "%d\n"
     .text:08048428                 call    _printf
     .text:0804842D                 add     esp, 10h
     .text:08048430                 jmp     short loc_8048442
     .text:08048432 ; ---------------------------------------------------------------------------
     .text:08048432
     .text:08048432 loc_8048432:                            ; CODE XREF: main+4Fj
     .text:08048432                 sub     esp, 0Ch
     .text:08048435                 push    offset aWrong   ; "wrong!\n"
     .text:0804843A                 call    _printf
     .text:0804843F                 add     esp, 10h
     .text:08048442
     .text:08048442 loc_8048442:                            ; CODE XREF: main+6Cj
     .text:08048442                 mov     eax, 0
     .text:08048447                 leave
     .text:08048448                 retn
     .text:08048448 main            endp
     .text:08048448
     .text:08048448 ; ---------------------------------------------------------------------------
     .text:08048449                 align 10h
     .text:08048450

注意，这里栈的结果，局部变量和参数的情况，IDA已经自动推断出来，引用的常量地址也直接标注了其内容，汇编中引用到局部变量的也用名字来标志了，比objdump省事多了。

还有更省事的，用IDA Pro的decompiler插件，输出如下：

    int __cdecl main(int argc, const char **argv, const char **envp)
    {
        void *v3; // esp@1
        int v5; // [sp+Ch] [bp-Ch]@1
        int v6; // [sp+10h] [bp-8h]@1
        int v7; // [sp+14h] [bp-4h]@1

        v3 = alloca(0);
        v7 = 73319;
        v6 = 5968496;
        printf("Type cd-key: ");
        scanf("%d", &v5);
        if ( v6 == v5  )
        {
            v7 ^= 6u;
            printf("%d\n", v7);

        }
        else
        {
            printf("wrong!\n");

        }
        return 0;
    }

跟看源代码差不多了吧？
