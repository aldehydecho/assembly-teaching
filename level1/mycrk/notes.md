<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />

# mycrk程序分析

## 分析文件类型
用file命令可以得知，它是一个32位x86-linux的动态链接程序，符号表没有被剥离。

    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ file mycrk
    mycrk: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.0.0, not stripped
    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$

## 运行程序观察反应

    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ ./mycrk
    Type cd-key: 

随便输入一个key：

    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ ./mycrk
    Type cd-key: test
    wrong!
    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$

反汇编(objdump -d ./mycrk)：
[完整反汇编文件](disassemble.md)

## 定位程序相关内容所在

观察反汇编文件可以知道，这是一个比较简单的程序，主要逻辑都在main函数里边：

    080483c4 <main>:
     80483c4:	55                   	push   %ebp
     80483c5:	89 e5                	mov    %esp,%ebp
     80483c7:	83 ec 18             	sub    $0x18,%esp  # 增加0x18字节的栈空间
     80483ca:	83 e4 f0             	and    $0xfffffff0,%esp # 16字节对齐
     80483cd:	b8 00 00 00 00       	mov    $0x0,%eax  # 无意义，alloca(0
     80483d2:	29 c4                	sub    %eax,%esp
     80483d4:	c7 45 fc 67 1e 01 00 	movl   $0x11e67,-0x4(%ebp) # 局部变量1
     80483db:	c7 45 f8 70 12 5b 00 	movl   $0x5b1270,-0x8(%ebp) # 局部变量2
     80483e2:	c7 45 f0 06 00 00 00 	movl   $0x6,-0x10(%ebp) # 局部变量4
     80483e9:	83 ec 0c             	sub    $0xc,%esp   # 准备子程序的栈空间
     80483ec:	68 14 85 04 08       	push   $0x8048514  # 放一个参数给printf, 
                                                           # 字符串'Type cd-key:'
     80483f1:	e8 ee fe ff ff       	call   80482e4 <printf@plt>
     80483f6:	83 c4 10             	add    $0x10,%esp  # 恢复栈(0xc + 4)
     80483f9:	83 ec 08             	sub    $0x8,%esp   # 准备scanf参数
     80483fc:	8d 45 f4             	lea    -0xc(%ebp),%eax # 局部变量3的地址装到eax
     80483ff:	50                   	push   %eax # 参数2
     8048400:	68 22 85 04 08       	push   $0x8048522 # 参数1, 字符串'"%d"'
     8048405:	e8 ba fe ff ff       	call   80482c4 <scanf@plt>
     804840a:	83 c4 10             	add    $0x10,%esp # 恢复栈，0x8 + 4 + 4
     804840d:	8b 45 f8             	mov    -0x8(%ebp),%eax # 局部变量2，0x5b1270
     8048410:	3b 45 f4             	cmp    -0xc(%ebp),%eax # 和输入的数字比较
     8048413:	75 1d                	jne    8048432 <main+0x6e> # 不同则显示错误
     8048415:	8b 55 f0             	mov    -0x10(%ebp),%edx #取局部变量4=0x6
     8048418:	8d 45 fc             	lea    -0x4(%ebp),%eax #去局部变量1=0x11e67
     804841b:	31 10                	xor    %edx,(%eax) # 0x11e67 ^ 6 = 73313
     804841d:	83 ec 08             	sub    $0x8,%esp # 准备printf参数
     8048420:	ff 75 fc             	pushl  -0x4(%ebp) # 上述异或结果
     8048423:	68 25 85 04 08       	push   $0x8048525 # "%d\n"
     8048428:	e8 b7 fe ff ff       	call   80482e4 <printf@plt>
     804842d:	83 c4 10             	add    $0x10,%esp # 恢复栈
     8048430:	eb 10                	jmp    8048442 <main+0x7e> # 返回
     8048432:	83 ec 0c             	sub    $0xc,%esp # 准备调用printf
     8048435:	68 29 85 04 08       	push   $0x8048529 # 'wrong!\n'
     804843a:	e8 a5 fe ff ff       	call   80482e4 <printf@plt>
     804843f:	83 c4 10             	add    $0x10,%esp
     8048442:	b8 00 00 00 00       	mov    $0x0,%eax
     8048447:	c9                   	leave  
     8048448:	c3                   	ret    
     8048449:	90                   	nop

可以看到，密码是明文编码在程序里，输出的数字也只做了最简单的一个运算，只有具备阅读汇编程序的能力，就可以轻松的解开这个破解练习了。


怎么找到字符串的内容呢？例如第一个printf，参数是0x8048514，这个就是字符串的地址。有多种方法可以做。比如我们可以用readelf或者objdump这样的程序查看程序的结构，看这个地址对应的文件位置，然后用工具去查看。<br>
readelf -S ./mycrk输出如下,从第[15]节我们可以看到，虚拟地址0x804850c对应文件偏移0x50c，该节共0x25字节，包含了0x8048514，因此它应对应文件偏移0x514：
     
    共有 33 个节头，从偏移量 0x1b18 开始：

    节头：
      [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
      [ 0]                   NULL            00000000 000000 000000 00      0   0  0
      [ 1] .interp           PROGBITS        08048114 000114 000013 00   A  0   0  1
      [ 2] .note.ABI-tag     NOTE            08048128 000128 000020 00   A  0   0  4
      [ 3] .hash             HASH            08048148 000148 000030 04   A  4   0  4
      [ 4] .dynsym           DYNSYM          08048178 000178 000070 10   A  5   1  4
      [ 5] .dynstr           STRTAB          080481e8 0001e8 000066 00   A  0   0  1
      [ 6] .gnu.version      VERSYM          0804824e 00024e 00000e 02   A  4   0  2
      [ 7] .gnu.version_r    VERNEED         0804825c 00025c 000020 00   A  5   1  4
      [ 8] .rel.dyn          REL             0804827c 00027c 000008 08   A  4   0  4
      [ 9] .rel.plt          REL             08048284 000284 000018 08   A  4  11  4
      [10] .init             PROGBITS        0804829c 00029c 000017 00  AX  0   0  4
      [11] .plt              PROGBITS        080482b4 0002b4 000040 04  AX  0   0  4
      [12] .text             PROGBITS        08048300 000300 0001f0 00  AX  0   0 16
      [13] .fini             PROGBITS        080484f0 0004f0 00001b 00  AX  0   0  4
      [14] .rodata           PROGBITS        0804850c 00050c 000025 00   A  0   0  4
      [15] .data             PROGBITS        08049534 000534 00000c 00  WA  0   0  4 
      [16] .eh_frame         PROGBITS        08049540 000540 000004 00   A  0   0  4
      [17] .dynamic          DYNAMIC         08049544 000544 0000c8 08  WA  5   0  4
      [18] .ctors            PROGBITS        0804960c 00060c 000008 00  WA  0   0  4
      [19] .dtors            PROGBITS        08049614 000614 000008 00  WA  0   0  4
      [20] .jcr              PROGBITS        0804961c 00061c 000004 00  WA  0   0  4
      [21] .got              PROGBITS        08049620 000620 00001c 04  WA  0   0  4
      [22] .bss              NOBITS          0804963c 00063c 000004 00  WA  0   0  4
      [23] .comment          PROGBITS        00000000 00063c 00007e 00      0   0  1
      [24] .debug_aranges    PROGBITS        00000000 0006c0 000058 00      0   0  8
      [25] .debug_pubnames   PROGBITS        00000000 000718 000025 00      0   0  1
      [26] .debug_info       PROGBITS        00000000 00073d 00096e 00      0   0  1
      [27] .debug_abbrev     PROGBITS        00000000 0010ab 000124 00      0   0  1
      [28] .debug_line       PROGBITS        00000000 0011cf 0001ca 00      0   0  1
      [29] .debug_str        PROGBITS        00000000 001399 00065f 01  MS  0   0  1
      [30] .shstrtab         STRTAB          00000000 0019f8 00011e 00      0   0  1
      [31] .symtab           SYMTAB          00000000 002040 0006b0 10     32  82  4
      [32] .strtab           STRTAB          00000000 0026f0 000341 00      0   0  1
     Key to Flags:
      W (write), A (alloc), X (execute), M (merge), S (strings)
      I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
      O (extra OS processing required) o (OS specific), p (processor specific)

hexdump输出如下：

    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ hexdump -s 0x514 -C ./mycrk -n 16
    00000514  54 79 70 65 20 63 64 2d  6b 65 79 3a 20 00 25 64  |Type cd-key: .%d|
    00000524
    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$

当然，用一个二进制编辑器或者其他工具也可以。

实际上对于一个更复杂的程序，一般不是从程序反汇编内容去找字符串，而是知道了字符串，再去找引用它的地方，这样才能快速定位相关内容。

最后，为了完整起见，我们来输入正确的key，即0x5b117 = 5968496，拿到隐藏的关键信息完成任务：

    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ ./mycrk
    Type cd-key: 5968496
    73313
    foxsen@foxsen-pc:~/汇编教案/crackme/level1/mycrk$ 

以上不复杂，但还是有不少人工的事情，能不能更简单呢？用更强大的工具可以[用IDA Pro](ida.md)。
