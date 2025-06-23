from modules import *
# Remark: Some tests related to probabilities and relative
# True groundings may no longer work, since the evaluate function
# in logic.py belonging to the Relation class was rewritten
# to no longer consult XSB modules.
# Tests will be rewritten only if necessary.

# Tests for Term
# While there shouldn't be an instance of Term,
# we'll test it anyway.

def test_term_1():
	T = Term('T')
	S = Term('T')
	U = Term('U')
	s = 'T'
	print('T == S: (True)', T == S) # True
	print('T == U: (False)', T == U) # False
	print('T == s: (False)', T == s) # False

def test_term_2():
	c = Constant('c')
	X = Variable('X', {c})

	print(c.isConstant()) # True
	print(c.isVariable()) # False
	print(X.isConstant()) # False
	print(X.isVariable()) # True


# Tests for Constant

def test_constant_1():
	print('Try to Create upper case constant (should not work):')
	try:
		C = Constant('C') # Fails
	except IllegalArgumentError:
		print('Constant C could not be created.')

	print('Try to Create lower case constant (should work):')
	try:
		c = Constant('c') # Succeeds
	except IllegalArgumentError:
		print('Constant C could not be created.')

	a = Constant('a')
	b = Constant('c')
	t = Term('c')
	print('c == a (False)', c == a) # False
	print('c == b (True)', c == b) # True
	print('c == t (False)', c == t) # False

	print(a, b, c) # a, c, c

	s = {a, b, c}
	for u in s:
		print(u) # a, c

	l1 = [a, b]
	l2 = [a, c]
	l3 = [a, t]
	print(l1 == l2) # True
	print(l1 == l3) # False
	print(l2.index(b)) # 1


# Tests for Population

def test_population_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	p1 = Population()
	p2 = Population([a, b, c])
	p3 = Population([a, b, c, c, b, a])
	p4 = Population([a, b])

	print(p2 == p3) # True

	print('\n')
	for p in p1:
		print(p.getName()) # nothing

	print('\n')
	for p in p2:
		print(p.getName()) # a, b, c

	print('\n')
	for p in p3:
		print(p.getName()) # a, b, c

	print('\n')
	print(p1.getSize()) # 0
	print(p2.getSize()) # 3
	print(p3.getSize()) # 3
	print(p2.containsIndividual(a)) # True
	print(p4.containsIndividual(c)) # False

	p2.remove(b)
	print('\n')
	for p in p2:
		print(p.getName()) # a, c

	print('\n')
	print(p2 == p3) # False

# Tests for Variable

def test_variable_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('b')
	domain1 = Population([a, b])
	domain2 = Population([a, c])
	domain3 = Population([a])

	print('Try to Create lower case Variable (should not work):')
	try:
		x = Variable('x', domain1) # Fails
	except IllegalArgumentError:
		print('Constant C could not be created.')

	print('Try to Create upper case Variable (should work):')
	try:
		X = Variable('X', domain1) # Succeeds
	except IllegalArgumentError:
		print('Constant C could not be created.')

	print('\n')
	print('Domain of X:') # a, b
	for t in X.getPopulation():
		print(t.getName())
	print('\n')

	Y = Variable('Y', domain1)
	Z = Variable('X', domain1)
	U = Variable('X', domain2)
	V = Variable('X', domain3) # This should not happen, but we'll test it anyway

	print('X == Y: (False)', X == Y) # False
	print('X == Z: (True)', X == Z) # True
	print('X == U: (True)', X == U) # True
	print('X == V: (True)', X == V) # True
	print('X == a: (False)', X == a) # False


# Tests for Relation

def test_relation_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([b, c]))
	Z = Variable('Z', Population([a, c]))

	r = Relation('r', [X, a, b])
	q = Relation('q', [Y, Z])

	for x in r.getCodomain():
		print(x.getValue()) # False, True

	for t in r.getParameters(): # X
		print(t.getName())

	p = And(r, Not(q))
	for t in p.getParameters():
		print(t.getName()) # X, Y, Z

def test_relation_2():
	print('Try to Create upper case Relation (should not work):')
	try:
		R = Relaltion('R') # fails
	except:
		print('Relation R could not be created.')

	print('Try to Create lower case Relation (should work):')
	try:
		r = Relation('r') # succeeds
	except:
		print('Relation R could not be created.')

	a = Constant('a')
	b = Constant('b')
	c = Constant('b')

	domain1 = Population([a, b])
	domain2 = Population([a, c])
	domain3 = Population([a])

	X = Variable('X', domain1)
	Y = Variable('Y', domain1)
	Z = Variable('X', domain2) # == X
	W = Variable('X', domain3) # should not happen

	r = Relation('r', [X, Y, b])
	q = Relation('q', [X, Y, b])
	p = Relation('r', [Z, Y, b])
	s = Relation('r', [X, Y, c])

	print('\n')
	print('r == q: (False)', r == q) # False
	print('r == p: (True)', r == p) # True
	print('r == s: (True)', r == s) # True
	print('\n')

	print('Terms:')
	for t in r:
		print(t.getName()) # X, Y, b


# Test for Not:

def test_not_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a]))

	r = Relation('r', [X, a])
	q = Relation('q', [X])
	p = Relation('r', [X, a])

	not_r = Not(r)
	not_q = Not(q)
	not_p = Not(p)

	print(not_r.getName()) # !r

	print('\n')
	print('nor_r == not_q: (False)', not_r == not_q) # False
	print('nor_r == not_p: (True)', not_r == not_p) # True


# Tests for Or:

def test_or_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a]))

	r = Relation('r', [X,Y])
	q = Relation('q', [X])
	p = Relation('q', [X])

	r_or_q = Or(r, q)
	r_or_p = Or(r, p)
	q_or_r = Or(q, r)

	print(r_or_q.getName())

	print('\n')
	print('r or q == r or p: (True)', r_or_q == r_or_p) # True
	print('r or q == q or r: (False)', r_or_q == q_or_r) # False


# Tests for And:

def test_and_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a]))

	r = Relation('r', [X,Y])
	q = Relation('q', [X])
	p = Relation('q', [X])

	r_or_q = And(r, q)
	r_or_p = And(r, p)
	q_or_r = And(q, r)

	print(r_or_q.getName())

	print('\n')
	print('r or q == r or p: (True)', r_or_q == r_or_p) # True
	print('r or q == q or r: (False)', r_or_q == q_or_r) # False


# Tests for Implies:

def test_implies_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a]))

	r = Relation('r', [X,Y])
	q = Relation('q', [X])
	p = Relation('q', [X])

	r_or_q = Implies(r, q)
	r_or_p = Implies(r, p)
	q_or_r = Implies(q, r)

	print(r_or_q.getName())

	print('\n')
	print('r or q == r or p: (True)', r_or_q == r_or_p) # True
	print('r or q == q or r: (False)', r_or_q == q_or_r) # False


# Tests for Binding

def test_binding_1():
	a = Constant('a')
	b = Constant('b')

	X = Variable('X', Population([a, b]))
	Y = Variable('Y', Population([a, b]))
	Z = Variable('Z', Population([a]))

	s = Binding(X, a)
	t = Binding(Z, b)
	u = Binding(X, Y)
	v = Binding(X, Z)
	w = Binding(X, a)

	print(s.getFirstTerm().getName()) # X
	print(s.getSecondTerm().getName()) # a
	print(s.containsTerm(X)) # True
	print(s.containsTerm(Y)) # False

	print('\n')
	print(s.isValid()) # True
	print(t.isValid()) # False
	print(u.isValid()) # True
	print(v.isValid()) # False

	print('\n')
	print(s == t) # False
	print(s == w) # True


# Tests for Substitution

def test_substitution_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	population = Population([a, b, c])

	X = Variable('X', population)
	Y = Variable('Y', population)
	Z = Variable('Z', population)
	W = Variable('W', population)

	binding1 = Binding(X, a)
	binding2 = Binding(Y, Z)
	binding3 = Binding(Z, b)
	binding4 = Binding(W, X)

	s = Substitution([binding1, binding2, binding3])
	for key in s:
		print(key.getName()) # X, Y, Z

	print('\n')
	print(isinstance(s.getVariables(), set)) # True
	for key in s.getVariables():
		print(key.getName()) # X, Y, Z
	
	print('\n')
	print(s.getReplacement(X).getName()) # a
	print(s.getReplacement(Y).getName()) # Z

	print('\n')
	print(s.containsBinding(binding1)) # True
	print(s.containsBinding(binding4)) # False
	print('\n')
	print(s.containsVariable(X)) # True
	print(s.containsVariable(W)) # False
	print('\n')
	print(s.hasTerm(a)) # True
	print(s.hasTerm(X)) # True
	print(s.hasTerm(c)) # False
	print(s.hasTerm(W)) # False

	binding5 = Binding(Y, a)
	binding6 = Binding(Z, b)

	t = Substitution([binding1, binding5, binding6])
	u = Substitution()

	print('\n')
	print(t.hasCommonReplacement(X, Y)) # True
	print(t.hasCommonReplacement(X, Z)) # False
	print('\n')
	print(t.isEmpty()) # False
	print(u.isEmpty()) # True
	print('\n')
	print(t.getSize()) # 3
	print(u.getSize()) # 0
	print('\n')
	print(isinstance(t.asList(), list)) # True
	for binding in t.asList():
		print(binding.getFirstTerm().getName()) # X, Y, Z
	print('\n')
	try:
		print(u.getFirstBinding().getFirstTerm().getName()) # fails
	except ValueError:
		print('Das schlug fehl!')
	print(t.getFirstBinding().getFirstTerm().getName()) # X

	v = Substitution([binding1, binding2, binding3])

	print('\n')
	print(s == t) # False
	print(s == u) # False
	print(s == v) # True

def test_substitution_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	population = Population([a, b, c])

	X = Variable('X', population)
	Y = Variable('Y', population)
	Z = Variable('Z', population)

	r = Relation('r', [X, Y])
	q = Relation('q', [Y, Z])

	r_or_q = Or(r, q)

	s = Substitution([Binding(X, a), Binding(Z, c)])

	for t in r_or_q.getTerms():
		print(t.getName()) # X, Y, Y, Z

	substituted = r_or_q.applySubstitution(s)

	print('\n')
	for t in substituted.getTerms():
		print(t.getName()) # a, Y, Y, c
	
	p1 = Relation('p1', [X, Z])
	p2 = Relation('p1', [X, Y])
	t = Substitution([Binding(X, a), Binding(Y, c), Binding(Z, c)])
	print('\n')
	print(t.isUnifier(p1, p2)) # True
	p1 = Relation('p1', [X, Z])
	p2 = Relation('p1', [X, Y])
	t = Substitution([Binding(X, a), Binding(Y, b), Binding(Z, c)])
	print(t.isUnifier(p1, p2)) # False

def test_substitution_3():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	population = Population([a, b, c])

	X = Variable('X', population)
	Y = Variable('Y', population)

	s = Substitution([Binding(X, a)])

	r = Relation('r', [X, Y])
	p = r.applySubstitution(s)

	for t in r.getTerms():
		print(t.getName())
	print('\n') # X, Y

	for t in p.getTerms():
		print(t.getName()) # a, Y

# next test is taken from takiyama

def test_substitution_4():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)
	A = Variable('A', pop)
	B = Variable('B', pop)

	x1 = Constant('x1')
	x2 = Constant('x2')

	no_constraint = set()
	constraint_A_x1 = {InequalityConstraint(A, x1)}
	constraint_A_B = {InequalityConstraint(A, B)}

	A_x1 = Binding(A, x1)
	A_x2 = Binding(A, x2)
	A_B = Binding(A, B)
	B_x1 = Binding(B, x1)
	B_x2 = Binding(B, x2)
	B_A = Binding(B, A)

	print('True:', Substitution().isConsistentWithConstraints(no_constraint)) # True
	print('True:', Substitution([A_x1]).isConsistentWithConstraints(no_constraint)) # True
	print('True:', Substitution([A_B]).isConsistentWithConstraints(no_constraint)) # True
	print('False:', Substitution([A_x1]).isConsistentWithConstraints(constraint_A_x1)) # False
	print('True:', Substitution([A_x2]).isConsistentWithConstraints(constraint_A_x1)) # True
	print('True:', Substitution().isConsistentWithConstraints(constraint_A_x1)) # True
	print('False:', Substitution([A_B]).isConsistentWithConstraints(constraint_A_B)) # False
	print('False:', Substitution([A_x1, B_x1]).isConsistentWithConstraints(constraint_A_B)) # False
	print('False:', Substitution([B_A]).isConsistentWithConstraints(constraint_A_B)) # False
	print('True:', Substitution().isConsistentWithConstraints(constraint_A_B)) # True
	print('True:', Substitution([A_x1]).isConsistentWithConstraints(constraint_A_B)) # True
	print('True:', Substitution([B_x1]).isConsistentWithConstraints(constraint_A_B)) # True
	print('True:', Substitution([A_x1, B_x2]).isConsistentWithConstraints(constraint_A_B)) # True


# Tests for InequalityConstraint

# Tests taken from Takiyama

def test_inequality_constraint_1():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	q = X.getPopulation().getIndividualAt(0)

	c = InequalityConstraint(X, Y)
	b = Binding(X, q)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_2():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	q = X.getPopulation().getIndividualAt(0)

	c = InequalityConstraint(X, Y)
	b = Binding(Y, q)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_3():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	W = Variable('W', Population(population))

	c = InequalityConstraint(X, Y)
	b = Binding(X, W)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_4():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	W = Variable('W', Population(population))

	c = InequalityConstraint(X, Y)
	b = Binding(Y, W)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_5():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	t = Constant('x1')
	q = Constant('x1')

	c = InequalityConstraint(X, t)
	b = Binding(Y, q)

	print(c.isConsistentWithBinding(b)) # True

def test_inequality_constraint_6():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	Y = Variable('Y', Population(population))
	W = Variable('W', Population(population))
	t = Constant('x1')

	c = InequalityConstraint(X, t)
	b = Binding(Y, W)

	print(c.isConsistentWithBinding(b)) # True

def test_inequality_constraint_7():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	W = Variable('W', Population(population))
	t = Constant('x1')

	c = InequalityConstraint(X, t)
	b = Binding(X, W)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_8():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	t = Constant('x1')
	q = Constant('x1')

	c = InequalityConstraint(X, t)
	b = Binding(X, q)

	print(c.isConsistentWithBinding(b)) # False

def test_inequality_constraint_9():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	X = Variable('X', Population(population))
	t = Constant('x1')
	q = Constant('x2')

	c = InequalityConstraint(X, t)
	b = Binding(X, q)

	print(c.isConsistentWithBinding(b)) # True


# Tests for px:

def test_px_1():
	'''
	Correctness of this test relies on the content of
	test.P

	It is assumed that test.P is never changed, since
	it's for testing, so I won't repeat its contents here.
	'''
	consult('test')
	print(px_comp('usermod', 'r', 'a', 'b', 'c', vars=0)) # not empty
	print(px_comp('usermod', 'r', 'a', 'b', 'b', vars=0)) # empty

	print(not not px_comp('usermod', 'r', 'a', 'b', 'c', vars=0)) # True
	print(not not px_comp('usermod', 'r', 'a', 'b', 'b', vars=0)) # False


# Tests for evaluate

def test_evaluate_1():
	'''
	Correctness of this test relies on the content of
	test_evaluate_1.P

	The following settings were made, to make the tests
	work:

	r(a, b, c).
	r(a, c, b).
	r(b, a, c).
	r(b, c, a).
	r(c, a, b).
	r(c, b, c).

	q(a, b).
	q(b, a).

	p(a, a).
	p(b, b).
	p(c, c).
	'''
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')
	pop = Population([a, b, c])
	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, Z])

	Xa = Binding(X, a)
	Yb = Binding(Y, b)
	Zb = Binding(Z, b)
	Zc = Binding(Z, c)

	s1 = Substitution([Xa, Yb, Zc])
	s2 = Substitution([Xa, Yb, Zb])

	consult('test_evaluate_1')

	print(r.evaluate(s1, 'test_evaluate_1')) # True
	print(r.evaluate(s2, 'test_evaluate_1')) # False
	print('\n')

	print(Not(r).evaluate(s1, 'test_evaluate_1')) # False
	print(Not(r).evaluate(s2, 'test_evaluate_1')) # True
	print('\n')

	q = Relation('q', [X, Y])
	p = Relation('p', [X, Y])

	Ya = Binding(Y, a)

	s3 = Substitution([Xa, Ya])
	s4 = Substitution([Xa, Yb])

	print(And(q, p).evaluate(s3, 'test_evaluate_1')) # False
	print(Or(q, p).evaluate(s3, 'test_evaluate_1')) # True
	print(Implies(q, p).evaluate(s4, 'test_evaluate_1')) # False
	print(Implies(q, p).evaluate(s3, 'test_evaluate_1')) # True

def test_evaluate_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])
	X = Variable('X', pop)

	p_a = Relation('p', [X, a])
	p_b = Relation('p', [X, b])
	p_c = Relation('p', [X, c])
	q_a = Relation('q', [X, a])
	q_b = Relation('q', [X, b])	
	q_c = Relation('q', [X, c])	

	variables = [p_a, p_b, p_c, q_a, q_b]
	values = [True, True, False, True, False]

	print(p_a.evaluateByList(variables, values)) # True
	print(p_c.evaluateByList(variables, values)) # False
	print(Not(p_a).evaluateByList(variables, values)) # False
	print(Not(p_c).evaluateByList(variables, values)) # True
	print(Or(p_b, q_b).evaluateByList(variables, values)) # True
	print(Or(p_c, q_b).evaluateByList(variables, values)) # False
	print(And(p_a, q_a).evaluateByList(variables, values)) # True
	print(And(p_c, q_b).evaluateByList(variables, values)) # False
	print(Implies(p_a, q_a).evaluateByList(variables, values)) # True
	print(Implies(p_a, q_b).evaluateByList(variables, values)) # False
	try:
		print(q_c.evaluateByList(variables, values)) # This does not work
	except ValueError:
		print('This does not work')

# test for probability

def test_relative_true_groundings_1():
	'''
	Correctness of this test relies on the content of
	test_relative_true_groundings_1.P

	The following settings were made, to make the tests
	work:

	r(a,a).
	r(b,a).
	'''
	a = Constant('a')
	b = Constant('b')

	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, Y])

	b = Binding(X, a)
	s = Substitution([b])

	consult('test_relative_true_groundings_1')

	x = r.getRelativeTrueGroundings(s, 'test_relative_true_groundings_1')
	print(x) # 0.5

def test_relative_true_groundings_2():
	'''
	Correctness of this test relies on the content of
	interpretation.P

	The following settings were made, to make the tests
	work:

	r(a, a, a).
	r(a, a, b).
	'''
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop_ab = Population([a, b])
	pop_ac = Population([a, c])
	pop_abc = Population([a, b, c])

	X = Variable('X', pop_ab)
	Y = Variable('Y', pop_ac)
	Z = Variable('Z', pop_abc)

	r = Relation('r', [X, Y, Z])

	s = Substitution([Binding(X, a)])

	consult('test_relative_true_groundings_2')

	x = r.getRelativeTrueGroundings(s, 'test_relative_true_groundings_2')
	# 2*3 = 6 total possible groundings.
	# 2 true groundings
	# => x = 2/6 = 1/3
	print(x) # ~ 0.333

def test_relative_true_groundings_3():
	'''
	We test the relative true groundings,
	for an empty module.
	'''
	a = Constant('a')
	#b = Constant('b')

	pop = Population([a])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, Y])

	bind = Binding(X, a)
	s = Substitution([bind])

	consult('test_relative_true_groundings_3')

	x = r.getRelativeTrueGroundings(s, 'test_relative_true_groundings_3')
	print(x) # 0