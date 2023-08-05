import re,click
from beautifultable import BeautifulTable
from operator import itemgetter
from gutec.tokens import *
from gutec.glexer import *

# Given an input string of programs, split it by the eof symbol ($) and return them as a list


def dividePrograms(pgms):
    input_ = pgms.rstrip()
    eop_count = pgms.count('$')
    programs = pgms.split('$')

    if not programs[0]:
        if len(programs) > 1:
            return ['$' for i in range(eop_count)]

        return []
    else:
        # Filter empty elements in the list
        program_split = tuple(filter(None, programs))

        # Add back the eof character after the splt
        programs = [f'{program_split[i]}$' for i in range(eop_count)]

        # if our program count doesn't match the count of eop's in the input, or the eop count is 0 then we are missing a trailing eop
        program_count = len(programs)
        if eop_count is 0 or eop_count != program_count:
            programs[-1:] = program_split[-1:]
            programs[-1] = programs[-1] + '$'
            STDWARN("Warning: Missing EOP '$'")

        return programs


def removeComments(programs):
    return re.sub(r'(\/\*)(.|\n)+?(\*\/)', '', programs)

# Given a string of chars and a set of valid tokens find and return the kinds of tokens the string matches


def matchToken(char, matches, token_kinds, string_mode):
    for token in token_kinds:
        if string_mode and char != '"' and token != 'T_char':
            continue

        match = re.match(token_kinds[token], char)
        if match:
            matches.append((token, len(char), char))

# Given a list of matches and valid tokens get the longest match or the highest priority match and create a token


def spawnToken(matches, token_kinds, valid_tokens, curr_line):
    # Find Longast match
    longest = max(matches, key=itemgetter(1))
    if type(longest) is tuple:
        longest = [(longest)]

    # Highest priority is always the firstmost element because matches are created in priorty order
    highest_priority = longest[0]
    t_kind = highest_priority[0]
    t_val = highest_priority[2]

    if t_kind == 'T_keyword' or t_kind == 'T_symbol':
        # Instantiate token
        t_kind = valid_tokens[highest_priority[2]][1]

    return Token(t_kind, t_val, curr_line)

# Functions to print to the command line with pretty colors


def STDOUT(message):
    click.echo(click.style(message, fg='green'))


def STDERR(message):
    click.echo(click.style(message, fg='red'))


def STDWARN(message):
    click.echo(click.style(message, fg='yellow'))


def printTree(tree):
    def traverse(t, node):
        print(f'{"-" * t.level(node.identifier)}{node.tag}')
        for node in t.children(node.identifier):
            traverse(t, node)

    traverse(tree, tree.get_node(tree.root))


def getInorderList(tree, node, node_list):
    # def traverse(t, node):
    node_list.append(node)
    for node in tree.children(node.identifier):
        getInorderList(tree, node, node_list)
    return node_list


def traverseInorder(tree, node):
    # def traverse(t, node):
    print(node.tag)
    for node in tree.children(node.identifier):
        traverseInorder(tree, node)

def printSymbolTable(symbol_table):
    table = BeautifulTable()
    table.column_headers = ["Variable", "Type", "Initialized?","Used?","Line Number"]

    # print(symbol_table.ids)
    vars = symbol_table.ids.keys()

    for var in vars:
        details = symbol_table.ids[var]
        table.append_row([var, *details])
   
    print(table)
