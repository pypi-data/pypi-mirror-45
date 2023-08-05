from treelib import Node, Tree
from gutec.scope import gScope
from gutec.tokens import Token
from gutec.utilities import *


def makeAST(cst_nodes, program_num):
    STDOUT(f'Semantic Analysis:')
    semantic_error = False
    semantic_warns = []
    symbol_table = []
    curr_scope = None
    curr_node = None
    curr_cst_node = 0
    ast = Tree()


    def parseProgram(program_num):
        nonlocal ast, curr_node

        matchNode(cst_nodes[curr_cst_node].tag, '<Program>')
        parseBlock()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_eof')
        endChildren()

    def parseBlock():
        nonlocal ast, curr_node, curr_cst_node
        matchNode(cst_nodes[curr_cst_node].tag, "<Block>")
        newScope()

        if ast.size() is 0:
            curr_node = ast.create_node('<Block>')
        else:
            curr_node = ast.create_node('<Block>', parent=curr_node.identifier)

        matchNode(cst_nodes[curr_cst_node].data.type_, "T_l_brace")
        parseStatementList()
        matchNode(cst_nodes[curr_cst_node].data.type_, "T_r_brace")

        if len(symbol_table) > 1:
            endScope()
        endChildren()

    def parseStatementList():
        nonlocal ast, curr_node, curr_cst_node

        matchNode(cst_nodes[curr_cst_node].tag, '<Statement List>')
        if match(cst_nodes[curr_cst_node+1].tag, '<If Statement>') or match(cst_nodes[curr_cst_node+1].tag, '<While Statement>') or match(cst_nodes[curr_cst_node+1].tag, '<Print Statement>') or match(cst_nodes[curr_cst_node+1].tag, '<Assignment Statement>') or match(cst_nodes[curr_cst_node+1].tag, '<Variable Decleration>') or match(cst_nodes[curr_cst_node+1].tag, '<Block>'):
            parseStatement()
            parseStatementList()
        else:

            pass

    def parseStatement():
        matchNode(cst_nodes[curr_cst_node].tag, '<Statement>')

        if match(cst_nodes[curr_cst_node].tag, '<Print Statement>'):
            parsePrint()

        elif match(cst_nodes[curr_cst_node].tag, '<Assignment Statement>'):
            parseAssignment()

        elif match(cst_nodes[curr_cst_node].tag, '<Variable Decleration>'):
            parseVarDecl()

        elif match(cst_nodes[curr_cst_node].tag, '<While Statement>'):
            parseWhile()

        elif match(cst_nodes[curr_cst_node].tag, '<If Statement>'):
            parseIf()

        elif match(cst_nodes[curr_cst_node].tag, '<Block>'):
            parseBlock()

        else:
            semanticError(f'Expected if, while, print, ID, int, boolean, string or block')

    def parsePrint():
        nonlocal ast, curr_node

        curr_node = ast.create_node('<Print Statement>', parent=curr_node.identifier)
        nextCSTNode()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_k_print')
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_l_paren')
        parseExpr()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_r_paren')
        endChildren()

    def parseAssignment():
        nonlocal ast, curr_node

        curr_node = ast.create_node('<Assignment Statement>', parent=curr_node.identifier)
        nextCSTNode()

        parseID()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_assign')
        parseExpr()

        id_info = ast.children(curr_node.identifier)
        var_ = id_info[0].data.value
        value_ = id_info[1]
        line_ = id_info[0].data.line_num

        var_exists = checkID(var_)

        if var_exists:
            
            while not value_.data:
                value_ = ast.children(value_.identifier)[0]

            id_scope = checkScopeLevel(var_)

            var_type = symbol_table[id_scope].checkType(var_)
            value_type = value_.data.type_

            if var_type != value_type:
                scopeError(f'type mismatch, var {var_} cannot equal "{value_.data}"', line_)
                
            checkInit(var_)
        else:
            scopeError(f'variable "{var_}" has not been declared', line_)

        endChildren()

    def parseWhile():
        nonlocal ast, curr_node

        curr_node = ast.create_node('<While Statement>', parent=curr_node.identifier)
        nextCSTNode()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_k_while')
        parseBooleanExpr()
        parseBlock()
        endChildren()

    def parseIf():
        nonlocal ast, curr_node

        curr_node = ast.create_node('<If Statement>', parent=curr_node.identifier)
        nextCSTNode()
        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_k_if')
        parseBooleanExpr()
        parseBlock()
        endChildren()

    def parseVarDecl():
        nonlocal ast, curr_node, symbol_table
        curr_node = ast.create_node('<Variable Decleration>', parent=curr_node.identifier)
        matchNode(cst_nodes[curr_cst_node].tag, '<Variable Decleration>')
        parseType()
        parseID()

        id_info = ast.children(curr_node.identifier)
        name_ = id_info[1].data.value
        type_ = id_info[0].data.type_
        line_ = id_info[1].data.line_num

        id_exists = checkID(name_)
        if not id_exists:
            _print(f'Added var {name_}:({type_})')
            curr_scope.new_id(name_,type_,line_)
        else:
            scopeError(f'variable "{name_}" already declared', line_)

        endChildren()

    def parseExpr():
        nonlocal ast, curr_node, cst_nodes, curr_cst_node, curr_scope

        matchNode(cst_nodes[curr_cst_node].tag, '<Expr>')

        if match(cst_nodes[curr_cst_node].tag, '<Int Expr>'):
            parseIntExpr()
        elif match(cst_nodes[curr_cst_node].tag, '<Boolean Expr>'):
            parseBooleanExpr()
        elif match(cst_nodes[curr_cst_node].tag, '<String Expr>'):
            nextCSTNode()
            parseStringExpr()
        elif match(cst_nodes[curr_cst_node].tag, '<ID>'):
            parseID()

            var_info = ast.children(curr_node.identifier)
            var_ = var_info[0].data.value


            if checkID(var_):
                id_scope = checkScopeLevel(var_)
                line_ = symbol_table[id_scope].getLineNum(var_)

                scope_used = 0

                if checkInit(var_):
                    scope_used = checkUsed(var_)
                else:
                    scopeWarning(f'variable {var_} has not been initialized',line_)

                symbol_table[scope_used].used(var_)
            else:
                pass

        elif cst_nodes[curr_cst_node].data and match(cst_nodes[curr_cst_node].data.type_, 'T_l_paren'):
            parseBooleanExpr()
        else:
            semanticError('Expected Int, Bool, String Expressions or an ID')

    def parseIntExpr():
        nonlocal ast, curr_node,curr_scope

        matchNode(cst_nodes[curr_cst_node].tag, '<Int Expr>')
        if matchNode(cst_nodes[curr_cst_node].tag, '<Digit>'):
            digit = parseDigit()

            if match(cst_nodes[curr_cst_node].tag, '<Int Op>'):
                nextCSTNode()
                intop = parseIntOp()
                ast.add_node(digit,  parent=curr_node.identifier)
                parseExpr()

                digit_ = ast.children(curr_node.identifier)[0]
                to_add = ast.children(curr_node.identifier)[1]

                while not to_add.data:
                    to_add = ast.children(to_add.identifier)[0]

        
                digit_type = digit_.data.type_
                
                if to_add.data.type_ == 'T_id':
                    id_scope = checkScopeLevel(to_add.data.value)
                    to_add_type = symbol_table[id_scope].checkType(to_add.data.value)
                else:
                    to_add_type = to_add.data.type_

                if digit_type != to_add_type:
                    error_ = ""
                    if to_add.data.type_ == 'T_id':
                        error_ = f'type mismatch, {digit.data} cannot be added to var {to_add.data.value}'
                    else:
                        error_ = f'type mismatch, {digit.data} cannot be added to "{to_add.data.value}"'
                    
                    scopeError(error_, digit_.data.line_num)

                endChildren()
            else:
                ast.add_node(digit,  parent=curr_node.identifier)

    def parseStringExpr():
        nonlocal ast, curr_node

        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_quote')
        curr_node = ast.create_node('<Char List>', parent=curr_node.identifier)
        matchNode(cst_nodes[curr_cst_node].tag, '<Char List>')
        parseCharList()
        endChildren()

        matchNode(cst_nodes[curr_cst_node].data.type_, 'T_quote')
        endChildren()

    def parseBooleanExpr():
        nonlocal ast, curr_node, curr_cst_node

        matchNode(cst_nodes[curr_cst_node].tag, '<Boolean Expr>')
        if cst_nodes[curr_cst_node].data and match(cst_nodes[curr_cst_node].data.type_, 'T_l_paren'):
            nextCSTNode()

            counter = 0
            while not match(cst_nodes[curr_cst_node].tag, '<Bool Op>'):
                counter += 1
                nextCSTNode()

            parseBoolOp()
            curr_cst_node -= counter

            parseExpr()
            parseExpr()


            left = ast.children(curr_node.identifier)[0]
            right = ast.children(curr_node.identifier)[1]

            while not left.data:
                left = ast.children(left.identifier)[0]
            while not right.data:
                right = ast.children(right.identifier)[0]

            _line = left.data.line_num

            if left.data.type_ == 'T_id':
                left_scope = checkScopeLevel(left.data.value)
                left = symbol_table[left_scope].checkType(left.data.value)
            else:
                left = left.data.type_

            if right.data.type_ == 'T_id':
                right_scope = checkScopeLevel(right.data.value)
                right = symbol_table[right_scope].checkType(right.data.value)
            else:
                right = right.data.type_

            if left != right:
                scopeError(f'type mismatch, {left} cannot equal {right}==',_line)

            endChildren()
            matchNode(cst_nodes[curr_cst_node].data.type_, 'T_r_paren')

        elif match(cst_nodes[curr_cst_node].tag, '<BooleanVal>'):
            nextCSTNode()
            bool_node = parseBoolVal()
            ast.add_node(bool_node,  parent=curr_node.identifier)

        else:
            semanticError('Expected "(", true, or false')

    def parseID():
        nonlocal ast, curr_node

        matchNode(cst_nodes[curr_cst_node].tag, '<ID>')
        if match(cst_nodes[curr_cst_node].data.type_, 'T_id'):
            ast.create_node(cst_nodes[curr_cst_node].tag, parent=curr_node.identifier, data=cst_nodes[curr_cst_node].data)
            nextCSTNode()
        else:
            semanticError(f'Expected an ID')

    def parseCharList():
        nonlocal ast, curr_node

        char_list = []
        while match(cst_nodes[curr_cst_node].tag, '<Char>'):
            nextCSTNode()
            match(cst_nodes[curr_cst_node].data.type_, 'T_char')
            char_list.append(cst_nodes[curr_cst_node])
            nextCSTNode()

        if char_list:
            char_list_token = Token('T_k_string', "".join([char.tag[2] for char in char_list]), cst_nodes[curr_cst_node-1].data.line_num)
            curr_node = ast.create_node(f'[ {char_list_token.value} ]', parent=curr_node.identifier, data=char_list_token)

        else:
            char_list_token = Token('T_k_string', ' ', cst_nodes[curr_cst_node-2].data.line_num)
            curr_node = ast.create_node(f'[  ]', parent=curr_node.identifier, data=char_list_token)

    def parseType():
        nonlocal ast, curr_node
        matchNode(cst_nodes[curr_cst_node].tag, '<Type>')

        if match(cst_nodes[curr_cst_node].data.type_, 'T_k_int') or match(cst_nodes[curr_cst_node].data.type_, 'T_k_string') or match(cst_nodes[curr_cst_node].data.type_, 'T_k_boolean'):
            ast.create_node(cst_nodes[curr_cst_node].tag, parent=curr_node.identifier, data=cst_nodes[curr_cst_node].data)
            nextCSTNode()
        else:
            pass

    def parseDigit():
        nonlocal ast, curr_node
        if match(cst_nodes[curr_cst_node].data.type_, 'T_digit'):
            cst_nodes[curr_cst_node].data.type_ = 'T_k_int'
            digit_node = Node(cst_nodes[curr_cst_node].tag, data=cst_nodes[curr_cst_node].data)
            nextCSTNode()
            return digit_node
        else:
            pass

    def parseBoolOp():
        nonlocal ast, curr_node, curr_cst_node, cst_nodes

        matchNode(cst_nodes[curr_cst_node].tag, '<Bool Op>')
        del cst_nodes[curr_cst_node-1]
        curr_cst_node -= 1

        if match(cst_nodes[curr_cst_node].data.type_, 'T_boolop_eq'):
            curr_node = ast.create_node('<IsEqual>', parent=curr_node.identifier)
            nextCSTNode()
            del cst_nodes[curr_cst_node-1]
            curr_cst_node -= 1
        elif match(cst_nodes[curr_cst_node].data.type_, 'T_boolop_ineq'):
            nextCSTNode()
            curr_node = ast.create_node('<NotEqual>', parent=curr_node.identifier)
            del cst_nodes[curr_cst_node-1]
            curr_cst_node -= 1
        else:
            pass

    def parseBoolVal():
        nonlocal ast, curr_node
        bool_node = None

        if match(cst_nodes[curr_cst_node].data.type_, 'T_k_true') or match(cst_nodes[curr_cst_node].data.type_, 'T_k_false'):
            cst_nodes[curr_cst_node].data.type_ = 'T_k_boolean'
            bool_node = Node(cst_nodes[curr_cst_node].tag,data=cst_nodes[curr_cst_node].data)
            nextCSTNode()
        else:
            pass

        if bool_node:
            return bool_node

    def parseIntOp():
        nonlocal ast, curr_node

        if matchNode(cst_nodes[curr_cst_node].data.type_, 'T_intop_add'):
            curr_node = ast.create_node('<Add>', parent=curr_node.identifier)
        else:
            pass

    def match(input_node, expected_node):
        nonlocal curr_cst_node

        if not input_node:
            return False

        if input_node == expected_node:
            return True
        else:
            return False

    def matchNode(input_node, expected_node):
        nonlocal curr_cst_node
        
        if not input_node:
            return False

        if input_node == expected_node:
            nextCSTNode()
            return True
        else:
            semanticError(f'Expected "{expected_node}"')
            return False

    def endChildren():
        nonlocal ast, curr_node

        if ast.get_node(curr_node.bpointer):
            curr_node = ast.parent(curr_node.identifier)

    def nextCSTNode():
        nonlocal curr_cst_node
        curr_cst_node += 1

    def newScope():
        nonlocal symbol_table,curr_scope
        symbol_table.append(gScope())
        curr_scope = symbol_table[-1]
        _print(f'Creating new scope: {symbol_table.index(curr_scope)}')

    def endScope():
        nonlocal symbol_table,curr_scope
        _print(f'Ending scope:{symbol_table.index(curr_scope)}')
        symbol_table.pop()
        curr_scope = symbol_table[-1]

    def checkID(id):
        nonlocal symbol_table

        id_exists = [_scope.getLineNum(id) for _scope in symbol_table[::-1] if _scope.checkExists(id)]

        if id_exists:
            return id_exists[0] 
        return False

    def checkInit(id):
        nonlocal symbol_table, curr_scope

        id_init = [scope.getLineNum(id) for scope in symbol_table[::-1] if scope.checkInit(id)]

        if id_init:
            return id_init[0]
        return False

    def checkUsed(id):
        nonlocal symbol_table, curr_scope

        id_used = [scope.getLineNum(id) for scope in symbol_table[::-1] if scope.checkUsed(id)]

        if id_used:
            return id_used[0]
        return False

    def checkScopeLevel(id):
        nonlocal symbol_table, curr_scope

        for scope in symbol_table[::-1]:
            if scope.checkExists(id):
                return symbol_table.index(scope)
        return None

    def checkFinalWarnings():
        nonlocal curr_scope

        for var, details in curr_scope.ids.items():
            if not curr_scope.checkInit(var):
                line_ = curr_scope.getLineNum(var)
                scopeWarning(f'variable {var} has not been initialized', line_)
            if not curr_scope.checkUsed(var):
                line_ = curr_scope.getLineNum(var)
                scopeWarning(f'variable {var} has not been used', line_)

        pass
    
    def _print(message):
        nonlocal semantic_error
        if not semantic_error:
            print(message)
    
    def semanticError(error_message):
        nonlocal cst_nodes, curr_cst_node, semantic_error
        if not semanticError:
            STDERR(f'Semantic Error: {error_message} | Found "{cst_nodes[curr_cst_node].tag}"')
            semantic_error = True
    
    def scopeError(error_message, line_num):
        nonlocal cst_nodes, curr_cst_node, semantic_error
        
        if not semantic_error:
            STDERR(f'Semantic Error: {error_message} at line {line_num}')
            semantic_error = True

    def scopeWarning(warn_message, line_num):
        nonlocal cst_nodes, curr_cst_node, semantic_warns
        semantic_warns.append(f'Semantic Warning: {warn_message} at line {line_num}')
        semantic_error = True
        
    parseProgram(program_num)

    checkFinalWarnings()

    return ast, symbol_table, semantic_error, semantic_warns




def analyze(cst_nodes, program_num):
    ast, symbol_table, semantic_errors, semantic_warnings = makeAST(cst_nodes, program_num)

    if semantic_errors:
        return

    STDWARN(f'\nProgram {program_num} AST:')
    printTree(ast)
    print()
    if semantic_warnings:
        [STDWARN(warning) for warning in semantic_warnings]
        
    STDWARN(f'\nProgram {program_num} symbol table:')
    printSymbolTable(*symbol_table)
