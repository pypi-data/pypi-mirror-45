# -*- coding: utf-8 -*-

###############################################################################
# modify sys.path
import os  # noqa
import sys  # noqa

sys.modules.pop('token', None)  # noqa
sys.modules.pop('tokenize', None)  # noqa
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))  # noqa
###############################################################################

import collections.abc
import io
import locale
import re
import tokenize

import parso

###############################################################################
# reset sys.path
sys.path.pop(0)

sys.modules.pop('tokenize', None)
sys.modules.pop('token', None)
del sys
###############################################################################

__all__ = ['f2format', 'convert', 'ConvertError']

# macros
PARSO_VERSION = ('3.6', '3.7', '3.8')
LOCALE_ENCODING = locale.getpreferredencoding()

class ConvertError(SyntaxError):
    pass


class strarray(collections.abc.ByteString):
    """Construct a mutable strarray object."""
    def __init__(self, string):
        self.__data__ = [c for c in string]

    def __str__(self):
        return ''.join(self.__data__)

    def __repr__(self):
        return 'strarray(%s)' % ''.join(self.__data__)

    def __getitem__(self, index):
        return ''.join(self.__data__[index])

    def __len__(self):
        return len(self.__data__)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self.__data__[key] = [c for c in value]
        else:
            self.__data__[key] = value
        # print('setitem:', key, value, '###', repr(self)) ###


def convert(string, lineno=None):
    """The main conversion process.

    Args:
     - string -- str, context to be converted
     - lineno -- dict<int: int>, line number to actual offset mapping

    Returns:
     - str -- converted string

    """
    if lineno is None:
        lineno = {1: 0}
        for lnum, line in enumerate(string.splitlines(True), start=1):
            lineno[lnum+1] = lineno[lnum] + len(line)

    def parse(string, error_recovery=False):
        try:
            return parso.parse(string, error_recovery=error_recovery,
                               version=os.getenv('F2FORMAT_VERSION', PARSO_VERSION[-1]))
        except parso.ParserSyntaxError as error:
            message = '%s: <%s: %r> from %r' % (error.message, error.error_leaf.token_type,
                                                error.error_leaf.value, string)
            raise ConvertError(message).with_traceback(error.__traceback__)

    source = strarray(string)       # strarray source (mutable)
    f_string = [list()]             # [[token, ...], [...], ...] -> concatenable strings

    str_flag = False    # if previous item is token.STRING
    for token in tokenize.generate_tokens(io.StringIO(string).readline):
        cat_flag = False                    # if item is concatenable with previous item, i.e. adjacent string
        if token.type == tokenize.STRING:
            if str_flag:
                cat_flag = True
            if cat_flag:
                f_string[-1].append(token)
            else:
                f_string.append([token])
            str_flag = True
        elif token.type == tokenize.NL:     # skip token.NL
            continue
        else:                               # otherwise, not concatenable
            str_flag = False
        # print(token) ###

    # print() ###
    # import pprint ###
    # pprint.pprint(f_string) ###
    # print() ###

    for tokens in reversed(f_string):   # for each string concatenation
        # check if has f-string literal in this concatenation
        future = any(map(lambda token: re.match(r'^(f|rf|fr)', token.string, re.IGNORECASE), tokens))
        if not future:
            continue

        entryl = list()
        for token in tokens:            # for each token in concatenation
            token_string = token.string
            token_lineno = {1: 0}
            for lnum, line in enumerate(token_string.splitlines(True), start=1):
                token_lineno[lnum+1] = token_lineno[lnum] + len(line)

            module = parse(token_string)            # parse AST, get parso.python.tree.Module, _.children -> list
                                                    # _[0] -> parso.python.tree.PythonNode
                                                    # _[1] -> parso.python.tree.EndMarker
            tmpval = module.children[0]             # parsed string token
            tmpent = list()                         # temporary entry list

            if tmpval.type == 'fstring':            # parso.python.tree.PythonNode.type -> str, string / fstring
                # parso.python.tree.PythonNode.children[0] -> parso.python.tree.FStringStart, regex: /^((f|rf|fr)('''|'|"""|"))/
                # parso.python.tree.PythonNode.children[-1] -> parso.python.tree.FStringEnd, regex: /('''|'|"""|")$/
                for obj in tmpval.children[1:-1]:               # traverse parso.python.tree.PythonNode.children -> list # noqa
                    if obj.type == 'fstring_expr':                      # expression part (in braces), parso.python.tree.PythonNode # noqa
                        obj_children = obj.children                             # parso.python.tree.PythonNode.children -> list
                                                                                # _[0] -> parso.python.tree.Operator, '{' # noqa
                                                                                # _[1] -> %undetermined%, expression literal (f_expression) # noqa
                                                                                # _[2] -> %optional%, parso.python.tree.PythonNode, format specification (format_spec) # noqa
                                                                                # _[3] -> parso.python.tree.Operator, '}' # noqa
                        start_expr_pos = obj_children[1].start_pos              # _[1].start_pos -> tuple, (line, offset) # noqa
                        end_expr_pos = obj_children[1].end_pos                  # _[1].end_pos -> tuple, (line, offset) # noqa

                        start_expr = token_lineno[start_expr_pos[0]] + start_expr_pos[1]
                        end_expr = token_lineno[end_expr_pos[0]] + end_expr_pos[1]
                        tmpent.append(slice(start_expr, end_expr))              # entry of expression literal (f_expression)

                        if obj_children[2].type == 'fstring_format_spec':
                            for node in obj_children[2].children:               # traverse format specifications (format_spec)
                                if node.type == 'fstring_expr':                         # expression part (in braces), parso.python.tree.PythonNode # noqa
                                    node_chld = node.children                                   # parso.python.tree.PythonNode.children -> list # noqa
                                                                                                # _[0] -> parso.python.tree.Operator, '{' # noqa
                                                                                                # _[1] -> %undetermined%, expression literal (f_expression) # noqa
                                                                                                # _[2] -> parso.python.tree.Operator, '}' # noqa
                                    start_spec_pos = node_chld[1].start_pos                     # _[1].start_pos -> tuple, (line, offset) # noqa
                                    end_spec_pos = node_chld[1].end_pos                         # _[1].end_pos -> tuple, (line, offset) # noqa

                                    start_spec = token_lineno[start_spec_pos[0]] + start_spec_pos[1]
                                    end_spec = token_lineno[end_spec_pos[0]] + end_spec_pos[1]
                                    tmpent.append(slice(start_spec, end_spec))                  # entry of format specification (format_spec) # noqa
                    # print('length:', length, '###', token_string[:length], '###', token_string[length:]) ###
            entryl.append((token, tmpent))          # each token with a concatenation entry list

        # print('entry: ', end='') ###
        # pprint.pprint(entryl) ###
        # print() ###

        expr = list()
        for token, entries in entryl:   # extract expressions
            # print(token.string, entries) ###
            for entry in entries:       # walk entries
                temp_expr = token.string[entry]                                 # original expression
                val = parse(temp_expr, error_recovery=True).children[0]         # parse AST
                if val.type == 'testlist_star_expr' and \
                        re.fullmatch(r'\(.*\)', temp_expr, re.DOTALL) is None:  # if expression is implicit tuple
                    real_expr = '(%s)' % temp_expr                              # add parentheses
                else:
                    real_expr = temp_expr                                       # or keep original
                expr.append(real_expr)                                          # record expression

        # print() ###
        # print('expr: ', end='') ###
        # pprint.pprint(expr) ###

        # convert end of f-string to str.format literal
        end = lineno[tokens[-1].end[0]] + tokens[-1].end[1]
        source[end:end+1] = '.format(%s)%s' % (', '.join(expr), source[end])

        # for each token, convert expression literals and brace '{}' escape sequences
        for token, entries in reversed(entryl):     # using reversed to keep offset in leading context
            token_start = lineno[token.start[0]] + token.start[1]   # actual offset at start of token
            token_end = lineno[token.end[0]] + token.end[1]         # actual offset at end of token
            if entries:     # for f-string expressions, replace with empty string ('')
                for entry in reversed(entries):
                    start = token_start + entry.start
                    end = token_start + entry.stop
                    source[start:end] = ''
            else:           # for escape sequences, double braces
                source[token_start:token_end] = re.sub(r'([{}])', r'\1\1', source[token_start:token_end])

            # strip leading f-string literals ('[fF]')
            string = source[token_start:token_start+3]
            if re.match(r'^(rf|fr|f)', string, re.IGNORECASE) is not None:
                source[token_start:token_start+3] = re.sub(r'[fF]', r'', string, count=1)

    # return modified context
    return str(source)


def f2format(filename):
    """Wrapper works for conversion.

    Args:
     - filename -- str, file to be converted

    """
    print('Now converting %r...' % filename)

    # fetch encoding
    encoding = os.getenv('F2FORMAT_ENCODING', LOCALE_ENCODING)

    lineno = {1: 0}     # line number -> file offset
    content = list()    # file content
    with open(filename, 'r', encoding=encoding) as file:
        for lnum, line in enumerate(file, start=1):
            content.append(line)
            lineno[lnum+1] = lineno[lnum] + len(line)

    # now, do the dirty works
    string = ''.join(content)
    text = convert(string, lineno)

    # dump back to the file
    with open(filename, 'w', encoding=encoding) as file:
        file.write(text)

    # print() ###
    # print('original:', string, sep='\n') ###
    # print('###\n') ###
    # print('converted:', text, sep='\n') ###
