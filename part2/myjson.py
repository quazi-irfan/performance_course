# json = object | array
# object = '{' member *(',' member) '}'
#     member = string ':' value
#         string = '"' *char '"'
#             char = unescaped | '\' ('\' | '/' | 'b' | 'f' | 'n' | 'n' | 'r' | 't' | 'u' hex hex hex hex)
#                 unescaped = %x20-21 | %x23-5B | %x5D-10FFFF
#         value = object | array | number | string | 'true' | 'false' | 'null'
#             array = '[' value *(',' value) ] ']'
#             number = [ '-' ] int [ frac ] [ exp ]
#                 frac = '.' 1*digit
#                 exp = e [ minus / plus ] 1*DIGIT
#
#
# json = element
#     element = ws value ws
#         ws = '' | '0020' ws | '000A' ws | '000D' ws | '0009' ws
#         value = object | array | string | number | 'true' | 'false' | 'null'
#             object = '{' ws '}' | '{' members '}'
#                 members = member | member ',' members
#                     member = ws string ws ':' element
#             array = '[' ws ']' | '[' members ']'
#             string = '"' characters '"'
#                 characters = '' | character characters
#                     character = '0020' . '10FFFF' - '"' - '\' | '\' escape
#                         escape = '"' | '\' | '/' | 'b' | 'f' | 'n' | 'n' | 'r' | 't' | 'u' hex hex hex hex
#                             hex = digit | 'A'.'F' | 'a'.'f'
#                                 digit = '0' | onenine
#                                     onenine = '1'.'9'
#             number = integer fraction exponent
#                 integer = digit | onenine digits | '-' digit | '-' onenine digits
#                     digits = digit | digit digits
#                 fraction = '' | '.' digits
#                 exponent = '' | 'E' sign digits | 'e' sign digits
#                     sign = '' | '+' | '-'


# import functools
# n = functools.partial(f.read, 1)
# n = lambda: f.read(1)

# int(int , str) -> int
# int('0020', 16) -> 32
# int('0x0020', 16) -> 32
# int('0x0000', 16) <= ord(' ') <= int('0x10FFFF', 16)

# ord(str) -> int
# ord(' ') -> 32
# ord('A') -> 65
# ord('র') -> 2480

# hex(int) -> str
# hex(255) -> '0xff'

# chr(int) -> str
# chr(0x0020) ' '
# chr(0x10FFFF) '\U0010ffff'
# chr(0) '0x00'
# chr(32) ' '
# chr(1_114_111) '\U0010ffff'

# JSON RFC https://www.ietf.org/rfc/rfc4627.txt
# conversion table https://docs.python.org/3/library/json.html#json-to-py-table

# with open('json_points', encoding='utf-8') as f:
#     d = f.read()

d = ''
i = 0
s = i

def check(d, i, c):
    return True if i < len(d) and d[i] in c else False

def consume_ws():
    global d, i, s
    while check(d, i, ('\u0020', '\u000A', '\u000D', '\u0009')):
        s = s + 1
        i = i + 1


# number = ['-'] int [frac] [exp]
#   int = '0' | (onenine * zeronine)
#       onenine = ['1','2','3','4','5','6','7','8','9']
#       zeronine = ['0','1','2','3','4','5','6','7','8','9']
#   frac = '.' 1*zeronine
#   exp = ['e'|'E'] ['-'|'+'] 1*zeronine
def number():
    global d, i, s
    consume_ws()
    if check(d, i, '-'):
        i = i + 1
    jint()
    frac()
    exp()

    # convert to python type
    if '.' not in d[s:i]:
        if 'e' in d[s:i]:
            base = int(d[s:d[s:i].find('e')])
            exponent = int(d[d[s:i].find('e')+1:i])
            val = int(base * 10 ** exponent)
        else:
            val = int(d[s:i])
    else:
        val = float(d[s:i])
    s = i
    return val


def jint():
    global d, i, s
    if check(d, i, '0'):
        i = i + 1
        return
    elif check(d, i, list(map(str, range(1, 10)))):
        i = i + 1
        while check(d, i, list(map(str, range(10)))):
            i = i + 1


def frac():
    global d, i, s
    if check(d, i, '.'):
        i = i + 1
        if check(d, i, list(map(str, range(10)))):
            i = i + 1 # else ERROR
            while check(d, i, list(map(str, range(10)))):
                i = i + 1


def exp():
    global d, i, s
    if check(d, i, ('e','E')):
        i = i + 1
        if check(d, i, ('-','+')):
            i = i + 1
            if check(d, i, list(map(str, range(10)))):
                i = i + 1 # else ERROR
                while check(d, i, list(map(str, range(10)))):
                    i = i + 1


def string():
    global d, i, s
    consume_ws()
    if check(d, i, '"'):
        i = i + 1; s = s + 1
        val = char()
        if check(d, i, '"'):
            i = i + 1; s = s + 1
            return val


def char():
    global d, i, s
    while int('0x0000', 16) <= ord(d[i]) <= int('0x10FFFF', 16) and d[i] not in ('"', "\\"):
        i = i + 1

    val = str(d[s:i])
    s = i
    return val
    # if d[i] == '\\':
    #     i = i + 1
    #     if check(d, i, ('"','\\','/','b','f','n','r','t','u')):
    #         if check(d, i, 'u'):
    #             i = i + 4


def json():
    global d, i, s
    if check(d, i, '{'):
        val = jobject()
    else:
        val = jarray()

    return val


def jobject():
    global d, i, s
    result = {} # convert to python type
    if check(d, i, '{'):
        i = i + 1; s = s + 1
        result.update(member())
        while check(d, i, ','):
            i = i + 1; s = s + 1
            result.update(member())
        if check(d, i, '}'):
            i = i + 1; s = s + 1
    return result

def jarray():
    global d, i, s
    result = [] # convert to python type
    if check(d, i, '['):
        i = i + 1; s = s + 1
        result.append(value())
        while check(d, i, ','):
            i = i + 1; s = s + 1
            result.append(value())
        if check(d, i, ']'):
            i = i + 1; s = s + 1
    return result

def member():
    global d, i, s
    k = string()
    if check(d, i, ':'):
        i = i + 1; s = s + 1
        v = value()
    return {k: v}


def value():
    global d, i, s
    consume_ws()
    if check(d, i, '{'):
        val = jobject()
    elif check(d, i, '['):
        val = jarray()
    elif check(d, i, '"'):
        val = string()
    elif check(d, i, list(map(str, range(10))) + ['-']):
        val = number()
    elif check(d, i, ('t', 'f','n')):
        if d[i:i+4] == 'true':
            i = i + 4; s = s + 4
            val = True
        elif d[i:i+5] == 'false':
            i = i + 5; i = i + 5
            val = False
        elif d[i:i+4] == 'null':
            i = i + 4; s = s + 4
            val = None
    consume_ws()
    return val


def loads(data):
    global d, i, s
    d = data
    i = 0
    s = i
    return json()

# py_dict = json()
# print(len(py_dict['pairs']))






