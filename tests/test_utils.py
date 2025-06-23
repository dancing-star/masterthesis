from modules import *

# Tests for product:

def test_product_1():
	arg1 = []
	arg2 = [1, 2, 3]
	arg3 = [0.5, 0.5, 0.25]
	arg4 = [D('1'), D('0.5'), D('4.0'), D('0.01')]
	print(product(arg1)) # 1
	print(product(arg2)) # 6
	print(product(arg3)) # 0.0625
	print(product(arg4)) # 0.02

# Tests for sigmoid function:

def test_sigmoid_1():
	print(sigmoid(0)) # 0.5
	print(sigmoid(1)) # 1/(1+e^(-1))
	print(sigmoid(float('inf'))) # 1.0
	print(sigmoid(-float('inf'))) # 0.0


# Tests for sigmoid_product:

def test_sigmoid_product_1():
	print(sigmoid_product(0, 0, 0, 0)) # 1/16 == 0.0625
	print(sigmoid_product(float('inf'), float('inf'), float('inf'))) # 1.0


# Tests for Lists:

def test_lists_1():
	list1 = [1,2,3]
	list2 = [4,5,6]
	l = Lists.union(list1, list2)
	print(l) # [1, 2, 3, 4, 5, 6]

	list3 = [1,2,3,4]
	list4 = [6,2,4,7]
	l = Lists.union(list3, list4)
	print(l) # [1, 2, 3, 4, 6, 7]

def test_lists_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')
	d = Constant('d')
	l1 = [a, a, b, d]
	l2 = [b, c]
	
	for t in l1:
		print(t.getName()) # a, a, b, d
	print('\n')

	l = Lists.difference(l1, l2)
	for t in l:
		print(t.getName()) # a, d
	print('\n')

	m = Lists.difference(l1, [])
	for t in m:
		print(t.getName()) # a, b, d
	print('\n')

def test_lists_3():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')
	d = Constant('d')
	e = Constant('e')

	l1 = [a, b, c, d, b, d]
	l2 = [d, b, e, e, a]

	l = Lists.intersection(l1, l2)
	for t in l:
		print(t.getName()) # a, b, d


# Tests for Sets:

def test_sets_union_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('a')

	union = Sets.union({a, b}, {a, b, c})

	for t in union:
		print(t.getName()) # a, b

def test_sets_difference():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')
	d = Constant('a')

	set1 = Sets.difference({a, b}, {a})
	set2 = Sets.difference({a, d}, {a})
	set3 = Sets.difference({b, c, d}, {a})
	set4 = Sets.difference({a, b, c, d}, {a})

	for t in set1: # b
		print(t.getName())
	print('---\n')

	for t in set2: # nothing
		print(t.getName())
	print('---\n')

	for t in set3: 
		print(t.getName()) # b, c
	print('---\n')

	for t in set4:
		print(t.getName()) # b, c
	print('---')


# Tests for MathUtils:

def test_combination_1():
	try:
		print(MathUtils.combination(-1, 1)) # fails
	except IllegalArgumentError:
		print('This fails.')
	try:
		print(MathUtils.combination(1, -1)) # fails
	except IllegalArgumentError:
		print('This fails.')
	print(MathUtils.combination(10, 2)) # 45
	print(MathUtils.combination(10, 10)) # 1
	print(MathUtils.combination(0, 1)) # 0
	print(MathUtils.combination(10, 0)) # 1
	print(MathUtils.combination(5, 10)) # 0

# Tests by takiyama

def test_multinomial_empty():
	m = []
	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = D('1')

	print(result == answer) # True

def test_multinomial_0():
	m = [0]
	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = 1

	return result == answer # True

def test_multinomial_1():
	m = [1]
	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = 1

	return result == answer # True

def test_multinomial_1_1():
	m = [1, 1]

	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = 2

	return result == answer # TODO: I think this was supposed to be true -> check

def test_multinomial_1_1_1():
	m = [1, 1, 1]
	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = 6

	return result == answer # True

def test_multinomial_3_2():
	m = [3, 2]

	mul = Multinomial(m)

	result = MathUtils.multinomial(mul)
	answer = 10

	return result == answer # True

def test_pow_0_0():
	base = D('0')
	p = 0
	q = 1

	result = MathUtils.mathUtilsPow(base, p, q)
	answer = D('1')

	return result == answer # True

def test_pow_0_positive_number():
	base = D('0')
	p = 3
	q = 1

	result = MathUtils.mathUtilsPow(base, p, q)
	answer = D('0')

	print(result == answer) # True

def test_pow_0_negative_number():
	base = D('0')
	p = -3
	q = 1

	MathUtils.mathUtilsPow(base, p, q) # fails

def test_pow_minus_2_3():
	base = D('-2')
	p = 3
	q = 1

	# According to takiyama, this next operation should fail
	# However it does not!
	# Looking at the implementation this makes perfect sense,
	# as p % q == 0. The port seems to be semantically correct.
	# I cannot find the error. It may be on takiyamas end.
	# Nevertheless, the result -8 is correct.
	result = MathUtils.mathUtilsPow(base, p, q) # fails
	print(result)

def test_pow_2_2():
	base = D('2')
	p = 4
	q = 2

	result = MathUtils.mathUtilsPow(base, p, q)
	answer = D('4')

	print(result == answer) # True

def test_sqrt_4():
	base = D('4')
	p = 1
	q = 2

	result = MathUtils.mathUtilsPow(base, p, q)
	answer = D('2')

	print(result == answer) # True

# not by takiyama

def test_pow_negative_float():
	base = D('-2')
	p = 1
	q = 2

	result = MathUtils.mathUtilsPow(base, p, q) # fails