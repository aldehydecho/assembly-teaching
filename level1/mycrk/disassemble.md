# 反汇编文件
    mycrk：     文件格式 elf32-i386

    Disassembly of section .init:

    0804829c <_init>:
     804829c:	55                   	push   %ebp
     804829d:	89 e5                	mov    %esp,%ebp
     804829f:	83 ec 08             	sub    $0x8,%esp
     80482a2:	e8 7d 00 00 00       	call   8048324 <call_gmon_start>
     80482a7:	e8 e4 00 00 00       	call   8048390 <frame_dummy>
     80482ac:	e8 0f 02 00 00       	call   80484c0 <__do_global_ctors_aux>
     80482b1:	c9                   	leave  
     80482b2:	c3                   	ret    

    Disassembly of section .plt:

    080482b4 <scanf@plt-0x10>:
     80482b4:	ff 35 24 96 04 08    	pushl  0x8049624
     80482ba:	ff 25 28 96 04 08    	jmp    *0x8049628
     80482c0:	00 00                	add    %al,(%eax)
        ...

    080482c4 <scanf@plt>:
     80482c4:	ff 25 2c 96 04 08    	jmp    *0x804962c
     80482ca:	68 00 00 00 00       	push   $0x0
     80482cf:	e9 e0 ff ff ff       	jmp    80482b4 <_init+0x18>

    080482d4 <__libc_start_main@plt>:
     80482d4:	ff 25 30 96 04 08    	jmp    *0x8049630
     80482da:	68 08 00 00 00       	push   $0x8
     80482df:	e9 d0 ff ff ff       	jmp    80482b4 <_init+0x18>

    080482e4 <printf@plt>:
     80482e4:	ff 25 34 96 04 08    	jmp    *0x8049634
     80482ea:	68 10 00 00 00       	push   $0x10
     80482ef:	e9 c0 ff ff ff       	jmp    80482b4 <_init+0x18>

    Disassembly of section .text:

    08048300 <_start>:
     8048300:	31 ed                	xor    %ebp,%ebp
     8048302:	5e                   	pop    %esi
     8048303:	89 e1                	mov    %esp,%ecx
     8048305:	83 e4 f0             	and    $0xfffffff0,%esp
     8048308:	50                   	push   %eax
     8048309:	54                   	push   %esp
     804830a:	52                   	push   %edx
     804830b:	68 80 84 04 08       	push   $0x8048480
     8048310:	68 50 84 04 08       	push   $0x8048450
     8048315:	51                   	push   %ecx
     8048316:	56                   	push   %esi
     8048317:	68 c4 83 04 08       	push   $0x80483c4
     804831c:	e8 b3 ff ff ff       	call   80482d4 <__libc_start_main@plt>
     8048321:	f4                   	hlt    
     8048322:	90                   	nop
     8048323:	90                   	nop

    08048324 <call_gmon_start>:
     8048324:	55                   	push   %ebp
     8048325:	89 e5                	mov    %esp,%ebp
     8048327:	53                   	push   %ebx
     8048328:	e8 00 00 00 00       	call   804832d <call_gmon_start+0x9>
     804832d:	5b                   	pop    %ebx
     804832e:	81 c3 f3 12 00 00    	add    $0x12f3,%ebx
     8048334:	50                   	push   %eax
     8048335:	8b 83 18 00 00 00    	mov    0x18(%ebx),%eax
     804833b:	85 c0                	test   %eax,%eax
     804833d:	74 02                	je     8048341 <call_gmon_start+0x1d>
     804833f:	ff d0                	call   *%eax
     8048341:	8b 5d fc             	mov    -0x4(%ebp),%ebx
     8048344:	c9                   	leave  
     8048345:	c3                   	ret    
     8048346:	90                   	nop
     8048347:	90                   	nop
     8048348:	90                   	nop
     8048349:	90                   	nop
     804834a:	90                   	nop
     804834b:	90                   	nop
     804834c:	90                   	nop
     804834d:	90                   	nop
     804834e:	90                   	nop
     804834f:	90                   	nop

    08048350 <__do_global_dtors_aux>:
     8048350:	55                   	push   %ebp
     8048351:	89 e5                	mov    %esp,%ebp
     8048353:	83 ec 08             	sub    $0x8,%esp
     8048356:	80 3d 3c 96 04 08 00 	cmpb   $0x0,0x804963c
     804835d:	75 2d                	jne    804838c <__do_global_dtors_aux+0x3c>
     804835f:	a1 3c 95 04 08       	mov    0x804953c,%eax
     8048364:	8b 10                	mov    (%eax),%edx
     8048366:	85 d2                	test   %edx,%edx
     8048368:	74 1b                	je     8048385 <__do_global_dtors_aux+0x35>
     804836a:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi
     8048370:	83 c0 04             	add    $0x4,%eax
     8048373:	a3 3c 95 04 08       	mov    %eax,0x804953c
     8048378:	ff d2                	call   *%edx
     804837a:	a1 3c 95 04 08       	mov    0x804953c,%eax
     804837f:	8b 10                	mov    (%eax),%edx
     8048381:	85 d2                	test   %edx,%edx
     8048383:	75 eb                	jne    8048370 <__do_global_dtors_aux+0x20>
     8048385:	c6 05 3c 96 04 08 01 	movb   $0x1,0x804963c
     804838c:	c9                   	leave  
     804838d:	c3                   	ret    
     804838e:	89 f6                	mov    %esi,%esi

    08048390 <frame_dummy>:
     8048390:	55                   	push   %ebp
     8048391:	89 e5                	mov    %esp,%ebp
     8048393:	83 ec 08             	sub    $0x8,%esp
     8048396:	a1 1c 96 04 08       	mov    0x804961c,%eax
     804839b:	85 c0                	test   %eax,%eax
     804839d:	74 21                	je     80483c0 <frame_dummy+0x30>
     804839f:	b8 00 00 00 00       	mov    $0x0,%eax
     80483a4:	85 c0                	test   %eax,%eax
     80483a6:	74 18                	je     80483c0 <frame_dummy+0x30>
     80483a8:	83 ec 0c             	sub    $0xc,%esp
     80483ab:	68 1c 96 04 08       	push   $0x804961c
     80483b0:	e8 4b 7c fb f7       	call   0 <_init-0x804829c>
     80483b5:	83 c4 10             	add    $0x10,%esp
     80483b8:	90                   	nop
     80483b9:	8d b4 26 00 00 00 00 	lea    0x0(%esi,%eiz,1),%esi
     80483c0:	89 ec                	mov    %ebp,%esp
     80483c2:	5d                   	pop    %ebp
     80483c3:	c3                   	ret    

    080483c4 <main>:
     80483c4:	55                   	push   %ebp
     80483c5:	89 e5                	mov    %esp,%ebp
     80483c7:	83 ec 18             	sub    $0x18,%esp
     80483ca:	83 e4 f0             	and    $0xfffffff0,%esp
     80483cd:	b8 00 00 00 00       	mov    $0x0,%eax
     80483d2:	29 c4                	sub    %eax,%esp
     80483d4:	c7 45 fc 67 1e 01 00 	movl   $0x11e67,-0x4(%ebp)
     80483db:	c7 45 f8 70 12 5b 00 	movl   $0x5b1270,-0x8(%ebp)
     80483e2:	c7 45 f0 06 00 00 00 	movl   $0x6,-0x10(%ebp)
     80483e9:	83 ec 0c             	sub    $0xc,%esp
     80483ec:	68 14 85 04 08       	push   $0x8048514
     80483f1:	e8 ee fe ff ff       	call   80482e4 <printf@plt>
     80483f6:	83 c4 10             	add    $0x10,%esp
     80483f9:	83 ec 08             	sub    $0x8,%esp
     80483fc:	8d 45 f4             	lea    -0xc(%ebp),%eax
     80483ff:	50                   	push   %eax
     8048400:	68 22 85 04 08       	push   $0x8048522
     8048405:	e8 ba fe ff ff       	call   80482c4 <scanf@plt>
     804840a:	83 c4 10             	add    $0x10,%esp
     804840d:	8b 45 f8             	mov    -0x8(%ebp),%eax
     8048410:	3b 45 f4             	cmp    -0xc(%ebp),%eax
     8048413:	75 1d                	jne    8048432 <main+0x6e>
     8048415:	8b 55 f0             	mov    -0x10(%ebp),%edx
     8048418:	8d 45 fc             	lea    -0x4(%ebp),%eax
     804841b:	31 10                	xor    %edx,(%eax)
     804841d:	83 ec 08             	sub    $0x8,%esp
     8048420:	ff 75 fc             	pushl  -0x4(%ebp)
     8048423:	68 25 85 04 08       	push   $0x8048525
     8048428:	e8 b7 fe ff ff       	call   80482e4 <printf@plt>
     804842d:	83 c4 10             	add    $0x10,%esp
     8048430:	eb 10                	jmp    8048442 <main+0x7e>
     8048432:	83 ec 0c             	sub    $0xc,%esp
     8048435:	68 29 85 04 08       	push   $0x8048529
     804843a:	e8 a5 fe ff ff       	call   80482e4 <printf@plt>
     804843f:	83 c4 10             	add    $0x10,%esp
     8048442:	b8 00 00 00 00       	mov    $0x0,%eax
     8048447:	c9                   	leave  
     8048448:	c3                   	ret    
     8048449:	90                   	nop
     804844a:	90                   	nop
     804844b:	90                   	nop
     804844c:	90                   	nop
     804844d:	90                   	nop
     804844e:	90                   	nop
     804844f:	90                   	nop

    08048450 <__libc_csu_init>:
     8048450:	55                   	push   %ebp
     8048451:	89 e5                	mov    %esp,%ebp
     8048453:	56                   	push   %esi
     8048454:	53                   	push   %ebx
     8048455:	31 db                	xor    %ebx,%ebx
     8048457:	e8 40 fe ff ff       	call   804829c <_init>
     804845c:	b8 34 95 04 08       	mov    $0x8049534,%eax
     8048461:	2d 34 95 04 08       	sub    $0x8049534,%eax
     8048466:	c1 f8 02             	sar    $0x2,%eax
     8048469:	39 c3                	cmp    %eax,%ebx
     804846b:	73 0f                	jae    804847c <__libc_csu_init+0x2c>
     804846d:	89 c6                	mov    %eax,%esi
     804846f:	90                   	nop
     8048470:	ff 14 9d 34 95 04 08 	call   *0x8049534(,%ebx,4)
     8048477:	43                   	inc    %ebx
     8048478:	39 f3                	cmp    %esi,%ebx
     804847a:	72 f4                	jb     8048470 <__libc_csu_init+0x20>
     804847c:	5b                   	pop    %ebx
     804847d:	5e                   	pop    %esi
     804847e:	5d                   	pop    %ebp
     804847f:	c3                   	ret    

    08048480 <__libc_csu_fini>:
     8048480:	55                   	push   %ebp
     8048481:	b8 34 95 04 08       	mov    $0x8049534,%eax
     8048486:	2d 34 95 04 08       	sub    $0x8049534,%eax
     804848b:	c1 f8 02             	sar    $0x2,%eax
     804848e:	89 e5                	mov    %esp,%ebp
     8048490:	83 ec 08             	sub    $0x8,%esp
     8048493:	89 5d fc             	mov    %ebx,-0x4(%ebp)
     8048496:	85 c0                	test   %eax,%eax
     8048498:	8d 58 ff             	lea    -0x1(%eax),%ebx
     804849b:	75 0b                	jne    80484a8 <__libc_csu_fini+0x28>
     804849d:	8b 5d fc             	mov    -0x4(%ebp),%ebx
     80484a0:	89 ec                	mov    %ebp,%esp
     80484a2:	5d                   	pop    %ebp
     80484a3:	e9 48 00 00 00       	jmp    80484f0 <_fini>
     80484a8:	ff 14 9d 34 95 04 08 	call   *0x8049534(,%ebx,4)
     80484af:	89 d8                	mov    %ebx,%eax
     80484b1:	4b                   	dec    %ebx
     80484b2:	85 c0                	test   %eax,%eax
     80484b4:	75 f2                	jne    80484a8 <__libc_csu_fini+0x28>
     80484b6:	eb e5                	jmp    804849d <__libc_csu_fini+0x1d>
     80484b8:	90                   	nop
     80484b9:	90                   	nop
     80484ba:	90                   	nop
     80484bb:	90                   	nop
     80484bc:	90                   	nop
     80484bd:	90                   	nop
     80484be:	90                   	nop
     80484bf:	90                   	nop

    080484c0 <__do_global_ctors_aux>:
     80484c0:	55                   	push   %ebp
     80484c1:	89 e5                	mov    %esp,%ebp
     80484c3:	53                   	push   %ebx
     80484c4:	52                   	push   %edx
     80484c5:	a1 0c 96 04 08       	mov    0x804960c,%eax
     80484ca:	83 f8 ff             	cmp    $0xffffffff,%eax
     80484cd:	bb 0c 96 04 08       	mov    $0x804960c,%ebx
     80484d2:	74 18                	je     80484ec <__do_global_ctors_aux+0x2c>
     80484d4:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi
     80484da:	8d bf 00 00 00 00    	lea    0x0(%edi),%edi
     80484e0:	83 eb 04             	sub    $0x4,%ebx
     80484e3:	ff d0                	call   *%eax
     80484e5:	8b 03                	mov    (%ebx),%eax
     80484e7:	83 f8 ff             	cmp    $0xffffffff,%eax
     80484ea:	75 f4                	jne    80484e0 <__do_global_ctors_aux+0x20>
     80484ec:	58                   	pop    %eax
     80484ed:	5b                   	pop    %ebx
     80484ee:	5d                   	pop    %ebp
     80484ef:	c3                   	ret    

    Disassembly of section .fini:

    080484f0 <_fini>:
     80484f0:	55                   	push   %ebp
     80484f1:	89 e5                	mov    %esp,%ebp
     80484f3:	53                   	push   %ebx
     80484f4:	e8 00 00 00 00       	call   80484f9 <_fini+0x9>
     80484f9:	5b                   	pop    %ebx
     80484fa:	81 c3 27 11 00 00    	add    $0x1127,%ebx
     8048500:	52                   	push   %edx
     8048501:	e8 4a fe ff ff       	call   8048350 <__do_global_dtors_aux>
     8048506:	8b 5d fc             	mov    -0x4(%ebp),%ebx
     8048509:	c9                   	leave  
     804850a:	c3                   	ret    
