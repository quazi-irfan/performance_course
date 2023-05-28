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

def getbit(val, *rng, bit_len=8) -> str:
    if len(rng) == 1:
        return getbit(val, rng[0], rng[0]+1, bit_len=bit_len)

    result = ''
    for i in range(rng[0], rng[1]):
        result += str((val & (1 << ((bit_len-1)-i))) >> ((bit_len-1)-i))
    return result


def getSignedVal(val, bit_length):
    return val if val < 2 ** (bit_length-1) else -(2 ** bit_length - val)


def getmodrm(mod, rm, content, i):
    if mod == '00' and rm == '110':
        temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
        return '[' + str(temp) + ']', i + 2
    else:
        if mod == '00':
            return '['+ reg_dict_rm[rm] + ']', i
        elif mod == '01':
            temp = getSignedVal(content[i + 1], 8)
            return '[' + reg_dict_rm[rm] + (str(temp) if temp < 0 else ' + ' + str(temp)) + ']', i + 1
        elif mod == '10':
            temp = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
            return '[' + reg_dict_rm[rm] + (str(temp) if temp < 0 else ' + ' + str(temp)) + ']', i + 2

def readAssembled(fileName, offset = 0):
    with open(fileName, mode='rb', buffering=0) as f:
        content = f.read()

    content = content[offset:]

    asm_out = [['bits 16']]

    i = -1
    while i < len(content) - 1:
        i = i + 1
        start_ip = i

        # MOV Register/Memory to/from Register
        #   Register to/from Register; mov ax, bx
        #   Memory to Register; mov ax, [bx + di - 37] LOAD FROM MEMORY
        #   Memory from Register; mov [si - 300], cx STORE TO MEMORY
        # ADD Register/memory with Register to either
        # SUB Register/Memory and Register to either
        # CMP Register/Memory and Register
        if getbit(content[i], 0, 6) in ('100010','000000','001010','001110'):
            fb, sb = f'{format(content[i], "b"):0>8}', f'{format(content[i+1], "b"):0>8}'
            i = i + 1
            opcode, d, w = fb[:6], fb[6], fb[7]
            mod, reg, rm = sb[:2], sb[2:5], sb[5:]

            dest = reg_dict[(reg, w)]
            if mod in ('00', '01', '10'):
                src, i = getmodrm(mod, rm, content, i)
            elif mod == '11':
                src = reg_dict[(rm, w)]

            if d == '0':
                dest, src = src, dest

            temp_opcode = {'100010':'mov', '000000':'add','001010':'sub','001110':'cmp' }
            asm_out.append([temp_opcode[opcode], dest, src, i - start_ip + 1])
            # print(temp_opcode[opcode] + dest + ',' + src, file=asm_out)

        # MOV Immediate to Register/Memory
        #   Immediate to Register; mov ax, 10
        #   Immediate to Memory; mov [di + 901], word 347 STORE TO MEMORY
        elif getbit(content[i], 0, 7) == '1100011':
            w, mod, rm = getbit(content[i], 7), getbit(content[i+1], 0, 2), getbit(content[i+1], 5, 8)
            i = i + 1
            dest, i = getmodrm(mod, rm, content, i)
            if w == '0':
                src = str(getSignedVal(content[i+1], 8)) # 'byte ' + str(getSignedVal(content[i+1], 8))
                i = i + 1
            else:
                src = str(getSignedVal(content[i+2] << 8 | content[i+1], 16)) # 'word ' + str(getSignedVal(content[i+2] << 8 | content[i+1], 16))
                i = i + 2

            asm_out.append(['mov', dest, src,i - start_ip + 1])
            # print('mov ' + dest + ', ' + src, file=asm_out)

        # MOV immediate to register mov cx, 12; mov dx, -3948
        elif getbit(content[i], 0, 4) == '1011':
            w, reg = getbit(content[i], 4), getbit(content[i], 5, 8)
            dest = reg_dict[(reg, w)]

            if w == '0':
                imm = getSignedVal(content[i+1], 8)
                i = i + 1
            else:
                temp_val = (content[i+2] << 8) | content[i+1]
                imm = getSignedVal(temp_val, 16)
                i = i + 2

            asm_out.append(['mov', dest, str(imm),i - start_ip + 1])
            # print('mov ' + dest + ',' + str(imm), file=asm_out)

        # MOV Memory to accumulator
        elif getbit(content[i], 0, 7) == '1010000': # does not handle al/ah
            w = getbit(content[i], 7)
            if w == '0':
                src = getSignedVal(content[i+1], 8)
                i = i + 1
            else:
                src = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
                i = i + 2

            asm_out.append(['mov', 'ax', '[' + str(src) + ']',i - start_ip + 1])
            # print('mov ax , [' + str(src) + ']', file=asm_out)

        # MOV Accumulator to Memory
        elif getbit(content[i], 0, 7) == '1010001': # does not handle al/ah
            w = getbit(content[i], 7)
            if w == '0':
                dest = getSignedVal(content[i+1], 8)
                i = i + 1
            else:
                dest = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
                i = i + 2

            asm_out.append(['mov', '[' + str(dest) + ']', 'ax',i - start_ip + 1])
            # print('mov [' + str(dest) + '], ax', file=asm_out)

        # ADD Immediate to Register/Memory
        # SUB Immediate to Register/Memory
        # CMP Immediate to Register/Memory
        elif getbit(content[i], 0, 6) == '100000':
            s, w = getbit(content[i], 6), getbit(content[i], 7)
            mod, marker, rm = getbit(content[i+1], 0, 2), getbit(content[i+1], 2, 5), getbit(content[i+1], 5, 8)
            i = i + 1

            dest = reg_dict[(rm, w)]
            if mod in ('00', '01', '10'):
                dest, i = getmodrm(mod, rm, content, i)
                if s == '0' and w == '1':
                    src = getSignedVal((content[i+2] << 8) | content[i+1], 16)
                    i = i + 2
                else:
                    src = getSignedVal(content[i + 1], 8)
                    i = i + 1
            elif mod == '11':
                if s+w == '01':
                    src = getSignedVal((content[i+2] << 8) | content[i+1], 16)
                    i = i + 2
                else:
                    src = getSignedVal(content[i + 1], 8)
                    i = i + 1

            src = str(src) # 'byte ' + str(src) if w == '0' else 'word ' + str(src)

            temp_opcode_2 = {'000':'add', '101':'sub', '111':'cmp'}
            asm_out.append([temp_opcode_2[marker], dest, str(src),i - start_ip + 1])
            # print(temp_opcode_2[marker] + dest + ', ' + str(src), file=asm_out)

        # ADD Immediate to Accumulator
        # SUB Immediate to Accumulator
        # CMP Immediate to Accumulator
        elif getbit(content[i], 0, 7) in ('0000010','0010110','0011110'):
            opcode, w = getbit(content[i], 0, 7), getbit(content[i], 7)
            if w == '0':
                dest = 'al'
                src = getSignedVal(content[i+1], 8)
                i = i + 1
            else: # Never happens for CMP
                dest = 'ax'
                src = getSignedVal((content[i + 2] << 8) | content[i + 1], 16)
                i = i + 2

            temp_opcode_3 = {'0000010':'add','0010110':'sub','0011110':'cmp'}
            asm_out.append([temp_opcode_3[opcode], dest, str(src),i - start_ip + 1])
            # print(temp_opcode_3[opcode] + dest + ', ' + str(src), file=asm_out)

        else:
            temp_opcode_4 ={
                '01110100': 'je', # jz
                '01111100': 'jl', # jnge
                '01111110': 'jle', # jng
                '01110010': 'jb', # jnae
                '01110110': 'jbe', # jan
                '01111010': 'jp', # jpe
                '01110000': 'jo',
                '01111000': 'js',
                '01110101': 'jnz', # jne
                '01111101': 'jnl', # jge
                '01111111': 'jnle', # jg
                '01110011': 'jnb', # jae
                '01110111': 'jnbe', # ja
                '01111011': 'jnp', # jpo
                '01110001': 'jno',
                '01111001': 'jns',
                '11100010': 'loop',
                '11100001': 'loopz', #loope
                '11100000': 'loopnz', #loopne
                '11100011': 'jcxz'
            }
            opcode = getbit(content[i], 0, 8)
            dest = str(getSignedVal(content[i+1], 8))
            i = i + 1
            asm_out.append([temp_opcode_4[opcode], dest, i - start_ip + 1])
            # print(temp_opcode_4[getbit(content[i], 0, 8)] + ' ' + dest, file=asm_out)

    return asm_out


if __name__ == '__main__':
    decoded = readAssembled('listing_0051_memory_mov', offset = 0)
    print(*decoded, sep='\n')