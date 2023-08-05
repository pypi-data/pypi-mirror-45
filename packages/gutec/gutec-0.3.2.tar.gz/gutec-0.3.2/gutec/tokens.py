import re
class Token():
    def __init__(self,type_,value,line_num):
        self.type_ = type_
        self.value = value
        self.line_num = line_num

    def __repr__(self):
        return f'{self.value}'


def grammarDict():
    valid_tokens = {
        # Keywords
        'if': ('(if)(?![\s\S])','T_k_if'),
        'int': ('(int)(?![\s\S])', 'T_k_int'),
        'true': ('(true)(?![\s\S])', 'T_k_true'),
        'false': ('(false)(?![\s\S])', 'T_k_false'),
        'while': ('(while)(?![\s\S])','T_k_while'),
        'print': ('(print)(?![\s\S])','T_k_print'),
        'string': ('(string)(?![\s\S])','T_k_string'),
        'boolean': ('(boolean)(?![\s\S])','T_k_boolean'),

        # Symbols
        '$': ('\$(?![\s\S])', 'T_eof'),
        '"': ('\"(?![\s\S])', 'T_quote'),
        '=': ('=(?![\s\S])', 'T_assign'),
        '{': ('{(?![\s\S])', 'T_l_brace'),
        '}': ('}(?![\s\S])', 'T_r_brace'),
        '(': ('\((?![\s\S])', 'T_l_paren'),
        ')': ('\)(?![\s\S])', 'T_r_paren'),
        '+': ('\+(?![\s\S])', 'T_intop_add'),
        '==': ('==(?![\s\S])', 'T_boolop_eq'),
        '!=': ('!=(?![\s\S])', 'T_boolop_ineq')
    }
    keyword_regex = r'^%s$' % '|'.join(valid_tokens[x][0] for x in valid_tokens)[0:140]
    id_regex = r'^[a-z]$'
    symbol_regex = r'^%s$' % '|'.join(valid_tokens[x][0] for x in valid_tokens)[141:]
    digit_regex = r'^[0-9]$'
    char_regex = r'^[a-z ]\Z'

    t_kinds = {
        'T_keyword': keyword_regex,
        'T_id': id_regex,
        'T_symbol': symbol_regex,
        'T_digit': digit_regex,
        'T_char': char_regex,
    }

    return valid_tokens, t_kinds

def tokenKinds():
    return set((
        # Keywords
        'T_k_if',
        'T_k_int',
        'T_k_true',
        'T_k_false',
        'T_k_while',
        'T_k_print',
        'T_k_string',
        'T_k_boolean',
        'T_eof',
        'T_quote',
        'T_assign',
        'T_l_brace',
        'T_r_brace',
        'T_l_paren',
        'T_r_paren',
        'T_intop_add',
        'T_boolop_eq',
        'T_boolop_ineq',
        'T_id',
        'T_digit',
        'T_char'
    ))

def tokenKindLiteral(token_kind):
    d = {
        'T_k_if':'if',
        'T_k_int':'int',
        'T_k_true':'true',
        'T_k_false': 'false',
        'T_k_while':'while',
        'T_k_print':'print',
        'T_k_string':'string',
        'T_k_boolean':'boolean',
        'T_eof':'$',
        'T_quote':'"',
        'T_assign':'=',
        'T_l_brace':'{',
        'T_r_brace':'}',
        'T_l_paren':'(',
        'T_r_paren':')',
        'T_intop_add':'+',
        'T_boolop_eq':'==',
        'T_boolop_ineq':'!=',
        'T_id':'ID',
        'T_digit':'Digit',
        'T_char': 'Char'
    }
    return d[token_kind]
