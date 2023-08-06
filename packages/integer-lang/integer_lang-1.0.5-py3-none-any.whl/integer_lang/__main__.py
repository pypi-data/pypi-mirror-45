Parser = Lark_StandAlone
import math
import sys
import re


#error classes
class Error(Exception):
	pass

class RecursionError(Error):
	#for when a user tries to build recursive functions. NOT ALLOWED! why? dunno. Though it does keep the call stack shorter by forcing you to use loops instead. So maybe that's why.
	pass

class ArgumentError(Error):
	#for when command line arguments are invalid - such as when a filename is not supplied, or it's malformed
	pass


#base converter

def toInt(numstr, base, alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
	#TODO - make interoperable with _num_to_base, using the alphabet argument
	width = 1
	while ((36 ** width) < base):
		width += 1
	
	radits = []
	res = 0
	
	while (len(numstr) > 0):
		cur = int(numstr[-width:], 36)
		if (cur >= base):
			raise ValueError("Radit '" + numstr[-width:] + "' out of base range.")
		radits.append(cur)
		numstr = numstr[:-width]
	
	for i in range(len(radits)):
		res += radits[i] * (base ** i)
	
	return res


#convert parse trees to AST
class Node:	#these will be what is fed into the interpreter methods :)
	def __init__ (self, type):
		self.type = type
		self.children = []
		
	def append(self, child):
		self.children.append(child)
		
	def __repr__(self):
		ret = "Node<" + self.type.upper() + ">("
		childs = []
		for i in self.children:
			childs.append(repr(i))
		return ret + ', '.join(childs) + ")"
		
	def __str__(self):
		return self.__repr__()

def toast(node):	#to AST = toast ;P
	if not hasattr(node, 'data'):
		return node
	else:
		if (len(node.children) == 1):
			return toast(node.children[0])
		else:
			ret = Node(node.data)
			for i in node.children:
				ret.append(toast(i))
			return ret

#a simple wrapper to call methods by name
def call(obj, method, arg):
	if (arg):
		return getattr(obj, method)(arg)
	else:
		return getattr(obj, method)()

#a file reader, because then I just call it and get what I want
def readFile(filepath):
	res = ''
	f = open(filepath, 'r')
	if (f.mode == 'r'):
		res = f.read()
	f.close()
	return res

#main interpreter class that does the easy work
class Interpreter:
	
	def __init__ (self, parser):
		self.parser = parser
		
		self.functions = {}	#store functions by name as AST.
		self.var = [0] #store var by function level, global being 0.
		
		self.function_stack = []
		self.function_level = 0
		self.loop_level = 0
	
	#INTERPRETER-FUNCTIONS---------------
	def reset(self):
		self.__init__(self.parser)
	
	def run(self, code_string):
		ast = self.parse_input(code_string)
		res = self.execute(ast)
		
		self.reset()
		return res
		
	def execute(self, node): #runs an AST node and its children
		res = call(self, node.type, node)
		self.setVar(res) #only sets if result is not None
		return self.getVar() #the return value of the program
	
	#HELPERS-----------------------------
	def getNum(self, node):
		return call(self, node.type, node)
	
	def getVar(self):
		if (len(self.var)-1 < self.function_level):
			return 0
		else:
			return self.var[self.function_level]
	
	def setVar(self, value):
		if (value != None):
			if (len(self.var)-1 < self.function_level):
				self.var.append(value)
			else:
				self.var[self.function_level] = value
	
	def inc_FunctionLevel(self):
		self.function_level += 1
		self.setVar(0)
	
	def dec_FunctionLevel(self):
		self.function_level -= 1
	
	def parse_input(self, input):
		return toast(self.parser.parse(input))
	
	def int_to_str(self, num):
		strlen = num % 256
		num //= 256
		res = ''
		for i in range(strlen):
			res = chr(num % 128) + res
			num = num // 256
		return res
	
	def str_to_int(self, strn):
		strlen = len(strn)
		res = 0
		while (len(strn) > 0):
			res = (res + ord(strn[0])) * 256
			strn = strn[1:]
		return res + strlen
	
	#START-------------------------------
	def start (self, node): #the entry point for most programs
		for n in node.children:
			self.execute(n)
		return self.getVar()
	
	#MATH--------------------------------
	def sum (self, node): #(product ADD)* product
		cur = 1
		res = self.getNum(node.children[0])
		while (len(node.children)-1 > cur):
			b = self.getNum(node.children[cur + 1])
			if (node.children[cur].type == 'ADD'):
				res += b
			cur += 2
		return res	
	
	def product (self, node): #(compare (MULT|DIV))* compare
		cur = 1
		res = self.getNum(node.children[0])
		while (len(node.children)-1 > cur):
			b = self.getNum(node.children[cur + 1])
			type = node.children[cur].type
			if (type == 'MULT'):
				res *= b
			if (type == 'DIV'):
				res //= b
			cur += 2
		return res
	
	def compare (self, node): #(bitwise GREATER)* bitwise
		cur = 1
		a = self.getNum(node.children[0])
		res = 0
		while (len(node.children) -1 > cur):
			b = self.getNum(node.children[cur + 1])
			type = node.children[cur].type
			if (type == 'GREATER'):
				if (a > b):
					res = 1
				else:
					res = 0
			a = b #set up for the next loop
			cur += 2
		return res
	
	def bitwise (self, node): #(<value> (B_AND|B_OR|B_XOR))* <value>
		cur = 1
		res = self.getNum(node.children[0])
		while (len(node.children) -1 > cur):
			b = self.getNum(node.children[cur + 1])
			type = node.children[cur].type
			if (type == "B_AND"):
				res = res & b
			
			if (type == "B_OR"):
				res = res | b
			
			if (type == "B_XOR"):
				res = res ^ b
			
			cur += 1
		return res
	
	#BLOCKS------------------------------
	def run_block (self, node, is_if):
		res = False
		if (node.type == "END"):
			return res
		for i in node.children:
			if (i.type == 'BREAK') and is_if:
				res = True
				continue
			if (i.type == 'END'):
				break
			self.setVar(call(self, i.type, i))
		return res
	
	#FUNCTIONS---------------------------
	def function_definition (self, node):
		fblock = node.children[1]
		fname = str(node.children[0]).upper()
		if (fblock.type != 'END') and ('BREAK' in fblock.children):
			self.BREAK(node)
		else:
			self.functions[fname] = fblock
	
	def function_call (self, node):
		res = 0
		fname = str(node.children[0]).upper()
		if (fname in self.function_stack):
			raise RecursionError("Recursion is not allowed.")
		elif not (fname in self.functions):
			raise NameError("Function " + fname + " does not exist")
		else:
			self.function_stack.append(fname)
			arg = self.getNum(node.children[1])
			
			self.function_level += 1
			self.setVar(arg)
			
			fblock = self.functions[fname]
			self.run_block(fblock, False)
			
			res = self.var.pop()
			self.function_level -= 1
			self.function_stack.pop()
			
		return res
			
	
	#LOOPS-------------------------------
	def loop_call (self, node):
		self.loop_level += 1
		self.function_level += 1
		runlevel = self.loop_level
		ins = 0
		res = None
		while(self.loop_level >= runlevel):
			i = node.children[1].children[ins]
			if (i.type == 'BREAK'):
				self.loop_level -= 1
				break
			elif (i.type == 'END'):
				ins = 0
			else:
				self.setVar(call(self, i.type, i))
				res = self.getVar()
				ins += 1
		self.function_level -= 1
		self.setVar(res)
	
	#FLOW-CONTROL------------------------
	def if_call (self, node):
		cond = self.getNum(node.children[1]) % 2
		if (cond == 1):
			block = node.children[2]
			res = self.run_block(block, True)
			if res:
				self.run_break()
	
	#NUMBERS-----------------------------
	def number (self, node):
		numstr = str(node.children[0]).replace('.','').upper()
		base = str(node.children[1])[1:]
		
		return toInt(numstr, int(base))
	
	def NUMBER_STRING (self, node):
		return int(node.value.replace('.',''))
	
	def VAR (self, node):
		return self.getVar()
	
	#I/O---------------------------------
	def READ (self, node):
		strn = input('?: ') + '\n'
		return self.str_to_int(strn)
	
	def write (self, node):
		num = self.getNum(node.children[1])
		print(self.int_to_str(num), end='')
	
	def include (self, node):
		if (len(node.children) == 2):
			s = str(node.children[1])
			s = re.split('[\/\\]', s)
			while s[-1] == '':
				s = s[:-1]
			as_str = s[-1].split('.')[0]
		else:
			as_str = str(node.children[2])
		
		strn = readFile(str(node.children[2]))
		i = Interpreter(self.parser)
		ast = i.parse_input(strn)
		i.execute(ast)
		
		for fun in i.functions:
			self.functions[as_str + '.' + fun] = i.functions[fun]
			
		return i.getVar()
	
	def eval_call (self, node):
		strn = self.int_to_str(node.children[1])
		ast = self.parse_input(strn)
		return self.execute(ast) #safe? no. Eval never is ;D
	
	#OTHER-------------------------------
	def BREAK (self, node):
		raise SyntaxError('BREAK statement cannot be used outside of LOOP blocks')
	
	def run_break (self):
		#this runs when BREAK is used properly
		if (self.loop_level == 0):
			raise SyntaxError('BREAK statement cannot be used outside of LOOP blocks')
		else:
			self.loop_level -= 1
	

###-----MAIN-FUNCTION-----###
def main():
	if (len(sys.argv) < 2):
		raise ArgumentError('Filename required (sorry, no REPL)')
	
	fname = sys.argv[1]
	pstr = readFile(fname)
	
	p = Parser()
	i = Interpreter(p)
	
	ret = i.run(pstr)
	print("=> " + str(ret))


if __name__ == "__main__":
	main()









#####-----------Lark standalone parser-----------#####

# These definitions were automatically generated by Lark v0.7.0
#
#
#   Lark Stand-alone Generator Tool
# ----------------------------------
# Generates a stand-alone LALR(1) parser with a standard lexer
#
# Git:    https://github.com/erezsh/lark
# Author: Erez Shinan (erezshin@gmail.com)
#
#
#    >>> LICENSE
#
#    This tool and its generated code use a separate license from Lark.
#
#    It is licensed under GPLv2 or above.
#
#    If you wish to purchase a commercial license for this tool and its
#    generated code, contact me via email.
#
#    If GPL is incompatible with your free or open-source project,
#    contact me and we'll work it out (for free).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    See <http://www.gnu.org/licenses/>.
#
#

class LarkError(Exception):
    pass

class GrammarError(LarkError):
    pass

class ParseError(LarkError):
    pass

class LexError(LarkError):
    pass

class UnexpectedInput(LarkError):
    pos_in_stream = None

    def get_context(self, text, span=40):
        pos = self.pos_in_stream
        start = max(pos - span, 0)
        end = pos + span
        before = text[start:pos].rsplit('\n', 1)[-1]
        after = text[pos:end].split('\n', 1)[0]
        return before + after + '\n' + ' ' * len(before) + '^\n'

    def match_examples(self, parse_fn, examples):
        """ Given a parser instance and a dictionary mapping some label with
            some malformed syntax examples, it'll return the label for the
            example that bests matches the current error.
        """
        assert self.state is not None, "Not supported for this exception"

        candidate = None
        for label, example in examples.items():
            assert not isinstance(example, STRING_TYPE)

            for malformed in example:
                try:
                    parse_fn(malformed)
                except UnexpectedInput as ut:
                    if ut.state == self.state:
                        try:
                            if ut.token == self.token:  # Try exact match first
                                return label
                        except AttributeError:
                            pass
                        if not candidate:
                            candidate = label

        return candidate


class UnexpectedCharacters(LexError, UnexpectedInput):
    def __init__(self, seq, lex_pos, line, column, allowed=None, considered_tokens=None, state=None):
        message = "No terminal defined for '%s' at line %d col %d" % (seq[lex_pos], line, column)

        self.line = line
        self.column = column
        self.allowed = allowed
        self.considered_tokens = considered_tokens
        self.pos_in_stream = lex_pos
        self.state = state

        message += '\n\n' + self.get_context(seq)
        if allowed:
            message += '\nExpecting: %s\n' % allowed

        super(UnexpectedCharacters, self).__init__(message)



class UnexpectedToken(ParseError, UnexpectedInput):
    def __init__(self, token, expected, considered_rules=None, state=None):
        self.token = token
        self.expected = expected     # XXX str shouldn't necessary
        self.line = getattr(token, 'line', '?')
        self.column = getattr(token, 'column', '?')
        self.considered_rules = considered_rules
        self.state = state
        self.pos_in_stream = getattr(token, 'pos_in_stream', None)

        message = ("Unexpected token %r at line %s, column %s.\n"
                   "Expected one of: \n\t* %s\n"
                   % (token, self.line, self.column, '\n\t* '.join(self.expected)))

        super(UnexpectedToken, self).__init__(message)

class VisitError(LarkError):
    def __init__(self, tree, orig_exc):
        self.tree = tree
        self.orig_exc = orig_exc

        message = 'Error trying to process rule "%s":\n\n%s' % (tree.data, orig_exc)
        super(VisitError, self).__init__(message)

try:
    STRING_TYPE = basestring
except NameError:   # Python 3
    STRING_TYPE = str


import types
from functools import wraps, partial
from contextlib import contextmanager

Str = type(u'')
try:
    classtype = types.ClassType # Python2
except AttributeError:
    classtype = type    # Python3

def smart_decorator(f, create_decorator):
    if isinstance(f, types.FunctionType):
        return wraps(f)(create_decorator(f, True))

    elif isinstance(f, (classtype, type, types.BuiltinFunctionType)):
        return wraps(f)(create_decorator(f, False))

    elif isinstance(f, types.MethodType):
        return wraps(f)(create_decorator(f.__func__, True))

    elif isinstance(f, partial):
        # wraps does not work for partials in 2.7: https://bugs.python.org/issue3445
        return create_decorator(f.__func__, True)

    else:
        return create_decorator(f.__func__.__call__, True)

def dedup_list(l):
    """Given a list (l) will removing duplicates from the list,
       preserving the original order of the list. Assumes that
       the list entrie are hashable."""
    dedup = set()
    return [ x for x in l if not (x in dedup or dedup.add(x))]


class Meta:
    def __init__(self):
        self.empty = True

class Tree(object):
    def __init__(self, data, children, meta=None):
        self.data = data
        self.children = children
        self._meta = meta

    @property
    def meta(self):
        if self._meta is None:
            self._meta = Meta()
        return self._meta

    def __repr__(self):
        return 'Tree(%s, %s)' % (self.data, self.children)

    def _pretty_label(self):
        return self.data

    def _pretty(self, level, indent_str):
        if len(self.children) == 1 and not isinstance(self.children[0], Tree):
            return [ indent_str*level, self._pretty_label(), '\t', '%s' % (self.children[0],), '\n']

        l = [ indent_str*level, self._pretty_label(), '\n' ]
        for n in self.children:
            if isinstance(n, Tree):
                l += n._pretty(level+1, indent_str)
            else:
                l += [ indent_str*(level+1), '%s' % (n,), '\n' ]

        return l

    def pretty(self, indent_str='  '):
        return ''.join(self._pretty(0, indent_str))

    def __eq__(self, other):
        try:
            return self.data == other.data and self.children == other.children
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.data, tuple(self.children)))

from inspect import getmembers, getmro

class Discard(Exception):
    pass

# Transformers

class Transformer:
    """Visits the tree recursively, starting with the leaves and finally the root (bottom-up)

    Calls its methods (provided by user via inheritance) according to tree.data
    The returned value replaces the old one in the structure.

    Can be used to implement map or reduce.
    """

    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            try:
                if getattr(f, 'meta', False):
                    return f(children, tree.meta)
                elif getattr(f, 'inline', False):
                    return f(*children)
                elif getattr(f, 'whole_tree', False):
                    if new_children is not None:
                        raise NotImplementedError("Doesn't work with the base Transformer class")
                    return f(tree)
                else:
                    return f(children)
            except (GrammarError, Discard):
                raise
            except Exception as e:
                raise VisitError(tree, e)

    def _transform_children(self, children):
        for c in children:
            try:
                yield self._transform_tree(c) if isinstance(c, Tree) else c
            except Discard:
                pass

    def _transform_tree(self, tree):
        children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree, children)

    def transform(self, tree):
        return self._transform_tree(tree)

    def __mul__(self, other):
        return TransformerChain(self, other)

    def __default__(self, data, children, meta):
        "Default operation on tree (for override)"
        return Tree(data, children, meta)

    @classmethod
    def _apply_decorator(cls, decorator, **kwargs):
        mro = getmro(cls)
        assert mro[0] is cls
        libmembers = {name for _cls in mro[1:] for name, _ in getmembers(_cls)}
        for name, value in getmembers(cls):
            if name.startswith('_') or name in libmembers:
                continue
            if not callable(cls.__dict__[name]):
                continue

            # Skip if v_args already applied (at the function level)
            if hasattr(cls.__dict__[name], 'vargs_applied'):
                continue

            static = isinstance(cls.__dict__[name], (staticmethod, classmethod))
            setattr(cls, name, decorator(value, static=static, **kwargs))
        return cls


class InlineTransformer(Transformer):   # XXX Deprecated
    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            return f(*children)


class TransformerChain(object):
    def __init__(self, *transformers):
        self.transformers = transformers

    def transform(self, tree):
        for t in self.transformers:
            tree = t.transform(tree)
        return tree

    def __mul__(self, other):
        return TransformerChain(*self.transformers + (other,))


class Transformer_InPlace(Transformer):
    "Non-recursive. Changes the tree in-place instead of returning new instances"
    def _transform_tree(self, tree):           # Cancel recursion
        return self._call_userfunc(tree)

    def transform(self, tree):
        for subtree in tree.iter_subtrees():
            subtree.children = list(self._transform_children(subtree.children))

        return self._transform_tree(tree)


class Transformer_InPlaceRecursive(Transformer):
    "Recursive. Changes the tree in-place instead of returning new instances"
    def _transform_tree(self, tree):
        tree.children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree)



# Visitors

class VisitorBase:
    def _call_userfunc(self, tree):
        return getattr(self, tree.data, self.__default__)(tree)

    def __default__(self, tree):
        "Default operation on tree (for override)"
        return tree


class Visitor(VisitorBase):
    """Bottom-up visitor, non-recursive

    Visits the tree, starting with the leaves and finally the root (bottom-up)
    Calls its methods (provided by user via inheritance) according to tree.data
    """


    def visit(self, tree):
        for subtree in tree.iter_subtrees():
            self._call_userfunc(subtree)
        return tree

class Visitor_Recursive(VisitorBase):
    """Bottom-up visitor, recursive

    Visits the tree, starting with the leaves and finally the root (bottom-up)
    Calls its methods (provided by user via inheritance) according to tree.data
    """

    def visit(self, tree):
        for child in tree.children:
            if isinstance(child, Tree):
                self.visit(child)

        f = getattr(self, tree.data, self.__default__)
        f(tree)
        return tree



def visit_children_decor(func):
    "See Interpreter"
    @wraps(func)
    def inner(cls, tree):
        values = cls.visit_children(tree)
        return func(cls, values)
    return inner


class Interpreter:
    """Top-down visitor, recursive

    Visits the tree, starting with the root and finally the leaves (top-down)
    Calls its methods (provided by user via inheritance) according to tree.data

    Unlike Transformer and Visitor, the Interpreter doesn't automatically visit its sub-branches.
    The user has to explicitly call visit_children, or use the @visit_children_decor
    """
    def visit(self, tree):
        return getattr(self, tree.data)(tree)

    def visit_children(self, tree):
        return [self.visit(child) if isinstance(child, Tree) else child
                for child in tree.children]

    def __getattr__(self, name):
        return self.__default__

    def __default__(self, tree):
        return self.visit_children(tree)




# Decorators

def _apply_decorator(obj, decorator, **kwargs):
    try:
        _apply = obj._apply_decorator
    except AttributeError:
        return decorator(obj, **kwargs)
    else:
        return _apply(decorator, **kwargs)



def _inline_args__func(func):
    @wraps(func)
    def create_decorator(_f, with_self):
        if with_self:
            def f(self, children):
                return _f(self, *children)
        else:
            def f(self, children):
                return _f(*children)
        return f

    return smart_decorator(func, create_decorator)


def inline_args(obj):   # XXX Deprecated
    return _apply_decorator(obj, _inline_args__func)



def _visitor_args_func_dec(func, inline=False, meta=False, whole_tree=False, static=False):
    assert [whole_tree, meta, inline].count(True) <= 1
    def create_decorator(_f, with_self):
        if with_self:
            def f(self, *args, **kwargs):
                return _f(self, *args, **kwargs)
        else:
            def f(self, *args, **kwargs):
                return _f(*args, **kwargs)
        return f

    if static:
        f = wraps(func)(create_decorator(func, False))
    else:
        f = smart_decorator(func, create_decorator)
    f.vargs_applied = True
    f.inline = inline
    f.meta = meta
    f.whole_tree = whole_tree
    return f

def v_args(inline=False, meta=False, tree=False):
    "A convenience decorator factory, for modifying the behavior of user-supplied visitor methods"
    if [tree, meta, inline].count(True) > 1:
        raise ValueError("Visitor functions can either accept tree, or meta, or be inlined. These cannot be combined.")
    def _visitor_args_dec(obj):
        return _apply_decorator(obj, _visitor_args_func_dec, inline=inline, meta=meta, whole_tree=tree)
    return _visitor_args_dec



class Indenter:
    def __init__(self):
        self.paren_level = None
        self.indent_level = None
        assert self.tab_len > 0

    def handle_NL(self, token):
        if self.paren_level > 0:
            return

        yield token

        indent_str = token.rsplit('\n', 1)[1] # Tabs and spaces
        indent = indent_str.count(' ') + indent_str.count('\t') * self.tab_len

        if indent > self.indent_level[-1]:
            self.indent_level.append(indent)
            yield Token.new_borrow_pos(self.INDENT_type, indent_str, token)
        else:
            while indent < self.indent_level[-1]:
                self.indent_level.pop()
                yield Token.new_borrow_pos(self.DEDENT_type, indent_str, token)

            assert indent == self.indent_level[-1], '%s != %s' % (indent, self.indent_level[-1])

    def _process(self, stream):
        for token in stream:
            if token.type == self.NL_type:
                for t in self.handle_NL(token):
                    yield t
            else:
                yield token

            if token.type in self.OPEN_PAREN_types:
                self.paren_level += 1
            elif token.type in self.CLOSE_PAREN_types:
                self.paren_level -= 1
                assert self.paren_level >= 0

        while len(self.indent_level) > 1:
            self.indent_level.pop()
            yield Token(self.DEDENT_type, '')

        assert self.indent_level == [0], self.indent_level

    def process(self, stream):
        self.paren_level = 0
        self.indent_level = [0]
        return self._process(stream)

    # XXX Hack for ContextualLexer. Maybe there's a more elegant solution?
    @property
    def always_accept(self):
        return (self.NL_type,)


class Token(Str):
    __slots__ = ('type', 'pos_in_stream', 'value', 'line', 'column', 'end_line', 'end_column')

    def __new__(cls, type_, value, pos_in_stream=None, line=None, column=None, end_line=None, end_column=None):
        try:
            self = super(Token, cls).__new__(cls, value)
        except UnicodeDecodeError:
            value = value.decode('latin1')
            self = super(Token, cls).__new__(cls, value)

        self.type = type_
        self.pos_in_stream = pos_in_stream
        self.value = value
        self.line = line
        self.column = column
        self.end_line = end_line
        self.end_column = end_column
        return self

    @classmethod
    def new_borrow_pos(cls, type_, value, borrow_t):
        return cls(type_, value, borrow_t.pos_in_stream, borrow_t.line, borrow_t.column, borrow_t.end_line, borrow_t.end_column)

    def __reduce__(self):
        return (self.__class__, (self.type, self.value, self.pos_in_stream, self.line, self.column, ))

    def __repr__(self):
        return 'Token(%s, %r)' % (self.type, self.value)

    def __deepcopy__(self, memo):
        return Token(self.type, self.value, self.pos_in_stream, self.line, self.column)

    def __eq__(self, other):
        if isinstance(other, Token) and self.type != other.type:
            return False

        return Str.__eq__(self, other)

    __hash__ = Str.__hash__


class LineCounter:
    def __init__(self):
        self.newline_char = '\n'
        self.char_pos = 0
        self.line = 1
        self.column = 1
        self.line_start_pos = 0

    def feed(self, token, test_newline=True):
        """Consume a token and calculate the new line & column.

        As an optional optimization, set test_newline=False is token doesn't contain a newline.
        """
        if test_newline:
            newlines = token.count(self.newline_char)
            if newlines:
                self.line += newlines
                self.line_start_pos = self.char_pos + token.rindex(self.newline_char) + 1

        self.char_pos += len(token)
        self.column = self.char_pos - self.line_start_pos + 1

class _Lex:
    "Built to serve both Lexer and ContextualLexer"
    def __init__(self, lexer, state=None):
        self.lexer = lexer
        self.state = state

    def lex(self, stream, newline_types, ignore_types):
        newline_types = frozenset(newline_types)
        ignore_types = frozenset(ignore_types)
        line_ctr = LineCounter()

        while line_ctr.char_pos < len(stream):
            lexer = self.lexer
            for mre, type_from_index in lexer.mres:
                m = mre.match(stream, line_ctr.char_pos)
                if not m:
                    continue

                t = None
                value = m.group(0)
                type_ = type_from_index[m.lastindex]
                if type_ not in ignore_types:
                    t = Token(type_, value, line_ctr.char_pos, line_ctr.line, line_ctr.column)
                    if t.type in lexer.callback:
                        t = lexer.callback[t.type](t)
                        if not isinstance(t, Token):
                            raise ValueError("Callbacks must return a token (returned %r)" % t)
                    yield t
                else:
                    if type_ in lexer.callback:
                        t = Token(type_, value, line_ctr.char_pos, line_ctr.line, line_ctr.column)
                        lexer.callback[type_](t)

                line_ctr.feed(value, type_ in newline_types)
                if t:
                    t.end_line = line_ctr.line
                    t.end_column = line_ctr.column

                break
            else:
                allowed = [v for m, tfi in lexer.mres for v in tfi.values()]
                raise UnexpectedCharacters(stream, line_ctr.char_pos, line_ctr.line, line_ctr.column, allowed=allowed, state=self.state)


class UnlessCallback:
    def __init__(self, mres):
        self.mres = mres

    def __call__(self, t):
        for mre, type_from_index in self.mres:
            m = mre.match(t.value)
            if m:
                t.type = type_from_index[m.lastindex]
                break
        return t

class CallChain:
    def __init__(self, callback1, callback2, cond):
        self.callback1 = callback1
        self.callback2 = callback2
        self.cond = cond

    def __call__(self, t):
        t2 = self.callback1(t)
        return self.callback2(t) if self.cond(t2) else t2



from functools import partial, wraps
from itertools import repeat, product


class ExpandSingleChild:
    def __init__(self, node_builder):
        self.node_builder = node_builder

    def __call__(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return self.node_builder(children)

class PropagatePositions:
    def __init__(self, node_builder):
        self.node_builder = node_builder

    def __call__(self, children):
        res = self.node_builder(children)

        if isinstance(res, Tree):
            for c in children:
                if isinstance(c, Tree) and c.children and not c.meta.empty:
                    res.meta.line = c.meta.line
                    res.meta.column = c.meta.column
                    res.meta.start_pos = c.meta.start_pos
                    res.meta.empty = False
                    break
                elif isinstance(c, Token):
                    res.meta.line = c.line
                    res.meta.column = c.column
                    res.meta.start_pos = c.pos_in_stream
                    res.meta.empty = False
                    break

            for c in reversed(children):
                if isinstance(c, Tree) and c.children and not c.meta.empty:
                    res.meta.end_line = c.meta.end_line
                    res.meta.end_column = c.meta.end_column
                    res.meta.end_pos = c.meta.end_pos
                    res.meta.empty = False
                    break
                elif isinstance(c, Token):
                    res.meta.end_line = c.end_line
                    res.meta.end_column = c.end_column
                    res.meta.end_pos = c.pos_in_stream + len(c.value)
                    res.meta.empty = False
                    break

        return res


class ChildFilter:
    def __init__(self, to_include, append_none, node_builder):
        self.node_builder = node_builder
        self.to_include = to_include
        self.append_none = append_none

    def __call__(self, children):
        filtered = []

        for i, to_expand, add_none in self.to_include:
            if add_none:
                filtered += [None] * add_none
            if to_expand:
                filtered += children[i].children
            else:
                filtered.append(children[i])

        if self.append_none:
            filtered += [None] * self.append_none

        return self.node_builder(filtered)

class ChildFilterLALR(ChildFilter):
    "Optimized childfilter for LALR (assumes no duplication in parse tree, so it's safe to change it)"

    def __call__(self, children):
        filtered = []
        for i, to_expand, add_none in self.to_include:
            if add_none:
                filtered += [None] * add_none
            if to_expand:
                if filtered:
                    filtered += children[i].children
                else:   # Optimize for left-recursion
                    filtered = children[i].children
            else:
                filtered.append(children[i])

        if self.append_none:
            filtered += [None] * self.append_none

        return self.node_builder(filtered)

class ChildFilterLALR_NoPlaceholders(ChildFilter):
    "Optimized childfilter for LALR (assumes no duplication in parse tree, so it's safe to change it)"
    def __init__(self, to_include, node_builder):
        self.node_builder = node_builder
        self.to_include = to_include

    def __call__(self, children):
        filtered = []
        for i, to_expand in self.to_include:
            if to_expand:
                if filtered:
                    filtered += children[i].children
                else:   # Optimize for left-recursion
                    filtered = children[i].children
            else:
                filtered.append(children[i])
        return self.node_builder(filtered)

def _should_expand(sym):
    return not sym.is_term and sym.name.startswith('_')

def maybe_create_child_filter(expansion, keep_all_tokens, ambiguous, _empty_indices):
    # Prepare empty_indices as: How many Nones to insert at each index?
    if _empty_indices:
        assert _empty_indices.count(False) == len(expansion)
        s = ''.join(str(int(b)) for b in _empty_indices)
        empty_indices = [len(ones) for ones in s.split('0')]
        assert len(empty_indices) == len(expansion)+1, (empty_indices, len(expansion))
    else:
        empty_indices = [0] * (len(expansion)+1)

    to_include = []
    nones_to_add = 0
    for i, sym in enumerate(expansion):
        nones_to_add += empty_indices[i]
        if keep_all_tokens or not (sym.is_term and sym.filter_out):
            to_include.append((i, _should_expand(sym), nones_to_add))
            nones_to_add = 0

    nones_to_add += empty_indices[len(expansion)]

    if _empty_indices or len(to_include) < len(expansion) or any(to_expand for i, to_expand,_ in to_include):
        if _empty_indices or ambiguous:
            return partial(ChildFilter if ambiguous else ChildFilterLALR, to_include, nones_to_add)
        else:
            # LALR without placeholders
            return partial(ChildFilterLALR_NoPlaceholders, [(i, x) for i,x,_ in to_include])

class AmbiguousExpander:
    """Deal with the case where we're expanding children ('_rule') into a parent but the children
       are ambiguous. i.e. (parent->_ambig->_expand_this_rule). In this case, make the parent itself
       ambiguous with as many copies as their are ambiguous children, and then copy the ambiguous children
       into the right parents in the right places, essentially shifting the ambiguiuty up the tree."""
    def __init__(self, to_expand, tree_class, node_builder):
        self.node_builder = node_builder
        self.tree_class = tree_class
        self.to_expand = to_expand

    def __call__(self, children):
        def _is_ambig_tree(child):
            return hasattr(child, 'data') and child.data == '_ambig'

        #### When we're repeatedly expanding ambiguities we can end up with nested ambiguities.
        #    All children of an _ambig node should be a derivation of that ambig node, hence
        #    it is safe to assume that if we see an _ambig node nested within an ambig node
        #    it is safe to simply expand it into the parent _ambig node as an alternative derivation.
        ambiguous = []
        for i, child in enumerate(children):
            if _is_ambig_tree(child):
                if i in self.to_expand:
                    ambiguous.append(i)

                to_expand = [j for j, grandchild in enumerate(child.children) if _is_ambig_tree(grandchild)]
                child.expand_kids_by_index(*to_expand)

        if not ambiguous:
            return self.node_builder(children)

        expand = [ iter(child.children) if i in ambiguous else repeat(child) for i, child in enumerate(children) ]
        return self.tree_class('_ambig', [self.node_builder(list(f[0])) for f in product(zip(*expand))])

def maybe_create_ambiguous_expander(tree_class, expansion, keep_all_tokens):
    to_expand = [i for i, sym in enumerate(expansion)
                 if keep_all_tokens or ((not (sym.is_term and sym.filter_out)) and _should_expand(sym))]
    if to_expand:
        return partial(AmbiguousExpander, to_expand, tree_class)

class Callback(object):
    pass


def ptb_inline_args(func):
    @wraps(func)
    def f(children):
        return func(*children)
    return f

class ParseTreeBuilder:
    def __init__(self, rules, tree_class, propagate_positions=False, keep_all_tokens=False, ambiguous=False, maybe_placeholders=False):
        self.tree_class = tree_class
        self.propagate_positions = propagate_positions
        self.always_keep_all_tokens = keep_all_tokens
        self.ambiguous = ambiguous
        self.maybe_placeholders = maybe_placeholders

        self.rule_builders = list(self._init_builders(rules))

        self.user_aliases = {}

    def _init_builders(self, rules):
        for rule in rules:
            options = rule.options
            keep_all_tokens = self.always_keep_all_tokens or (options.keep_all_tokens if options else False)
            expand_single_child = options.expand1 if options else False

            wrapper_chain = filter(None, [
                (expand_single_child and not rule.alias) and ExpandSingleChild,
                maybe_create_child_filter(rule.expansion, keep_all_tokens, self.ambiguous, options.empty_indices if self.maybe_placeholders and options else None),
                self.propagate_positions and PropagatePositions,
                self.ambiguous and maybe_create_ambiguous_expander(self.tree_class, rule.expansion, keep_all_tokens),
            ])

            yield rule, wrapper_chain


    def create_callback(self, transformer=None):
        callback = Callback()

        i = 0
        for rule, wrapper_chain in self.rule_builders:
            internal_callback_name = '_cb%d_%s' % (i, rule.origin)
            i += 1

            user_callback_name = rule.alias or rule.origin.name
            try:
                f = getattr(transformer, user_callback_name)
                assert not getattr(f, 'meta', False), "Meta args not supported for internal transformer"
                # XXX InlineTransformer is deprecated!
                if getattr(f, 'inline', False) or isinstance(transformer, InlineTransformer):
                    f = ptb_inline_args(f)
            except AttributeError:
                f = partial(self.tree_class, user_callback_name)

            self.user_aliases[rule] = rule.alias
            rule.alias = internal_callback_name

            for w in wrapper_chain:
                f = w(f)

            if hasattr(callback, internal_callback_name):
                raise GrammarError("Rule '%s' already exists" % (rule,))
            setattr(callback, internal_callback_name, f)

        return callback



class _Parser:
    def __init__(self, parse_table, callbacks):
        self.states = parse_table.states
        self.start_state = parse_table.start_state
        self.end_state = parse_table.end_state
        self.callbacks = callbacks

    def parse(self, seq, set_state=None):
        token = None
        stream = iter(seq)
        states = self.states

        state_stack = [self.start_state]
        value_stack = []

        if set_state: set_state(self.start_state)

        def get_action(token):
            state = state_stack[-1]
            try:
                return states[state][token.type]
            except KeyError:
                expected = [s for s in states[state].keys() if s.isupper()]
                raise UnexpectedToken(token, expected, state=state)

        def reduce(rule):
            size = len(rule.expansion)
            if size:
                s = value_stack[-size:]
                del state_stack[-size:]
                del value_stack[-size:]
            else:
                s = []

            value = self.callbacks[rule](s)

            _action, new_state = states[state_stack[-1]][rule.origin.name]
            assert _action is Shift
            state_stack.append(new_state)
            value_stack.append(value)

        # Main LALR-parser loop
        for token in stream:
            while True:
                action, arg = get_action(token)
                assert arg != self.end_state

                if action is Shift:
                    state_stack.append(arg)
                    value_stack.append(token)
                    if set_state: set_state(arg)
                    break # next token
                else:
                    reduce(arg)

        token = Token.new_borrow_pos('$END', '', token) if token else Token('$END', '', 0, 1, 1)
        while True:
            _action, arg = get_action(token)
            if _action is Shift:
                assert arg == self.end_state
                val ,= value_stack
                return val
            else:
                reduce(arg)


class Symbol(object):
    is_term = NotImplemented

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        assert isinstance(other, Symbol), other
        return self.is_term == other.is_term and self.name == other.name

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.name)

    fullrepr = property(__repr__)

class Terminal(Symbol):
    is_term = True

    def __init__(self, name, filter_out=False):
        self.name = name
        self.filter_out = filter_out

    @property
    def fullrepr(self):
        return '%s(%r, %r)' % (type(self).__name__, self.name, self.filter_out)


class NonTerminal(Symbol):
    is_term = False

class Rule(object):
    """
        origin : a symbol
        expansion : a list of symbols
        order : index of this expansion amongst all rules of the same name
    """
    __slots__ = ('origin', 'expansion', 'alias', 'options', 'order', '_hash')
    def __init__(self, origin, expansion, order=0, alias=None, options=None):
        self.origin = origin
        self.expansion = expansion
        self.alias = alias
        self.order = order
        self.options = options
        self._hash = hash((self.origin, tuple(self.expansion)))


    def __str__(self):
        return '<%s : %s>' % (self.origin.name, ' '.join(x.name for x in self.expansion))

    def __repr__(self):
        return 'Rule(%r, %r, %r, %r)' % (self.origin, self.expansion, self.alias, self.options)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Rule):
            return False
        return self.origin == other.origin and self.expansion == other.expansion


class RuleOptions:
    def __init__(self, keep_all_tokens=False, expand1=False, priority=None):
        self.keep_all_tokens = keep_all_tokens
        self.expand1 = expand1
        self.priority = priority
        self.empty_indices = ()

    def __repr__(self):
        return 'RuleOptions(%r, %r, %r)' % (
            self.keep_all_tokens,
            self.expand1,
            self.priority,
        )

Shift = 0
Reduce = 1
import re
class LexerRegexps: pass
NEWLINE_TYPES = ['FILE_PATH', 'COMMENT', 'WS']
IGNORE_TYPES = ['COMMENT', 'WS']
LEXERS = {}
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[0] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[1] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BASE>_(?:[0-9])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BASE',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'END',
   12: 'VAR',
   13: 'IF',
   14: 'DIV',
   15: 'ADD',
   16: 'B_AND',
   17: 'B_OR',
   18: 'B_XOR',
   19: 'GREATER',
   20: 'LPAR',
   21: 'MULT',
   22: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[2] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[3] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[4] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[5] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[6] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[7] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[8] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[9] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[10] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[11] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[12] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[13] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[14] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[15] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[16] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[17] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[18] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[19] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[20] = (lexer_regexps)
MRES = (
[('(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)',
  {1: 'COMMENT', 2: 'WS'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[21] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[22] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[23] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[24] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[25] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[26] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)',
  {1: 'IDENTIFIER', 2: 'COMMENT', 3: 'WS'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[27] = (lexer_regexps)
MRES = (
[('(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<__ANON_0>")',
  {1: 'COMMENT', 2: 'WS', 3: '__ANON_0'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[28] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[29] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[30] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[31] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[32] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[33] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[34] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[35] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[36] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[37] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[38] = (lexer_regexps)
MRES = (
[('(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<RPAR>\\))',
  {1: 'COMMENT', 2: 'WS', 3: 'RPAR'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[39] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[40] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[41] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[42] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[43] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[44] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[45] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[46] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[47] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[48] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[49] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[50] = (lexer_regexps)
MRES = (
[('(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)',
  {1: 'COMMENT', 2: 'WS'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[51] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[52] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[53] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[54] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[55] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[56] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[57] = (lexer_regexps)
MRES = (
[('(?P<FILE_PATH>(?:[a-zA-Z]\\:\\\\\\\\|\\.\\\\|\\.\\.\\\\|\\~)?(?:[^\\<\\>\\:"\\/\\\\\\|\\?\\*\\0-\\37]|(?:\\\\|\\/))+)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)',
  {1: 'FILE_PATH', 2: 'COMMENT', 3: 'WS'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[58] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[59] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<DIV>\\/)|(?P<ADD>\\+)|(?P<B_AND>\\&)|(?P<B_OR>\\|)|(?P<B_XOR>\\^)|(?P<GREATER>\\>)|(?P<LPAR>\\()|(?P<MULT>\\*)|(?P<RPAR>\\))',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'DIV',
   14: 'ADD',
   15: 'B_AND',
   16: 'B_OR',
   17: 'B_XOR',
   18: 'GREATER',
   19: 'LPAR',
   20: 'MULT',
   21: 'RPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[60] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[61] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[62] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[63] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[64] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[65] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[66] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'READ',
   6: 'VAR',
   7: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)',
                 {1: 'READ', 2: 'VAR'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[67] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[68] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'BREAK',
   6: 'WRITE',
   7: 'LOOP',
   8: 'READ',
   9: 'END',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'BREAK',
                  2: 'WRITE',
                  3: 'LOOP',
                  4: 'READ',
                  5: 'END',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[69] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<END>(?i:END))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'END',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<END>(?i:END)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'END',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[70] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'DEFINE',
   6: 'BREAK',
   7: 'WRITE',
   8: 'LOOP',
   9: 'READ',
   10: 'VAR',
   11: 'IF',
   12: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'DEFINE',
                  2: 'BREAK',
                  3: 'WRITE',
                  4: 'LOOP',
                  5: 'READ',
                  6: 'VAR',
                  7: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[71] = (lexer_regexps)
MRES = (
[('(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<__ANON_0>")',
  {1: 'COMMENT', 2: 'WS', 3: '__ANON_0'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[72] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<AS>(?i:AS))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'AS',
   13: 'IF',
   14: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<AS>(?i:AS)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'AS',
                  9: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[73] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[74] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)',
  {1: 'IDENTIFIER', 2: 'COMMENT', 3: 'WS'})]
)
LEXER_CALLBACK = (
{}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[75] = (lexer_regexps)
MRES = (
[('(?P<IDENTIFIER>(?:(?:[A-Z]|[a-z])|\\-)(?:(?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.)|\\-))*)|(?P<NUMBER_STRING>[0-9](?:(?:(?:(?:[A-Z]|[a-z])|[0-9])|\\.))*)|(?P<COMMENT>(?:\\#(?:[^\n'
  '])*|\\/\\*(?:.)*\\*\\/))|(?P<WS>(?:[ \t\x0c'
  '\r\n'
  '])+)|(?P<INCL>(?i:INCLUDE))|(?P<DEFINE>(?i:DEFINE))|(?P<BREAK>(?i:BREAK))|(?P<WRITE>(?i:WRITE))|(?P<LOOP>(?i:LOOP))|(?P<READ>(?i:READ))|(?P<VAR>(?i:VAR))|(?P<IF>(?i:IF))|(?P<LPAR>\\()',
  {1: 'IDENTIFIER',
   2: 'NUMBER_STRING',
   3: 'COMMENT',
   4: 'WS',
   5: 'INCL',
   6: 'DEFINE',
   7: 'BREAK',
   8: 'WRITE',
   9: 'LOOP',
   10: 'READ',
   11: 'VAR',
   12: 'IF',
   13: 'LPAR'})]
)
LEXER_CALLBACK = (
{'IDENTIFIER': [('(?P<INCL>(?i:INCLUDE)$)|(?P<DEFINE>(?i:DEFINE)$)|(?P<BREAK>(?i:BREAK)$)|(?P<WRITE>(?i:WRITE)$)|(?P<LOOP>(?i:LOOP)$)|(?P<READ>(?i:READ)$)|(?P<VAR>(?i:VAR)$)|(?P<IF>(?i:IF)$)',
                 {1: 'INCL',
                  2: 'DEFINE',
                  3: 'BREAK',
                  4: 'WRITE',
                  5: 'LOOP',
                  6: 'READ',
                  7: 'VAR',
                  8: 'IF'})]}
)
lexer_regexps = LexerRegexps()
lexer_regexps.mres = [(re.compile(p), d) for p, d in MRES]
lexer_regexps.callback = {n: UnlessCallback([(re.compile(p), d) for p, d in mres])
                          for n, mres in LEXER_CALLBACK.items()}
LEXERS[76] = (lexer_regexps)
class ContextualLexer:
    def __init__(self):
        self.lexers = LEXERS
        self.set_parser_state(None)
    def set_parser_state(self, state):
        self.parser_state = state
    def lex(self, stream):
        newline_types = NEWLINE_TYPES
        ignore_types = IGNORE_TYPES
        lexers = LEXERS
        l = _Lex(lexers[self.parser_state], self.parser_state)
        for x in l.lex(stream, newline_types, ignore_types):
            yield x
            l.lexer = lexers[self.parser_state]
            l.state = self.parser_state
CON_LEXER = ContextualLexer()
def lex(stream):
    return CON_LEXER.lex(stream)
RULES = {
  0: Rule(NonTerminal('start'), [NonTerminal('__anon_star_0'), NonTerminal('__anon_star_1')], alias=None, options=RuleOptions(False, False, None)),
  1: Rule(NonTerminal('start'), [NonTerminal('__anon_star_0')], alias=None, options=RuleOptions(False, False, None)),
  2: Rule(NonTerminal('start'), [NonTerminal('__anon_star_1')], alias=None, options=RuleOptions(False, False, None)),
  3: Rule(NonTerminal('start'), [], alias=None, options=RuleOptions(False, False, None)),
  4: Rule(NonTerminal('include'), [Terminal('INCL', False), Terminal('__ANON_0', False), Terminal('FILE_PATH', False), Terminal('__ANON_0', False), NonTerminal('include_as')], alias=None, options=RuleOptions(False, False, None)),
  5: Rule(NonTerminal('include'), [Terminal('INCL', False), Terminal('__ANON_0', False), Terminal('FILE_PATH', False), Terminal('__ANON_0', False)], alias=None, options=RuleOptions(False, False, None)),
  6: Rule(NonTerminal('include_as'), [Terminal('AS', True), Terminal('IDENTIFIER', False)], alias=None, options=RuleOptions(False, False, None)),
  7: Rule(NonTerminal('eval_call'), [Terminal('EVAL', False), NonTerminal('sum')], alias=None, options=RuleOptions(False, False, None)),
  8: Rule(NonTerminal('expression'), [NonTerminal('sum')], alias=None, options=RuleOptions(False, False, None)),
  9: Rule(NonTerminal('expression'), [NonTerminal('if_call')], alias=None, options=RuleOptions(False, False, None)),
  10: Rule(NonTerminal('expression'), [NonTerminal('loop_call')], alias=None, options=RuleOptions(False, False, None)),
  11: Rule(NonTerminal('expression'), [Terminal('BREAK', False)], alias=None, options=RuleOptions(False, False, None)),
  12: Rule(NonTerminal('expression'), [NonTerminal('write')], alias=None, options=RuleOptions(False, False, None)),
  13: Rule(NonTerminal('write'), [Terminal('WRITE', False), NonTerminal('sum')], alias=None, options=RuleOptions(False, False, None)),
  14: Rule(NonTerminal('block'), [NonTerminal('__anon_star_2'), Terminal('END', False)], alias=None, options=RuleOptions(False, False, None)),
  15: Rule(NonTerminal('block'), [Terminal('END', False)], alias=None, options=RuleOptions(False, False, None)),
  16: Rule(NonTerminal('function_definition'), [Terminal('DEFINE', True), Terminal('IDENTIFIER', False), NonTerminal('block')], alias=None, options=RuleOptions(False, False, None)),
  17: Rule(NonTerminal('function_call'), [Terminal('IDENTIFIER', False), NonTerminal('sum')], alias=None, options=RuleOptions(False, False, None)),
  18: Rule(NonTerminal('if_call'), [Terminal('IF', False), NonTerminal('sum'), NonTerminal('block')], alias=None, options=RuleOptions(False, False, None)),
  19: Rule(NonTerminal('loop_call'), [Terminal('LOOP', False), NonTerminal('block')], alias=None, options=RuleOptions(False, False, None)),
  20: Rule(NonTerminal('sum'), [NonTerminal('__anon_star_3'), NonTerminal('product')], alias=None, options=RuleOptions(False, False, None)),
  21: Rule(NonTerminal('sum'), [NonTerminal('product')], alias=None, options=RuleOptions(False, False, None)),
  22: Rule(NonTerminal('product'), [NonTerminal('__anon_star_4'), NonTerminal('compare')], alias=None, options=RuleOptions(False, False, None)),
  23: Rule(NonTerminal('product'), [NonTerminal('compare')], alias=None, options=RuleOptions(False, False, None)),
  24: Rule(NonTerminal('compare'), [NonTerminal('__anon_star_5'), NonTerminal('bitwise')], alias=None, options=RuleOptions(False, False, None)),
  25: Rule(NonTerminal('compare'), [NonTerminal('bitwise')], alias=None, options=RuleOptions(False, False, None)),
  26: Rule(NonTerminal('bitwise'), [NonTerminal('__anon_star_6'), NonTerminal('clause')], alias=None, options=RuleOptions(False, False, None)),
  27: Rule(NonTerminal('bitwise'), [NonTerminal('clause')], alias=None, options=RuleOptions(False, False, None)),
  28: Rule(NonTerminal('clause'), [Terminal('LPAR', True), NonTerminal('sum'), Terminal('RPAR', True)], alias=None, options=RuleOptions(False, False, None)),
  29: Rule(NonTerminal('clause'), [NonTerminal('value')], alias=None, options=RuleOptions(False, False, None)),
  30: Rule(NonTerminal('value'), [NonTerminal('number')], alias=None, options=RuleOptions(False, False, None)),
  31: Rule(NonTerminal('value'), [NonTerminal('function_call')], alias=None, options=RuleOptions(False, False, None)),
  32: Rule(NonTerminal('value'), [Terminal('VAR', False)], alias=None, options=RuleOptions(False, False, None)),
  33: Rule(NonTerminal('value'), [Terminal('READ', False)], alias=None, options=RuleOptions(False, False, None)),
  34: Rule(NonTerminal('number'), [Terminal('NUMBER_STRING', False), Terminal('BASE', False)], alias=None, options=RuleOptions(False, False, None)),
  35: Rule(NonTerminal('number'), [Terminal('NUMBER_STRING', False)], alias=None, options=RuleOptions(False, False, None)),
  36: Rule(NonTerminal('__anon_star_0'), [NonTerminal('include')], alias=None, options=None),
  37: Rule(NonTerminal('__anon_star_0'), [NonTerminal('__anon_star_0'), NonTerminal('include')], alias=None, options=None),
  38: Rule(NonTerminal('__anon_star_1'), [NonTerminal('expression')], alias=None, options=None),
  39: Rule(NonTerminal('__anon_star_1'), [NonTerminal('function_definition')], alias=None, options=None),
  40: Rule(NonTerminal('__anon_star_1'), [NonTerminal('__anon_star_1'), NonTerminal('expression')], alias=None, options=None),
  41: Rule(NonTerminal('__anon_star_1'), [NonTerminal('__anon_star_1'), NonTerminal('function_definition')], alias=None, options=None),
  42: Rule(NonTerminal('__anon_star_2'), [NonTerminal('expression')], alias=None, options=None),
  43: Rule(NonTerminal('__anon_star_2'), [NonTerminal('__anon_star_2'), NonTerminal('expression')], alias=None, options=None),
  44: Rule(NonTerminal('__anon_star_3'), [NonTerminal('product'), Terminal('ADD', False)], alias=None, options=None),
  45: Rule(NonTerminal('__anon_star_3'), [NonTerminal('__anon_star_3'), NonTerminal('product'), Terminal('ADD', False)], alias=None, options=None),
  46: Rule(NonTerminal('__anon_star_4'), [NonTerminal('compare'), Terminal('MULT', False)], alias=None, options=None),
  47: Rule(NonTerminal('__anon_star_4'), [NonTerminal('compare'), Terminal('DIV', False)], alias=None, options=None),
  48: Rule(NonTerminal('__anon_star_4'), [NonTerminal('__anon_star_4'), NonTerminal('compare'), Terminal('MULT', False)], alias=None, options=None),
  49: Rule(NonTerminal('__anon_star_4'), [NonTerminal('__anon_star_4'), NonTerminal('compare'), Terminal('DIV', False)], alias=None, options=None),
  50: Rule(NonTerminal('__anon_star_5'), [NonTerminal('bitwise'), Terminal('GREATER', False)], alias=None, options=None),
  51: Rule(NonTerminal('__anon_star_5'), [NonTerminal('__anon_star_5'), NonTerminal('bitwise'), Terminal('GREATER', False)], alias=None, options=None),
  52: Rule(NonTerminal('__anon_star_6'), [NonTerminal('clause'), Terminal('B_AND', False)], alias=None, options=None),
  53: Rule(NonTerminal('__anon_star_6'), [NonTerminal('clause'), Terminal('B_OR', False)], alias=None, options=None),
  54: Rule(NonTerminal('__anon_star_6'), [NonTerminal('clause'), Terminal('B_XOR', False)], alias=None, options=None),
  55: Rule(NonTerminal('__anon_star_6'), [NonTerminal('__anon_star_6'), NonTerminal('clause'), Terminal('B_AND', False)], alias=None, options=None),
  56: Rule(NonTerminal('__anon_star_6'), [NonTerminal('__anon_star_6'), NonTerminal('clause'), Terminal('B_OR', False)], alias=None, options=None),
  57: Rule(NonTerminal('__anon_star_6'), [NonTerminal('__anon_star_6'), NonTerminal('clause'), Terminal('B_XOR', False)], alias=None, options=None),
}
parse_tree_builder = ParseTreeBuilder(RULES.values(), Tree)
class ParseTable: pass
parse_table = ParseTable()
STATES = {
  0: {0: (1, 3), 1: (0, 1), 2: (0, 2), 3: (0, 3), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 8: (0, 8), 9: (0, 9), 10: (0, 10), 11: (0, 11), 12: (0, 12), 13: (0, 13), 14: (0, 14), 15: (0, 15), 16: (0, 16), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 21: (0, 21), 22: (0, 22), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 27: (0, 27), 28: (0, 28), 29: (0, 29), 30: (0, 30), 31: (0, 31), 32: (0, 32)},
  1: {27: (1, 25), 22: (1, 25), 6: (1, 25), 18: (1, 25), 9: (1, 25), 33: (1, 25), 32: (1, 25), 34: (1, 25), 35: (1, 25), 36: (1, 25), 37: (1, 25), 4: (1, 25), 38: (1, 25), 39: (1, 25), 2: (1, 25), 7: (1, 25), 0: (1, 25), 40: (1, 25), 26: (1, 25), 41: (0, 33)},
  2: {27: (1, 35), 22: (1, 35), 6: (1, 35), 18: (1, 35), 9: (1, 35), 33: (1, 35), 32: (1, 35), 34: (1, 35), 35: (1, 35), 36: (1, 35), 37: (1, 35), 4: (1, 35), 38: (1, 35), 39: (1, 35), 2: (1, 35), 7: (1, 35), 0: (1, 35), 40: (1, 35), 26: (1, 35), 41: (1, 35), 42: (0, 34)},
  3: {0: (1, 1), 1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 10: (0, 10), 11: (0, 11), 12: (0, 12), 13: (0, 13), 14: (0, 14), 15: (0, 15), 16: (0, 16), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 8: (0, 35), 22: (0, 22), 31: (0, 36), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 27: (0, 27), 28: (0, 28), 29: (0, 29), 30: (0, 30), 32: (0, 32)},
  4: {27: (1, 32), 22: (1, 32), 6: (1, 32), 18: (1, 32), 9: (1, 32), 33: (1, 32), 32: (1, 32), 34: (1, 32), 35: (1, 32), 36: (1, 32), 37: (1, 32), 4: (1, 32), 38: (1, 32), 39: (1, 32), 2: (1, 32), 7: (1, 32), 0: (1, 32), 40: (1, 32), 26: (1, 32), 41: (1, 32)},
  5: {27: (1, 23), 22: (1, 23), 6: (1, 23), 18: (1, 23), 9: (1, 23), 33: (0, 37), 32: (1, 23), 34: (1, 23), 35: (0, 38), 36: (1, 23), 37: (1, 23), 4: (1, 23), 38: (1, 23), 39: (1, 23), 2: (1, 23), 7: (1, 23), 0: (1, 23), 40: (1, 23), 26: (1, 23), 41: (1, 23)},
  6: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 11: (0, 11), 10: (0, 10), 12: (0, 12), 14: (0, 14), 16: (0, 16), 17: (0, 17), 19: (0, 19), 20: (0, 20), 25: (0, 39), 26: (0, 26), 30: (0, 30)},
  7: {27: (1, 33), 22: (1, 33), 6: (1, 33), 18: (1, 33), 9: (1, 33), 33: (1, 33), 32: (1, 33), 34: (1, 33), 35: (1, 33), 36: (1, 33), 37: (1, 33), 4: (1, 33), 38: (1, 33), 39: (1, 33), 2: (1, 33), 7: (1, 33), 0: (1, 33), 40: (1, 33), 26: (1, 33), 41: (1, 33)},
  8: {0: (1, 2), 1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 14: (0, 14), 16: (0, 16), 15: (0, 40), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 27: (0, 27), 30: (0, 30), 32: (0, 32), 29: (0, 41)},
  9: {27: (1, 11), 22: (1, 11), 6: (1, 11), 18: (1, 11), 9: (1, 11), 32: (1, 11), 4: (1, 11), 38: (1, 11), 2: (1, 11), 7: (1, 11), 0: (1, 11), 26: (1, 11)},
  10: {27: (1, 21), 22: (1, 21), 6: (1, 21), 18: (1, 21), 9: (1, 21), 33: (1, 21), 32: (1, 21), 34: (0, 42), 35: (1, 21), 36: (1, 21), 37: (1, 21), 4: (1, 21), 38: (1, 21), 39: (1, 21), 2: (1, 21), 7: (1, 21), 0: (1, 21), 40: (1, 21), 26: (1, 21), 41: (1, 21)},
  11: {1: (0, 1), 2: (0, 2), 5: (0, 5), 14: (0, 14), 4: (0, 4), 26: (0, 26), 6: (0, 6), 7: (0, 7), 19: (0, 19), 17: (0, 17), 12: (0, 12), 16: (0, 16), 30: (0, 30), 10: (0, 43), 20: (0, 20)},
  12: {27: (1, 29), 22: (1, 29), 6: (1, 29), 18: (1, 29), 9: (1, 29), 33: (1, 29), 32: (1, 29), 34: (1, 29), 35: (1, 29), 36: (1, 29), 37: (1, 29), 4: (1, 29), 38: (1, 29), 39: (1, 29), 2: (1, 29), 7: (1, 29), 0: (1, 29), 40: (1, 29), 26: (1, 29), 41: (1, 29)},
  13: {27: (1, 10), 22: (1, 10), 6: (1, 10), 18: (1, 10), 9: (1, 10), 32: (1, 10), 4: (1, 10), 38: (1, 10), 2: (1, 10), 7: (1, 10), 0: (1, 10), 26: (1, 10)},
  14: {1: (0, 1), 2: (0, 2), 4: (0, 4), 26: (0, 26), 6: (0, 6), 5: (0, 44), 7: (0, 7), 19: (0, 19), 17: (0, 17), 12: (0, 12), 16: (0, 16), 30: (0, 30), 20: (0, 20)},
  15: {27: (1, 38), 22: (1, 38), 6: (1, 38), 18: (1, 38), 9: (1, 38), 32: (1, 38), 4: (1, 38), 2: (1, 38), 7: (1, 38), 0: (1, 38), 26: (1, 38)},
  16: {2: (0, 2), 4: (0, 4), 26: (0, 26), 6: (0, 6), 7: (0, 7), 19: (0, 19), 17: (0, 17), 12: (0, 12), 30: (0, 30), 1: (0, 45), 20: (0, 20)},
  17: {30: (0, 30), 2: (0, 2), 19: (0, 46), 4: (0, 4), 20: (0, 20), 26: (0, 26), 6: (0, 6), 7: (0, 7), 12: (0, 12)},
  18: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 11: (0, 11), 10: (0, 10), 12: (0, 12), 14: (0, 14), 16: (0, 16), 17: (0, 17), 19: (0, 19), 20: (0, 20), 26: (0, 26), 30: (0, 30), 25: (0, 47)},
  19: {27: (1, 27), 22: (1, 27), 6: (1, 27), 18: (1, 27), 9: (1, 27), 33: (1, 27), 32: (1, 27), 34: (1, 27), 35: (1, 27), 36: (0, 49), 37: (0, 50), 4: (1, 27), 38: (1, 27), 39: (0, 48), 2: (1, 27), 7: (1, 27), 0: (1, 27), 40: (1, 27), 26: (1, 27), 41: (1, 27)},
  20: {27: (1, 30), 22: (1, 30), 6: (1, 30), 18: (1, 30), 9: (1, 30), 33: (1, 30), 32: (1, 30), 34: (1, 30), 35: (1, 30), 36: (1, 30), 37: (1, 30), 4: (1, 30), 38: (1, 30), 39: (1, 30), 2: (1, 30), 7: (1, 30), 0: (1, 30), 40: (1, 30), 26: (1, 30), 41: (1, 30)},
  21: {0: (0, 51)},
  22: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 38: (0, 52), 14: (0, 14), 16: (0, 16), 43: (0, 53), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 15: (0, 54), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 30: (0, 30), 44: (0, 55), 32: (0, 32)},
  23: {27: (1, 12), 22: (1, 12), 6: (1, 12), 18: (1, 12), 9: (1, 12), 32: (1, 12), 4: (1, 12), 38: (1, 12), 2: (1, 12), 7: (1, 12), 0: (1, 12), 26: (1, 12)},
  24: {27: (1, 9), 22: (1, 9), 6: (1, 9), 18: (1, 9), 9: (1, 9), 32: (1, 9), 4: (1, 9), 38: (1, 9), 2: (1, 9), 7: (1, 9), 0: (1, 9), 26: (1, 9)},
  25: {27: (1, 8), 22: (1, 8), 6: (1, 8), 18: (1, 8), 9: (1, 8), 32: (1, 8), 4: (1, 8), 38: (1, 8), 2: (1, 8), 7: (1, 8), 0: (1, 8), 26: (1, 8)},
  26: {25: (0, 56), 1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 11: (0, 11), 10: (0, 10), 12: (0, 12), 14: (0, 14), 16: (0, 16), 17: (0, 17), 19: (0, 19), 20: (0, 20), 26: (0, 26), 30: (0, 30)},
  27: {26: (0, 57)},
  28: {45: (0, 58)},
  29: {27: (1, 39), 22: (1, 39), 6: (1, 39), 18: (1, 39), 9: (1, 39), 32: (1, 39), 4: (1, 39), 2: (1, 39), 7: (1, 39), 0: (1, 39), 26: (1, 39)},
  30: {27: (1, 31), 22: (1, 31), 6: (1, 31), 18: (1, 31), 9: (1, 31), 33: (1, 31), 32: (1, 31), 34: (1, 31), 35: (1, 31), 36: (1, 31), 37: (1, 31), 4: (1, 31), 38: (1, 31), 39: (1, 31), 2: (1, 31), 7: (1, 31), 0: (1, 31), 40: (1, 31), 26: (1, 31), 41: (1, 31)},
  31: {27: (1, 36), 22: (1, 36), 6: (1, 36), 18: (1, 36), 9: (1, 36), 32: (1, 36), 4: (1, 36), 28: (1, 36), 2: (1, 36), 7: (1, 36), 0: (1, 36), 26: (1, 36)},
  32: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 25: (0, 59), 11: (0, 11), 10: (0, 10), 12: (0, 12), 14: (0, 14), 16: (0, 16), 17: (0, 17), 19: (0, 19), 20: (0, 20), 26: (0, 26), 30: (0, 30)},
  33: {4: (1, 50), 2: (1, 50), 7: (1, 50), 6: (1, 50), 26: (1, 50)},
  34: {27: (1, 34), 22: (1, 34), 6: (1, 34), 18: (1, 34), 9: (1, 34), 33: (1, 34), 32: (1, 34), 34: (1, 34), 35: (1, 34), 36: (1, 34), 37: (1, 34), 4: (1, 34), 38: (1, 34), 39: (1, 34), 2: (1, 34), 7: (1, 34), 0: (1, 34), 40: (1, 34), 26: (1, 34), 41: (1, 34)},
  35: {0: (1, 0), 1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 14: (0, 14), 16: (0, 16), 15: (0, 40), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 27: (0, 27), 30: (0, 30), 32: (0, 32), 29: (0, 41)},
  36: {27: (1, 37), 22: (1, 37), 6: (1, 37), 18: (1, 37), 9: (1, 37), 32: (1, 37), 4: (1, 37), 28: (1, 37), 2: (1, 37), 7: (1, 37), 0: (1, 37), 26: (1, 37)},
  37: {4: (1, 47), 2: (1, 47), 7: (1, 47), 6: (1, 47), 26: (1, 47)},
  38: {4: (1, 46), 2: (1, 46), 7: (1, 46), 6: (1, 46), 26: (1, 46)},
  39: {40: (0, 60)},
  40: {27: (1, 40), 22: (1, 40), 6: (1, 40), 18: (1, 40), 9: (1, 40), 32: (1, 40), 4: (1, 40), 2: (1, 40), 7: (1, 40), 0: (1, 40), 26: (1, 40)},
  41: {27: (1, 41), 22: (1, 41), 6: (1, 41), 18: (1, 41), 9: (1, 41), 32: (1, 41), 4: (1, 41), 2: (1, 41), 7: (1, 41), 0: (1, 41), 26: (1, 41)},
  42: {4: (1, 44), 2: (1, 44), 7: (1, 44), 6: (1, 44), 26: (1, 44)},
  43: {27: (1, 20), 22: (1, 20), 6: (1, 20), 18: (1, 20), 9: (1, 20), 33: (1, 20), 32: (1, 20), 34: (0, 61), 35: (1, 20), 36: (1, 20), 37: (1, 20), 4: (1, 20), 38: (1, 20), 39: (1, 20), 2: (1, 20), 7: (1, 20), 0: (1, 20), 40: (1, 20), 26: (1, 20), 41: (1, 20)},
  44: {27: (1, 22), 22: (1, 22), 6: (1, 22), 18: (1, 22), 9: (1, 22), 33: (0, 63), 32: (1, 22), 34: (1, 22), 35: (0, 62), 36: (1, 22), 37: (1, 22), 4: (1, 22), 38: (1, 22), 39: (1, 22), 2: (1, 22), 7: (1, 22), 0: (1, 22), 40: (1, 22), 26: (1, 22), 41: (1, 22)},
  45: {27: (1, 24), 22: (1, 24), 6: (1, 24), 18: (1, 24), 9: (1, 24), 33: (1, 24), 32: (1, 24), 34: (1, 24), 35: (1, 24), 36: (1, 24), 37: (1, 24), 4: (1, 24), 38: (1, 24), 39: (1, 24), 2: (1, 24), 7: (1, 24), 0: (1, 24), 40: (1, 24), 26: (1, 24), 41: (0, 64)},
  46: {27: (1, 26), 22: (1, 26), 6: (1, 26), 18: (1, 26), 9: (1, 26), 33: (1, 26), 32: (1, 26), 34: (1, 26), 35: (1, 26), 36: (0, 66), 37: (0, 67), 4: (1, 26), 38: (1, 26), 39: (0, 65), 2: (1, 26), 7: (1, 26), 0: (1, 26), 40: (1, 26), 26: (1, 26), 41: (1, 26)},
  47: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 38: (0, 52), 14: (0, 14), 16: (0, 16), 43: (0, 53), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 15: (0, 54), 23: (0, 23), 44: (0, 68), 24: (0, 24), 25: (0, 25), 26: (0, 26), 30: (0, 30), 32: (0, 32)},
  48: {4: (1, 53), 2: (1, 53), 7: (1, 53), 6: (1, 53), 26: (1, 53)},
  49: {4: (1, 52), 2: (1, 52), 7: (1, 52), 6: (1, 52), 26: (1, 52)},
  50: {4: (1, 54), 2: (1, 54), 7: (1, 54), 6: (1, 54), 26: (1, 54)},
  51: {},
  52: {27: (1, 15), 22: (1, 15), 6: (1, 15), 18: (1, 15), 9: (1, 15), 32: (1, 15), 4: (1, 15), 38: (1, 15), 2: (1, 15), 7: (1, 15), 0: (1, 15), 26: (1, 15)},
  53: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 15: (0, 69), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 14: (0, 14), 16: (0, 16), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 30: (0, 30), 32: (0, 32), 38: (0, 70)},
  54: {22: (1, 42), 6: (1, 42), 18: (1, 42), 9: (1, 42), 32: (1, 42), 4: (1, 42), 38: (1, 42), 2: (1, 42), 7: (1, 42), 26: (1, 42)},
  55: {27: (1, 19), 22: (1, 19), 6: (1, 19), 18: (1, 19), 9: (1, 19), 32: (1, 19), 4: (1, 19), 38: (1, 19), 2: (1, 19), 7: (1, 19), 0: (1, 19), 26: (1, 19)},
  56: {27: (1, 17), 22: (1, 17), 6: (1, 17), 18: (1, 17), 9: (1, 17), 33: (1, 17), 32: (1, 17), 34: (1, 17), 35: (1, 17), 36: (1, 17), 37: (1, 17), 4: (1, 17), 38: (1, 17), 39: (1, 17), 2: (1, 17), 7: (1, 17), 0: (1, 17), 40: (1, 17), 26: (1, 17), 41: (1, 17)},
  57: {1: (0, 1), 2: (0, 2), 4: (0, 4), 5: (0, 5), 6: (0, 6), 7: (0, 7), 9: (0, 9), 11: (0, 11), 10: (0, 10), 12: (0, 12), 13: (0, 13), 38: (0, 52), 14: (0, 14), 16: (0, 16), 43: (0, 53), 17: (0, 17), 18: (0, 18), 19: (0, 19), 20: (0, 20), 22: (0, 22), 15: (0, 54), 44: (0, 71), 23: (0, 23), 24: (0, 24), 25: (0, 25), 26: (0, 26), 30: (0, 30), 32: (0, 32)},
  58: {46: (0, 72)},
  59: {27: (1, 13), 22: (1, 13), 6: (1, 13), 18: (1, 13), 9: (1, 13), 32: (1, 13), 4: (1, 13), 38: (1, 13), 2: (1, 13), 7: (1, 13), 0: (1, 13), 26: (1, 13)},
  60: {27: (1, 28), 22: (1, 28), 6: (1, 28), 18: (1, 28), 9: (1, 28), 33: (1, 28), 32: (1, 28), 34: (1, 28), 35: (1, 28), 36: (1, 28), 37: (1, 28), 4: (1, 28), 38: (1, 28), 39: (1, 28), 2: (1, 28), 7: (1, 28), 0: (1, 28), 40: (1, 28), 26: (1, 28), 41: (1, 28)},
  61: {4: (1, 45), 2: (1, 45), 7: (1, 45), 6: (1, 45), 26: (1, 45)},
  62: {4: (1, 48), 2: (1, 48), 7: (1, 48), 6: (1, 48), 26: (1, 48)},
  63: {4: (1, 49), 2: (1, 49), 7: (1, 49), 6: (1, 49), 26: (1, 49)},
  64: {4: (1, 51), 2: (1, 51), 7: (1, 51), 6: (1, 51), 26: (1, 51)},
  65: {4: (1, 56), 2: (1, 56), 7: (1, 56), 6: (1, 56), 26: (1, 56)},
  66: {4: (1, 55), 2: (1, 55), 7: (1, 55), 6: (1, 55), 26: (1, 55)},
  67: {4: (1, 57), 2: (1, 57), 7: (1, 57), 6: (1, 57), 26: (1, 57)},
  68: {27: (1, 18), 22: (1, 18), 6: (1, 18), 18: (1, 18), 9: (1, 18), 32: (1, 18), 4: (1, 18), 38: (1, 18), 2: (1, 18), 7: (1, 18), 0: (1, 18), 26: (1, 18)},
  69: {22: (1, 43), 6: (1, 43), 18: (1, 43), 9: (1, 43), 32: (1, 43), 4: (1, 43), 38: (1, 43), 2: (1, 43), 7: (1, 43), 26: (1, 43)},
  70: {27: (1, 14), 22: (1, 14), 6: (1, 14), 18: (1, 14), 9: (1, 14), 32: (1, 14), 4: (1, 14), 38: (1, 14), 2: (1, 14), 7: (1, 14), 0: (1, 14), 26: (1, 14)},
  71: {27: (1, 16), 22: (1, 16), 6: (1, 16), 18: (1, 16), 9: (1, 16), 32: (1, 16), 4: (1, 16), 2: (1, 16), 7: (1, 16), 0: (1, 16), 26: (1, 16)},
  72: {45: (0, 73)},
  73: {27: (1, 5), 22: (1, 5), 6: (1, 5), 18: (1, 5), 9: (1, 5), 32: (1, 5), 4: (1, 5), 28: (1, 5), 2: (1, 5), 7: (1, 5), 0: (1, 5), 26: (1, 5), 47: (0, 74), 48: (0, 75)},
  74: {27: (1, 4), 22: (1, 4), 6: (1, 4), 18: (1, 4), 9: (1, 4), 32: (1, 4), 4: (1, 4), 28: (1, 4), 2: (1, 4), 7: (1, 4), 0: (1, 4), 26: (1, 4)},
  75: {26: (0, 76)},
  76: {27: (1, 6), 22: (1, 6), 6: (1, 6), 18: (1, 6), 9: (1, 6), 32: (1, 6), 4: (1, 6), 28: (1, 6), 2: (1, 6), 7: (1, 6), 0: (1, 6), 26: (1, 6)},
}
TOKEN_TYPES = (
{0: '$END',
 1: 'bitwise',
 2: 'NUMBER_STRING',
 3: '__anon_star_0',
 4: 'VAR',
 5: 'compare',
 6: 'LPAR',
 7: 'READ',
 8: '__anon_star_1',
 9: 'BREAK',
 10: 'product',
 11: '__anon_star_3',
 12: 'value',
 13: 'loop_call',
 14: '__anon_star_4',
 15: 'expression',
 16: '__anon_star_5',
 17: '__anon_star_6',
 18: 'IF',
 19: 'clause',
 20: 'number',
 21: 'start',
 22: 'LOOP',
 23: 'write',
 24: 'if_call',
 25: 'sum',
 26: 'IDENTIFIER',
 27: 'DEFINE',
 28: 'INCL',
 29: 'function_definition',
 30: 'function_call',
 31: 'include',
 32: 'WRITE',
 33: 'DIV',
 34: 'ADD',
 35: 'MULT',
 36: 'B_AND',
 37: 'B_XOR',
 38: 'END',
 39: 'B_OR',
 40: 'RPAR',
 41: 'GREATER',
 42: 'BASE',
 43: '__anon_star_2',
 44: 'block',
 45: '__ANON_0',
 46: 'FILE_PATH',
 47: 'include_as',
 48: 'AS'}
)
parse_table.states = {s: {TOKEN_TYPES[t]: (a, RULES[x] if a is Reduce else x) for t, (a, x) in acts.items()}
                      for s, acts in STATES.items()}
parse_table.start_state = 0
parse_table.end_state = 51

class Lark_StandAlone:
  def __init__(self, transformer=None, postlex=None):
     callback = parse_tree_builder.create_callback(transformer=transformer)
     callbacks = {rule: getattr(callback, rule.alias or rule.origin, None) for rule in RULES.values()}
     self.parser = _Parser(parse_table, callbacks)
     self.postlex = postlex
  def parse(self, stream):
     tokens = lex(stream)
     sps = CON_LEXER.set_parser_state
     if self.postlex: tokens = self.postlex.process(tokens)
     return self.parser.parse(tokens, sps)
