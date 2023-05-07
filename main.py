# Most instruction can take their operand either from register, memory or from constant
# ASM-86 instruction
# MOV <des> <src>
# Length vary form 1 to 6 bytes
# 1 byte length mov instruction only work on register
# First two byte contains all information regarding decoding longer instruction
# first 6 bit indicates the assembly instruction
# if D bit is 0 then instruction <src> is at REG contains, otherwise instruction <des> is at REG
# if W bit is 0 then instruction operates on byte data, otherwise word data 

# xxxxxxxuu 11

# R/M depends on how MOD field is set
# since MOD is 11, REG will identify another register

#

reg_dict = {
    ('000', '0'): 'al',
    ('001', '0'): 'cl',
    ('010', '0'): 'dl',
    ('011', '0'): 'bl',
    ('100', '0'): 'ah',
    ('101', '0'): 'ch',
    ('110', '0'): 'dh',
    ('111', '0'): 'bh',

    ('000', '1'): 'ax',
    ('001', '1'): 'cx',
    ('010', '1'): 'dx',
    ('011', '1'): 'bx',
    ('100', '1'): 'sp',
    ('101', '1'): 'bp',
    ('110', '1'): 'si',
    ('111', '1'): 'di'
}

reg_dict_rm = {
    '000': 'bx + si',
    '001': 'bx + di',
    '010': 'bp + si',
    '011': 'bp + di',
    '100': 'si',
    '101': 'di',
    '110': 'bp',
    '111': 'bx',
}

def getbit(val, *rng):
    if len(rng) == 1:
        return getbit(val, rng[0], rng[0]+1)

    result = ''
    for i in range(rng[0], rng[1]):
        result += str((val & (1 << (7-i))) >> (7-i))
    return result


def getSignedVal(val, bit_length=8):
    return val if val < 2 ** (bit_length-1) else -(2 ** bit_length - val)


def getmodrm(mod, rm, content, i):
    if rm != '110':
        if mod == '00':
            return '['+ reg_dict_rm[rm] + ']', i
        elif mod == '01':
            temp = getSignedVal(content[i + 1])
            return '[' + reg_dict_rm[rm] + (str(temp) if temp < 0 else ' + ' + str(temp)) + ']', i + 1
        elif mod == '10':
            temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
            return '[' + reg_dict_rm[rm] + (str(temp) if temp < 0 else ' + ' + str(temp)) + ']', i + 2
    else:
        temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
        return '[' + str(temp) + ']', i + 2


with open('listing_0040_challenge_movs', mode='rb', buffering=0) as f:
    content = f.read() # returns a class <'bytes'>; content[0] returns int\

# content = content[19:]
# print(list(map(bin, content)))
# exit(0)
# content = content[27:]
result = ['bits 16']

i = -1
while i < len(content) - 1:
    i = i + 1

    if getbit(content[i], 0, 6) == '100010' or getbit(content[i], 0, 7) == '1100011' or getbit(content[i], 0, 4) == '1011' or getbit(content[i], 0, 7) == '1010000'or getbit(content[i], 0, 7) == '1010001'or getbit(content[i], 0, 8) == '10001110' or getbit(content[i], 0, 8) == '10001100':

        # MOVE DESTINATION SOURCE
        if getbit(content[i], 0, 6) == '100010':
            fb, sb = f'{format(content[i], "b"):0>8}', f'{format(content[i+1], "b"):0>8}'
            i = i + 1
            opcode, d, w = fb[:6], fb[6], fb[7]
            mod, reg, rm = sb[:2], sb[2:5], sb[5:]

            # dest = reg_dict[(reg, w)] if d == '1' else reg_dict[(rm, w)]

            dest = reg_dict[(reg, w)]
            if mod in ('00', '01', '10'):
                src, i = getmodrm(mod, rm, content, i)
            elif mod == '11':
                src = reg_dict[(rm, w)]

            if d == '0':
                dest, src = src, dest

            print('mov ' + dest + ',' + src)
            # result.append('mov ' + dest + ',' + src)

        elif getbit(content[i], 0, 7) == '1100011':
            w, mod, rm = getbit(content[i], 7), getbit(content[i+1], 0, 2), getbit(content[i+1], 5, 8)
            i = i + 1
            dest, i = getmodrm(mod, rm, content, i)
            if w == '0':
                src = 'byte ' + str(getSignedVal(content[i+1]))
                i = i + 1
            else:
                src = 'word ' + str(getSignedVal(content[i+2] << 8 | content[i+1], 16))
                i = i + 2

            print('mov ' + dest + ', ' + src)

        elif getbit(content[i], 0, 4) == '1011':
            w, reg = getbit(content[i], 4), getbit(content[i], 5, 8)
            dest = reg_dict[(reg, w)]

            if w == '0':
                imm = getSignedVal(content[i+1])
                i = i + 1
            else:
                temp_val = (content[i+2] << 8) | content[i+1]
                imm = getSignedVal(temp_val, 16)
                i = i + 2

            print('mov ' + dest + ',' + str(imm))
            # result.append('mov ' + dest + ',' + str(imm))

        elif getbit(content[i], 0, 7) == '1010000':
            w = getbit(content[i], 7)
            if w == '0':
                temp = getSignedVal(content[i+1])
                i = i + 1
            else:
                temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
                i = i + 2

            print('mov ax , [' + str(temp) + ']')

        elif getbit(content[i], 0, 7) == '1010001':
            w = getbit(content[i], 7)
            if w == '0':
                temp = getSignedVal(content[i+1])
                i = i + 1
            else:
                temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
                i = i + 2

            print('mov [' + str(temp) + '], ax')

# with open('output.asm', 'w') as o:
#     print(*result, file=o, sep='\n')