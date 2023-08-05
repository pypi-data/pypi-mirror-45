from treelib import Node, Tree
from gutec.tokens import tokenKinds, tokenKindLiteral
from gutec.utilities import STDERR, STDOUT, STDWARN


def guteParse(token_stream, program_num):
    STDOUT(f'PARSER:')
    token_kinds = tokenKinds()
    cst = Tree()
    parse_error = False
    curr_node = cst.create_node('<Program>')
    curr_token = 0

    def parseProgram(program_num):
        nonlocal cst, curr_node
        parseBlock()
        matchConsume('T_eof')
        endChildren()

    def parseBlock():
        nonlocal cst, curr_node
        _print('Block')
        curr_node = cst.create_node('<Block>', parent=curr_node.identifier)

        matchConsume('T_l_brace')
        parseStatementList()
        matchConsume('T_r_brace')
        endChildren()

    def parseStatementList():
        nonlocal cst, curr_node
        _print('Statement List')

        curr_node = cst.create_node(
            '<Statement List>', parent=curr_node.identifier)

        if match('T_k_if') or match('T_k_while') or match('T_k_print') or match('T_id') or match('T_k_int') or match('T_k_boolean') or match('T_k_string') or match('T_l_brace'):
            parseStatement()
            parseStatementList()
        else:
            pass
        endChildren()


    def parseStatement():
        nonlocal cst, curr_node, token_stream
        _print('Statement')
        curr_node = cst.create_node('<Statement>', parent=curr_node.identifier)

        if match('T_k_print'):
            parsePrint()

        elif match('T_id'):
            parseAssignment()

        elif match('T_k_int') or match('T_k_boolean') or match('T_k_string'):
            parseVarDecl()

        elif match('T_k_while'):
            parseWhile()

        elif match('T_k_if'):
            parseIf()

        elif match('T_l_brace'):
            parseBlock()

        else:
            parseError(
                f'Expected if, while, print, ID, int, boolean, string or block')

        endChildren()

    def parsePrint():
        nonlocal cst, curr_node
        _print('Print Statement')

        curr_node = cst.create_node(
            '<Print Statement>', parent=curr_node.identifier)
        matchConsume('T_k_print')
        matchConsume('T_l_paren')
        parseExpr()
        matchConsume('T_r_paren')
        endChildren()

    def parseAssignment():
        nonlocal cst, curr_node
        _print('Assignment Statement')

        curr_node = cst.create_node(
            '<Assignment Statement>', parent=curr_node.identifier)
        parseID()
        matchConsume('T_assign')
        parseExpr()
        endChildren()

    def parseVarDecl():
        nonlocal cst, curr_node
        print('Variable Decleration')

        curr_node = cst.create_node(
            '<Variable Decleration>', parent=curr_node.identifier)
        parseType()
        parseID()
        endChildren()

    def parseWhile():
        nonlocal cst, curr_node
        _print('While Statement')

        curr_node = cst.create_node(
            '<While Statement>', parent=curr_node.identifier)
        matchConsume('T_k_while')
        parseBooleanExpr()
        parseBlock()
        endChildren()

    def parseIf():
        nonlocal cst, curr_node
        print('If Statement')

        curr_node = cst.create_node(
            '<If Statement>', parent=curr_node.identifier)
        matchConsume('T_k_if')

        parseBooleanExpr()
        parseBlock()
        endChildren()

    def parseExpr():
        nonlocal cst, curr_node
        _print('Expression')

        curr_node = cst.create_node('<Expr>', parent=curr_node.identifier)
        if match('T_digit'):
            parseIntExpr()
        elif match('T_l_paren'):
            parseBooleanExpr()
        elif match('T_k_true') or match('T_k_false'):
            parseBooleanExpr()
        elif match('T_quote'):
            parseStringExpr()
        elif match('T_id'):
            parseID()
        else:
            parseError('Expected Int, Bool, String Expressions or an ID')

        endChildren()

    def parseIntExpr():
        nonlocal cst, curr_node
        _print('Int Expression')

        curr_node = cst.create_node('<Int Expr>', parent=curr_node.identifier)
        if match('T_digit'):
            parseDigit()

        if match('T_intop_add'):
            parseIntOp()
            parseExpr()

        endChildren()

    def parseStringExpr():
        nonlocal cst, curr_node
        _print('String Expression')

        curr_node = cst.create_node('<String Expr>', parent=curr_node.identifier)
        matchConsume('T_quote')

        curr_node = cst.create_node('<Char List>', parent=curr_node.identifier)
        _print('Char List')
        parseCharList()
        endChildren()

        matchConsume('T_quote')
        endChildren()

    def parseBooleanExpr():
        nonlocal cst, curr_node
        _print('Boolean Expression')

        curr_node = cst.create_node('<Boolean Expr>', parent=curr_node.identifier)
        if match('T_l_paren'):
            matchConsume('T_l_paren')
            parseExpr()
            parseBoolOp()
            parseExpr()
            matchConsume('T_r_paren')

        elif match('T_k_true') or match('T_k_false'):
            parseBoolVal()

        else:
            parseError('Expected "(", true, or false')

        endChildren()

    def parseID():
        nonlocal cst, curr_node
        _print('ID')

        curr_node = cst.create_node('<ID>', parent=curr_node.identifier)
        if match('T_id'):
            matchConsume('T_id')
        else:
            parseError(f'Expected {tokenKindLiteral("T_id")}')

        endChildren()

    def parseCharList():
        nonlocal cst, curr_node

        if match('T_char'):
            parseChar()
            parseCharList()
        else:
            pass

    def parseType():
        nonlocal cst, curr_node
        _print('Type')
        curr_node = cst.create_node('<Type>', parent=curr_node.identifier)

        if match('T_k_int'):
            matchConsume('T_k_int')
        elif match('T_k_string'):
            matchConsume('T_k_string')
        elif matchConsume('T_k_boolean'):
            matchConsume('T_k_boolean')
        else:
            pass
        endChildren()

    def parseChar():
        nonlocal cst, curr_node
        _print('Character')

        curr_node = cst.create_node('<Char>', parent=curr_node.identifier)

        if matchConsume('T_char'):
            pass
        else:
            pass

        endChildren()

    def parseDigit():
        nonlocal curr_node
        curr_node = cst.create_node('<Digit>', parent=curr_node.identifier)
        _print('Digit')
        if matchConsume('T_digit'):
            return
        else:
            pass

        endChildren()

    def parseBoolOp():
        nonlocal cst, curr_node
        _print('Boolean Operation')

        curr_node = cst.create_node('<Bool Op>', parent=curr_node.identifier)

        if match('T_boolop_eq'):
            matchConsume('T_boolop_eq')
        elif match('T_boolop_ineq'):
            matchConsume('T_boolop_ineq')
        else:
            parseError(f'Expected == or !=')

        endChildren()

    def parseBoolVal():
        nonlocal cst, curr_node
        _print('Boolean Value')
        curr_node = cst.create_node(
            '<BooleanVal>', parent=curr_node.identifier)
        if match('T_k_true'):
            matchConsume('T_k_true')
        if match('T_k_false'):
            matchConsume('T_k_false')
        else:
            pass
        endChildren()

    def parseIntOp():
        nonlocal cst, curr_node
        _print('Integer Operation')
        curr_node = cst.create_node('<Int Op>', parent=curr_node.identifier)
        if match('T_intop_add'):
            matchConsume('T_intop_add')
        else:
            pass
        endChildren()

    def match(to_match):
        nonlocal cst, curr_token, token_kinds, token_stream, curr_node

        if token_stream[curr_token].type_ == to_match and to_match in token_kinds:
            return True

        return False

    def matchConsume(to_match):
        nonlocal cst, curr_token, token_kinds, token_stream, curr_node

        if token_stream[curr_token].type_ == to_match and to_match in token_kinds:
            cst.create_node(f'[ {token_stream[curr_token]} ]',parent=curr_node.identifier, data=token_stream[curr_token])
            curr_token += 1
        else:
            parseError(f'Expected "{tokenKindLiteral(to_match)}"')

    def endChildren():
        nonlocal curr_node

        if cst.get_node(curr_node.bpointer):
            curr_node = cst.parent(curr_node.identifier)

    def parseError(error_message):
        nonlocal curr_token, token_stream, parse_error
        STDERR(
            f'Parse Error: {error_message} | Found "{token_stream[curr_token]}" on line {token_stream[curr_token].line_num}')
        parse_error = True

    def _print(message):
        nonlocal parse_error
        if not parse_error:
            print(message)

    parseProgram(program_num)
    return cst, parse_error
