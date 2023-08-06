from standalone import Lark_StandAlone as Parser
from basenum import _str_to_base_num as toInt
import sys
import re

class Error(Exception):
	pass

class RecursionError(Error):
	#for when a user tries to build recursive functions. NOT ALLOWED! why? dunno. Though it does keep the call stack shorter by forcing you to use loops instead. So maybe that's why.
	pass

class ArgumentError(Error):
	#for when command line arguments are invalid - such as when a filename is not supplied, or it's malformed
	pass

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