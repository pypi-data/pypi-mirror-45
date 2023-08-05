import re
def grammarDict():
    valid_tokens = {
        # Keywords
        'T_K_if'      : '(if)(?![\s\S])',
        'T_K_int'     : '(int)(?![\s\S])',
        'T_K_true'    : '(true)(?![\s\S])',
        'T_K_false'   : '(false)(?![\s\S])',
        'T_K_while'   : '(while)(?![\s\S])',
        'T_K_print'   : '(print)(?![\s\S])',
        'T_K_string'  : '(string)(?![\s\S])',
        'T_K_boolean' : '(boolean)(?![\s\S])',

        # Symbols
        'T_EOF'         : '\$(?![\s\S])',
        'T_quote'       : '\"(?![\s\S])',
        'T_var_decl'      : '=(?![\s\S])',
        'T_LBrace'      : '{(?![\s\S])',
        'T_RBrace'      : '}(?![\s\S])',
        'T_LParen'      : '\((?![\s\S])',
        'T_RParen'      : '\)(?![\s\S])',
        'T_intop_add'   : '\+(?![\s\S])',
        'T_boolop_eq'   : '==(?![\s\S])',
        'T_boolop_ineq' : '!=(?![\s\S])',
    }
    keyword_regex = r'^%s$' % '|'.join(valid_tokens[x] for x in valid_tokens)[0:140]
    id_regex = r'^[a-z]$'
    symbol_regex = r'^%s$' % '|'.join(valid_tokens[x] for x in valid_tokens)[141:]
    digit_regex = r'^[0-9]$'
    char_regex = r'^[a-z ]$'

    t_kinds = {
        keyword_regex:('T_keyword',1),
        id_regex:     ('T_ID',     2),
        symbol_regex: ('T_symbol', 3),
        digit_regex:  ('T_digit',  4),
        char_regex:   ('T_char',   5),
    }

    return valid_tokens, t_kinds

    
