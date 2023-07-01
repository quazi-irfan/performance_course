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
; LISTING 39
; ========================================================================

bits 16

; Register-to-register
mov si, bx 0 10001001 11011110
mov dh, al 2 10001000 11000110

; 8-bit immediate-to-register
mov cl, 12 4 10110001 00001100
mov ch, -12 6 10110101 11110100

; 16-bit immediate-to-register
mov cx, 12 8 10111001 00001100 00000000
mov cx, -12 11 10111001 11110100 11111111
mov dx, 3948 14 10111010 01101100 00001111
mov dx, -3948 17 10111010 10010100 11110000

; Source address calculation
mov al, [bx + si] 19 10001010 00000000
mov bx, [bp + di] 21 10001011 00011011
mov dx, [bp] 23 10001011 01010110 00000000

; Source address calculation plus 8-bit displacement
mov ah, [bx + si + 4] 26 10001010 01100000 00000100

; Source address calculation plus 16-bit displacement
mov al, [bx + si + 4999] 29 10001010 10000000 10000111 00010011

; Dest address calculation
mov [bx + di], cx 33 10001001 00001001
mov [bp + si], cl 35 10001000 00001010
mov [bp], ch 37 10001000 01101110 00000000
