import math

#TODO - make these also work for negative and fractional bases!

def from_basenum(numstr, *args):
	if args:
		n = numstr
		b = args[0]
	else:
		n = numstr
		b = 10
	
	if "_" in numstr:
		n, b = numstr.split("_")
		b = int(b)
	
	return _str_to_base_num(n, b)

def to_basenum(num, *args):
	if args:
		base = args[0]
	else:
		base = 10
	return _num_to_base(num, base) + "_" + str(base)

def _str_to_base_num(numstr, base, alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
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

def _num_to_base(num, base, alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
	a_len = len(alphabet)
	width = 1
	while ((a_len ** width) < base):
		width += 1
	
	res = ''
	
	while (num > 0):
		cur = num % base
		num //= base
		
		for i in range(width):
			res = alphabet[cur % a_len] + res
			cur //= a_len
	
	return res