from tokens import *
from utilities import *
import re

def guteLex(program):
    STDOUT(f'LEXER:')

    buffer = []
    tokens = []
    matches = []
    # curr_col = 1
    curr_line = 1
    # comment_len = 0
    string_mode = False
    comment_mode = False
    # ignored_comment = False
    need_newline = False
    newline = '\n'
    whitespace = ' '
    string_quote = '"'
    comment_block = set(('/*', '*/'))
    lookahead = set(('=','!'))
    valid_tokens, token_kinds = grammarDict()
    tokenize = set(('$','"','{','}','(',')','=','==','!='))
    program = program.translate({ord('\t'): '  ', ord('\r'): '\n'})

    def parseError(error_message):
        STDERR(f'Lexer Error: {error_message} | Line: {curr_line}')

    
    program = [*program]

    while program or buffer:
        if not program:
            if not matches:
                parseError(f'Invalid Character {repr(buffer[0])}')
                return
                
            token = spawnToken(matches, token_kinds, valid_tokens,curr_line)
            tokens.append(token)
           

            t_len = len(tokens[-1].value)
            if (buffer[0] == tokens[-1].value):
                del buffer[0]
            else:
                del buffer[:t_len]

            program = program + buffer
            buffer = []
            matches = []

            continue

        next_char = program.pop(0)
        next_next_char = program[0] if 0 < len(program) else None

        if f'{next_char}{next_next_char}' in comment_block:
            comment_mode = not comment_mode
            del program[0]
            continue 

        if comment_mode:
            if next_char == newline:
                curr_line += 1
            continue

        if next_char == whitespace and not string_mode:
            if not buffer:
                continue
            
            if not matches:
                parseError(f'Invalid Character {repr(buffer[0])}')
                return

            token = spawnToken(matches, token_kinds, valid_tokens, curr_line)
            tokens.append(token)

            t_len = len(tokens[-1].value)
            if (buffer[0] == tokens[-1].value):
                del buffer[0]
            else:
                del buffer[:t_len]

            program = buffer + program
            buffer = []
            matches = []

            continue

        if next_char == newline and not string_mode:
            if not buffer:
                curr_line += 1
                continue

            if not matches:
                parseError(f'Invalid Character {repr(buffer[0])}')
                return

            token = spawnToken(matches, token_kinds, valid_tokens, curr_line)
            tokens.append(token)

            curr_line += 1


            t_len = len(tokens[-1].value)
            if (buffer[0] == tokens[-1].value):
                del buffer[0]
            else:
                del buffer[:t_len]

            program = buffer + program
            buffer = []
            matches = []
            continue  

        if next_char in lookahead:
            if f'{next_char}{next_next_char}' in tokenize:
                next_char = f'{next_char}{program.pop(0)}'
                next_next_char = program[0] if 0 < len(program) else None

        if buffer and next_char in tokenize:
            # Make a token
            if not matches:
                parseError(f'Invalid Character {repr(buffer[0])}')
                return

            token = spawnToken(matches, token_kinds,valid_tokens, curr_line)
            tokens.append(token)

            t_len = len(tokens[-1].value)

            if (buffer[0] == tokens[-1].value):
                del buffer[0]
            else:
                del buffer[:t_len]

            program = buffer + [next_char] + program
            buffer = []
            matches = []
            continue
                    
        buffer.append(next_char)

        match = matchToken(''.join(buffer), matches, token_kinds, string_mode)

        if buffer and buffer[-1] == string_quote:
            string_mode = not string_mode
        if match:
            matches.append(match)

    if string_mode:
        parseError('Unterminated string')
        return
    if comment_mode:
        parseError('Unterminated comment')

    return tokens




