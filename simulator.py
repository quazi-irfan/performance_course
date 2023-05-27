import decoder, re

reg = {
    'ax': 0b0000_0000_0000_0000,
    'bx': 0b0000_0000_0000_0000,
    'cx': 0b0000_0000_0000_0000,
    'dx': 0b0000_0000_0000_0000,
    'sp': 0b0000_0000_0000_0000,
    'bp': 0b0000_0000_0000_0000,
    'si': 0b0000_0000_0000_0000,
    'di': 0b0000_0000_0000_0000,
}

flag_reg = {
    't': 0,  # trap
    'd': 0,  # direction
    'i': 0,  # interrupt-enable
    'o': 0,  # overflow
    's': 0,  # sign
    'z': 0,  # zero
    'a': 0,  # auxiliary
    'p': 0,  # parity
    'c': 0   # carry
}

reg_names = ['ax','bx','cx','dx','sp','bp','si','di','ah','al','bh','bl','ch','cl','dh','dl'
             'ss','ds','es']

# from array import array
# reg = array('I', [0,0,0,0,0,0,0,0]) # ax, bx, cx, dx, sp, bp, si, di

decoded = decoder.readAssembled(fileName='listing_0046_add_sub_cmp')

for d in decoded:

    if d[0] == 'mov':
        if d[1] in reg_names and d[2] not in reg_names: # immediate to reg
            if d[1][1] == 'l':
                reg[d[1]] = (reg[d[1]] & 0b11111111_00000000) | d[2]
            elif d[1][1] == 'h':
                reg[d[1]] = (reg[d[1]] & 0b00000000_11111111) | (d[2] << 8)
            else:
                reg[d[1]] = d[2]
        elif d[1] in reg_names and d[2] in reg_names: # reg to reg
            if d[2][1] == 'l':
                val = reg[d[2][0] + 'x'] | 0b00000000_11111111
            elif d[2][1] == 'h':
                val = reg[d[2][0] + 'x'] >> 8
            else:
                val = reg[d[2]]

            if d[1][1] == 'l':
                reg[d[1][0] + 'x'] = (reg[d[1][0] + 'x'] & 0b11111111_00000000) | val
            elif d[1][1] == 'h':
                reg[d[1][0] + 'x'] = (reg[d[1][0] + 'x'] & 0b00000000_11111111) | (val << 8)
            else:
                reg[d[1]] = val
    elif d[0] == 'add':
        if d[2] in reg_names:
            reg[d[1]] = int(reg[d[1]]) + int(reg[d[2]])
        else:
            reg[d[1]] = int(reg[d[1]]) + int(d[2])

        flag_reg['z'] = 0 if reg[d[1]] else 1
        flag_reg['s'] = decoder.getbit(reg[d[1]], 0, bit_len=16)
    elif d[0] == 'sub':
        if d[2] in reg_names:
            reg[d[1]] = int(reg[d[1]]) - int(reg[d[2]])
        else:
            reg[d[1]] = int(reg[d[1]]) - int(d[2])

        flag_reg['z'] = 0 if reg[d[1]] else 1
        flag_reg['s'] = decoder.getbit(reg[d[1]], 0, bit_len=16)
    elif d[0] == 'cmp':
        flag_reg['z'] = 0 if (int(reg[d[1]]) - int(reg[d[2]])) else 1

print(reg)
print(flag_reg)

# add, (cmp, sub) same instruction, cmp is subtract
# sign flag, zero flag zf sf