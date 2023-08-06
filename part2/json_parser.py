from enum import Enum, auto

class Token_Type(Enum):
    open_brace = auto()
    open_bracket = auto()
    close_brace = auto()
    close_bracket = auto()
    comma = auto()
    colon = auto()
    semi_colon = auto()
    string_literal = auto()
    number = auto()
    true = auto()
    false = auto()
    null = auto()


class Json_Token:
    def __init__(self, type, value):
        self.type, self.value = type, value

# takes the json_content and parse
def get_next_token():
    global content, pos

    while pos < len(content) and content[pos] in ('\u0020', '\u000A', '\u000D', '\u0009'):
        pos += 1

    if content[pos] == '{':
        pos += 1
        return Json_Token(Token_Type.open_brace, '{')

    elif content[pos] == '}':
        pos += 1
        return Json_Token(Token_Type.close_brace, '}')

    elif content[pos] == '[':
        pos += 1
        return Json_Token(Token_Type.open_bracket, '[')

    elif content[pos] == ']':
        pos += 1
        return Json_Token(Token_Type.close_bracket, ']')

    elif content[pos] == ',':
        pos +=1
        return Json_Token(Token_Type.comma, ',')

    elif content[pos] == ';':
        pos += 1
        return Json_Token(Token_Type.semi_colon, ';')

    elif content[pos] == ':':
        pos += 1
        return Json_Token(Token_Type.colon, ':')

    elif content[pos] == 'f':
        pos += 5
        return Json_Token(Token_Type.false, False)

    elif content[pos] == 't':
        pos += 4
        return Json_Token(Token_Type.true, True)

    elif content[pos] == 'n':
        pos += 4
        return Json_Token(Token_Type.null, None)

    elif content[pos] == '"':
        pos += 1
        start = pos
        while pos < len(content) and int('0x0000', 16) <= ord(content[pos]) <= int('0x10FFFF', 16) and content[pos] not in ('"', "\\"):
            pos += 1
        pos += 1

        return Json_Token(Token_Type.string_literal, str(content[start:pos-1]))

    elif content[pos] in ('-','0','1','2','3','4', '5','6','7','8','9'):
        start = pos

        pos += 1
        while pos < len(content) and content[pos] in ('0','1','2','3','4', '5','6','7','8','9', '.', 'e'):
            pos += 1

        if '.' in content[start:pos]:
            value = float(eval(content[start:pos]))
        else:
            value = int(eval(content[start:pos]))

        return Json_Token(Token_Type.number, value)


def ParseJSONObject():
    result = dict()
    next_token = get_next_token()
    while next_token.type != Token_Type.close_brace:
        if next_token.type == Token_Type.string_literal:
            label = next_token.value

            next_token = get_next_token()
            if next_token.type == Token_Type.colon:
                next_token = get_next_token()
                value = ParseJSONElement(next_token)

        result.update({label : value})
        next_token = get_next_token()
    return result


def ParseJSONList():
    result = list()
    next_token = get_next_token()
    while next_token.type != Token_Type.close_bracket:
        result.append(ParseJSONElement(next_token))
        next_token = get_next_token()
        while next_token.type == Token_Type.comma:
            next_token = get_next_token()
            result.append(ParseJSONElement(next_token))
            next_token = get_next_token()
    return result


def ParseJSONElement(token):
    if token.type == Token_Type.open_brace:
        return ParseJSONObject()
    elif token.type == Token_Type.open_bracket:
        return ParseJSONList()
    elif token.type in (Token_Type.true, Token_Type.false, Token_Type.null, Token_Type.number, Token_Type.string_literal):
        return token.value

# content = ''
# pos = 0

def loads(input):
    global content, pos
    content = input
    pos = 0
    first_token = get_next_token()
    json_dict = ParseJSONElement(first_token)
    return json_dict
