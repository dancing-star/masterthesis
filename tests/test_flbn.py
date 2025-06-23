from modules import *
import timeit

# Remark: Some tests related to probabilities and relative
# True groundings may no longer work, since the evaluate function
# in logic.py belonging to the Relation class was rewritten
# to no longer consult XSB modules.
# Tests will be rewritten only if necessary.

# Tests for FlbnNode:

def test_flbn_node_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a, c]))

	r = Relation('r', [X, Y])
	q = Relation('q', [X])
	p = Relation('r', [X, Y])

	r_node = FlbnNode(r, [And(r,q), Not(r)], sigmoid_product)
	q_node = FlbnNode(q)
	p_node = FlbnNode(p, [And(r,q), Not(r)], sigmoid_product)

	print('Formulas in r_node:')
	for p in r_node:
		print(p.getName())

	print('\n')
	print('r_node == q_node: (False)', r_node == q_node) # False
	print('r_node == p_node: (True)', r_node == p_node) # True
	print('\n')

	print('r_node.f(0) ==', r_node.evalF(0, 0)) # 0.25
	#print('q_node.f(0) ==', q_node.evalF()) # 0.0
	print('r_node.name ==', r_node.getName()) # r
	print('r_node.length ==', r_node.getLength()) # 2
	print(r_node.getFormulaAt(1).getName()) # !r


# Tests for FLBN Methods

def test_flbn_methods_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a, c]))

	r = Relation('r', [X, Y])
	q = Relation('q', [X, Y])
	p = Relation('p', [X])

	r_node = FlbnNode(r, [], sigmoid_product)
	q_node = FlbnNode(q, [], sigmoid_product)
	p_node = FlbnNode(p, [Not(r), q], sigmoid_product)

	G = create_FLBN({r_node, q_node})
	add_to_FLBN(G, p_node, {r_node, q_node})

	nx.draw_spring(G, with_labels=True)
	plt.show()


# Tests for probability

def test_probability_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y])
	q = Relation('q', [X, Z])
	p = Relation('p', [Y, Z])

	q_node = FlbnNode(q, [], sigmoid_product)
	p_node = FlbnNode(p, [], sigmoid_product)
	r_node = FlbnNode(r, [q, p], sigmoid_product)

	s1 = Substitution([Binding(X, a)])
	s2 = Substitution([Binding(X, a), Binding(Z, c)])
	s3 = Substitution([Binding(X, a), Binding(Y, b)])

	consult('test_probability')

	try:
		r_node.probability(s1, 'test_probability') # fails
	except IllegalArgumentError:
		print('s1 fails')

	try:
		r_node.probability(s2, 'test_probability') # fails
	except IllegalArgumentError:
		print('s2 fails')

	try:
		r_node.probability(s3, 'test_probability') # succeeds
	except IllegalArgumentError:
		print('s3 fails')

def test_probability_2():
	'''
	Correctness of this test relies on the content of
	test_probability.P

	The following settings were made, to make the tests
	work:

	r(a).
	r(b).

	q(a, a).
	q(b, a).

	p(a, b).
	p(b, b).
	'''
	a = Constant('a')
	b = Constant('b')

	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Y])

	r_node = FlbnNode(r, [q, p], sigmoid_product)

	s = Substitution([Binding(X, a)])

	consult('test_probability')

	x = r_node.probability(s, 'test_probability')
	print(x) # sigmoid(0.5) * sigmoid(0.5) ~ 0.387456...

def test_probability_3():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Y])

	r_node = FlbnNode(r, [q, p], sigmoid_product)

	s = Substitution([Binding(X, a)])

	consult('test_probability_2')

	x = []
	x.append(r_node.probability(s, 'test_probability_2', [False, False, False]))
	x.append(r_node.probability(s, 'test_probability_2', [False, False, True]))
	x.append(r_node.probability(s, 'test_probability_2', [False, True, False]))
	x.append(r_node.probability(s, 'test_probability_2', [False, True, True]))
	x.append(r_node.probability(s, 'test_probability_2', [True, False, False]))
	x.append(r_node.probability(s, 'test_probability_2', [True, False, True]))
	x.append(r_node.probability(s, 'test_probability_2', [True, True, False]))
	x.append(r_node.probability(s, 'test_probability_2', [True, True, True]))
	print(x) # [0.66, 0.62, 0.62, 0.56, 0.34, 0.38, 0.38, 0.44] (Calculated with WolframAlpha and rounded to 2 significant digits)

# Tests for C-FOVE implementation for FLBNs

def test_node_to_parfactor_1():
	# Syntactic test
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X])
	q = Relation('q', [X, Y])
	p = Relation('p', [X, Y])

	p_node = FlbnNode(p, [], sigmoid_product)
	q_node = FlbnNode(q, [], sigmoid_product)
	r_node = FlbnNode(r, [p, q], sigmoid_product)

	G = create_FLBN([q_node, p_node])
	add_to_FLBN(G, r_node, [q_node, p_node])

	pf = node_to_parfactor(G, r_node)

	print(pf)

def test_node_to_parfactor_2():
	a = Constant('a')
	b = Constant('b')

	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, Y])
	q = Relation('q', [X])

	q_node = FlbnNode(q, [r], (lambda x : x[0]))
	r_node = FlbnNode(r, [], (lambda x : 1.0))

	G = create_FLBN([r_node])
	add_to_FLBN(G, q_node, [r_node])

	pf = node_to_parfactor(G, q_node)

	print(pf) # 1, 0.5, 0.5, 0, 0, 0.5, 0.5, 1


# Tests for truth tables

def test_generate_truth_table_1():
	n = 3
	truth_table = generate_truth_table(n)
	print(truth_table)

	print('\n')

	n = 4
	truth_table = generate_truth_table(n)
	print(truth_table)


# Tests for query:

def test_get_parfactors_1():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])
	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r1 = Relation('r1', [X, Y, Z])
	r2 = Relation('r2', [X, Y, Z])
	r3 = Relation('r3', [X, Y, Z])
	r4 = Relation('r4', [X, Y, Z])
	r5 = Relation('r5', [X, Y, Z])
	r6 = Relation('r6', [X, Y])
	r7 = Relation('r7', [X, Y])
	r8 = Relation('r8', [X])
	r9 = Relation('r9', [])

	v1 = FlbnNode(r1, [], product)
	v2 = FlbnNode(r2, [], product)
	v3 = FlbnNode(r3, [], product)
	v4 = FlbnNode(r4, [], product)
	v5 = FlbnNode(r5, [], product)
	v6 = FlbnNode(r6, [r1, r2], product)
	v7 = FlbnNode(r7, [r3, r4], product)
	v8 = FlbnNode(r8, [r6, r7], product)
	v9 = FlbnNode(r9, [r8, r5], product)

	G = create_FLBN([v1, v2, v3, v4, v5])
	add_to_FLBN(G, v6, [v1, v2])
	add_to_FLBN(G, v7, [v3, v4])
	add_to_FLBN(G, v8, [v6, v7])
	add_to_FLBN(G, v9, [v8, v5])

	parfactors = get_parfactors(G, v8)
	for p in parfactors:
		print(p) # parfactors for v1, v2, v3, v4, v6, v7, v8
		print('\n---------------\n')

def test_query_1():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])
	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r1 = Relation('r1', [X, Y, Z])
	r2 = Relation('r2', [X, Y, Z])
	r3 = Relation('r3', [X, Y, Z])
	r4 = Relation('r4', [X, Y, Z])
	r5 = Relation('r5', [X, Y, Z])
	r6 = Relation('r6', [X, Y])
	r7 = Relation('r7', [X, Y])
	r8 = Relation('r8', [X])
	r9 = Relation('r9', [])

	v1 = FlbnNode(r1, [], product)
	v2 = FlbnNode(r2, [], product)
	v3 = FlbnNode(r3, [], product)
	v4 = FlbnNode(r4, [], product)
	v5 = FlbnNode(r5, [], product)
	v6 = FlbnNode(r6, [r1, r2], product)
	v7 = FlbnNode(r7, [r3, r4], product)
	v8 = FlbnNode(r8, [r6, r7], product)
	v9 = FlbnNode(r9, [r8, r5], product)

	G = create_FLBN([v1, v2, v3, v4, v5])
	add_to_FLBN(G, v6, [v1, v2])
	add_to_FLBN(G, v7, [v3, v4])
	add_to_FLBN(G, v8, [v6, v7])
	add_to_FLBN(G, v9, [v8, v5])

	p = query(G, v8)
	print('\n')
	print(p) # r8
			 # 0.0
			 # 1.0

def test_query_2(n):
	p = []
	for i in range(n):
		c = Constant('c' + str(i))
		p.append(c)
	pop = Population(p)

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r1 = Relation('r1', [X, Y, Z])
	r2 = Relation('r2', [X, Y, Z])
	r3 = Relation('r3', [X, Y, Z])
	r4 = Relation('r4', [X, Y, Z])
	r5 = Relation('r5', [X, Y, Z])
	r6 = Relation('r6', [X, Y])
	r7 = Relation('r7', [X, Y])
	r8 = Relation('r8', [X])
	r9 = Relation('r9', [])

	v1 = FlbnNode(r1, [], product)
	v2 = FlbnNode(r2, [], product)
	v3 = FlbnNode(r3, [], product)
	v4 = FlbnNode(r4, [], product)
	v5 = FlbnNode(r5, [], product)
	v6 = FlbnNode(r6, [r1, r2], product)
	v7 = FlbnNode(r7, [r3, r4], product)
	v8 = FlbnNode(r8, [r6, r7], product)
	v9 = FlbnNode(r9, [r8, r5], product)

	G = create_FLBN([v1, v2, v3, v4, v5])
	add_to_FLBN(G, v6, [v1, v2])
	add_to_FLBN(G, v7, [v3, v4])
	add_to_FLBN(G, v8, [v6, v7])
	add_to_FLBN(G, v9, [v8, v5])

	p = query(G, v8)
	print('\n')
	print(p) # r8
			 # 0.0
			 # 1.0

def test_timeit_query_2(nint):
	t = timeit.timeit("test_query_2({})".format(nint), "from __main__ import test_query_2", number=1)
	print(t)
