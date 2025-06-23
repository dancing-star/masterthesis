from modules import *
import timeit
# Remark: Some tests related to probabilities and relative
# True groundings may no longer work, since the evaluate function
# in logic.py belonging to the Relation class was rewritten
# to no longer consult XSB modules.
# Tests will be rewritten only if necessary.

# tests for Groundings

def test_groundings_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a]))
	Y = Variable('Y', Population([a, b]))

	r = Relation('r', [X, Y])

	i = 1
	for bindings in Groundings(r): # 1: [X, a]; 1: [Y, a]; 2: [X, a]; 2: [Y, b]
		for binding in bindings:
			print(i, ': [', binding.getFirstTerm().getName(), ',', binding.getSecondTerm().getName(), ']')
		i += 1


# tests for parametrizedFlbnNode

def test_parametrized_flbn_node_1():
	# Test deprecated, as it uses a normal list
	# rather than a torch.tensor.
	# Should still work though.
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y])
	q = Relation('q', [X, Y, Z])
	p = Relation('p', [X, Y, Z])

	try:
		r_node = ParametrizedFlbnNode(r, [q, p], [0.1, 0.2]) # fails
	except IllegalArgumentError:
		print('Parameter-Liste zu kurz')

	try:
		r_node = ParametrizedFlbnNode(r, [q, p], [0.5, 0.25, 0.25]) # succeeds
	except IllegalArgumentError:
		print('Parameter-Liste zu kurz')

	print(r_node._f([-1, -1])) # sigmoid(0) = 0.5
	print('\n')

	print(r_node.getParameters()) # 0.5, 0.25, 0.25
	print(r_node.getParameterAt(1)) # 0.25
	print('\n')

	r_node.updateParameters([0.1, 0.1, 0.1])
	r_node.setParameterAt(1, 0.3)

	print(r_node.getParameters()) # 0.1, 0.3, 0.1
	print(r_node.getParameterAt(1)) # 0.3


# Tests for gradient descent related methods

def test_probability_4():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Y])

	module = 'test_probability'

	r_node = ParametrizedFlbnNode(r, [q, p], [0.5, 0.5, 0.5])
	s = Substitution([Binding(X, a)])

	consult('test_probability')

	x = r_node.probability(s, 'test_probability')
	print(x) # sigmoid(0.5 + 0.5 * 1/3 + 0.5 * 1/3) = 0.6970593...


# tests for distribution

# So far the following two tests are only syntactiacally.
# Will test semantics, when I get px properly working.

# TODO: Make sure these methods are SEMANTICALLY correct!

def test_distribution_1():
	test_file = 'test_distribution_1'
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Z])

	w_r = initialize_weights(3)
	#w_q = initialize_weigts(2)
	#w_p = initialize_weigts(2)

	r_node = ParametrizedFlbnNode(r, [q, p], w_r)
	#q_node = ParametrizedFlbnNode(q, [], w_q)

	d = rbn_distribution(test_file, [r_node], r_node._parameters)
	print(d)
	# We get 0.0538

def test_likelihood_1():
	test_file_1 = 'test_likelihood_1_1'
	test_file_2 = 'test_likelihood_1_2'
	test_file_3 = 'test_likelihood_1_3'
	tests = [test_file_1, test_file_2, test_file_3]

	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Z])

	w_r = initialize_weights(3)
	r_node = ParametrizedFlbnNode(r, [q, p], w_r)

	L = likelihood(tests, [r_node], r_node._parameters)
	print(L)
	# We get 0.0023

def test_likelihood_2():
	test_file_1 = 'test_likelihood_2_1'
	test_file_2 = 'test_likelihood_2_2'
	test_file_3 = 'test_likelihood_2_3'
	tests = [test_file_1, test_file_2, test_file_3]

	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Z])

	f = Relation('f', [X, Y])
	g = Relation('g', [X])

	w_r = initialize_weights(3)
	w = initialize_weights(9)

	r_node = ParametrizedFlbnNode(r, [q, p], w_r)
	f_node = ParametrizedFlbnNode(f, [q, p], w_r)
	g_node = ParametrizedFlbnNode(g, [q, p], w_r)

	L = likelihood(tests, [r_node, f_node, g_node], w)
	print(L)
	# We get 2.5790e-18

def test_gradient_descent_1():
	# Note: This is just a syntactic test.
	# It does not test, if the gradient descend works
	# correctly or 'makes sense'.
	test_file_1 = 'test_likelihood_2_1'
	test_file_2 = 'test_likelihood_2_2'
	test_file_3 = 'test_likelihood_2_3'
	tests = [test_file_1, test_file_2, test_file_3]

	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Z])

	f = Relation('f', [X, Y])
	g = Relation('g', [X])

	w_r = initialize_weights(3)

	r_node = ParametrizedFlbnNode(r, [q, p], w_r)
	f_node = ParametrizedFlbnNode(f, [q, p], w_r)
	g_node = ParametrizedFlbnNode(g, [q, p], w_r)

	gradient_descent(tests, [r_node, f_node, g_node], threshold=0.0001, n_iters=1000)

	print(r_node.getParameters())
	print(f_node.getParameters())
	print(g_node.getParameters())

def test_gradient_descent_2():
	# Requires simple_test.P
	# in the same folder!
	test_file = 'simple_test'
	consult(test_file)

	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)

	r = Relation('r', [X])
	w = initialize_weights(1)
	r_node = ParametrizedFlbnNode(r, [], w)

	p = r_node.probability(Substitution([Binding(X, a)]), test_file)
	print('\n')
	print('probability: ', p) # ~ 0.622

	d = rbn_distribution(test_file, [r_node], w)
	print('\n')
	print('distribution: ', d) # sigmoid(1/2)*(1-sigmoid(1/2))^2 ~ 0.089

	l = l = -torch.log(likelihood([test_file], [r_node], w))
	print('\n')
	print('likelihood: ', l) # -log(sigmoid(1/2)*(1-sigmoid(1/2))^2) ~ 2.422

	gradient_descent([test_file], [r_node])
	print('\n')
	print('learning result: ', r_node._parameters) # ln(1/2) ~ -0.69

def test_gradient_descent_3(n, lr=0.01, th=0.0000000001):
	test_file = 'test_learning_3'

	p = []
	for i in range(n):
		p.append(Constant('a' + str(i+1)))
	pop = Population(p)

	X = Variable('X', pop)

	r = Relation('r', [X])
	w = initialize_weights(1)
	r_node = ParametrizedFlbnNode(r, [], w)

	gradient_descent([test_file], [r_node], lr=lr, threshold=th)
	print('\n')
	print('learning result: ', r_node._parameters)

def test_gradient_descent_4(n, lr=0.01, th=0.00001):
	test_file = 'test_learning_4'

	p1 = []
	for i in range(n):
		p1.append(Constant('a' + str(i+1)))
	pop1 = Population(p1)

	p2 = []
	for i in range(n):
		p2.append(Constant('b' + str(i+1)))
	pop2 = Population(p2)

	X = Variable('X', pop1)
	Y = Variable('Y', pop2)

	r = Relation('r', [X, Y])
	q = Relation('q', [X])

	w = initialize_weights(1)
	u = initialize_weights(2)

	r_node = ParametrizedFlbnNode(r, [], w)
	q_node = ParametrizedFlbnNode(q, [r], u)

	gradient_descent([test_file], [r_node, q_node], lr=lr, threshold=th)
	print('\n')
	print('learning result r: ', r_node._parameters)
	print('learning result q: ', q_node._parameters)

def test_gradient_descent_5(n, lr=0.01, th=0.00001):
	test_file = 'test_learning_5'

	p1 = []
	for i in range(n):
		p1.append(Constant('a' + str(i+1)))
	pop1 = Population(p1)

	p2 = []
	for i in range(n):
		p2.append(Constant('b' + str(i+1)))
	pop2 = Population(p2)

	p3 = []
	for i in range(n):
		p3.append(Constant('c' + str(i+1)))
	pop3 = Population(p3)

	X = Variable('X', pop1)
	Y = Variable('Y', pop2)
	Z = Variable('Z', pop3)

	r = Relation('r', [X, Y, Z])
	q = Relation('q', [X, Y, Z])
	p = Relation('p', [X, Y])

	w1 = initialize_weights(1)
	w2 = initialize_weights(1)
	u = initialize_weights(3)

	r_node = ParametrizedFlbnNode(r, [], w1)
	q_node = ParametrizedFlbnNode(q, [], w2)
	p_node = ParametrizedFlbnNode(p, [r, q], u)

	gradient_descent([test_file], [r_node, q_node, p_node], lr=lr, threshold=th)
	print('\n')
	print('learning result r: ', r_node._parameters)
	print('learning result q: ', q_node._parameters)
	print('learning result p: ', p_node._parameters)

def test_timeit_gradient_descend_3(nint):
	t = timeit.timeit("test_gradient_descent_3({})".format(nint), "from __main__ import test_gradient_descent_3", number=1)
	print(t)

def test_timeit_gradient_descend_4(nint):
	t = timeit.timeit("test_gradient_descent_4({})".format(nint), "from __main__ import test_gradient_descent_4", number=1)
	print(t)

def test_timeit_gradient_descend_5(nint):
	t = timeit.timeit("test_gradient_descent_5({})".format(nint), "from __main__ import test_gradient_descent_5", number=1)
	print(t)