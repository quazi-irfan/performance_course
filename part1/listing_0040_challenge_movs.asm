; ========================================================================
;
; (C) Copyright 2023 by Molly Rocket, Inc., All Rights Reserved.
;
; This software is provided 'as-is', without any express or implied
; warranty. In no event will the authors be held liable for any damages
; arising from the use of this software.
;
; Please see https://computerenhance.com for further information
;
; ========================================================================

; ========================================================================
; LISTING 40
; ========================================================================

bits 16

; Signed displacements
mov ax, [bx + di - 37]      0 10001011 01000001 11011011
mov [si - 300], cx          3 10001001 10001100 11010100 11111110
mov dx, [bx - 32]           7 10001011 01010111 11100000

; Explicit sizes
mov [bp + di], byte 7       10 11000110 00000011 00000111
mov [di + 901], word 347    13 11000111 10000101 10000101 00000011 01011011 00000001

; Direct address
mov bp, [5]                 19 10001011 00101110 00000101 00000000
mov bx, [3458]              23 10001011 00011110 10000010 00001101

; Memory-to-accumulator test
mov ax, [2555]              27 10100001 11111011 00001001
mov ax, [16]                30 10100001 00010000 00000000

; Accumulator-to-memory test
mov [2554], ax              33 10100011 11111010 00001001
mov [15], ax                36 10100011 00001111 00000000
