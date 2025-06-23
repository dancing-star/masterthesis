from modules import *


# Tests for Tuple:

def test_tuple_1():
	t = Tuple([1,2,3])
	s = Tuple([1,2,3])

	for x in t:
		print(x) # 1, 2, 3

	print('\n')
	print(s == t) # True
	print(s.getSize()) # 3
	print(s.getElementAt(1)) # 2

	u = s.setElementAt(1, 4)
	print('\n')
	for x in u:
		print(x) # 1, 4, 3

	print('\n')
	print(u == t) # False
	print(t.isEmpty()) # False

	v = Tuple([])
	print('\n')
	print(v.isEmpty()) # True
	print(v == t) # False

	print('\n')
	w = t.subTuple([1, 2])
	for x in w:
		print(x) # 2, 3

def test_tuple_2():
	a = Constant('a')
	X = Variable('X', Population([a]))
	r = Relation('r', [X])
	q = Relation('q', [X])
	f = StdFactor('f', [r, q], [D('0.5'), D('0.5'), D('0.5'), D('0.5')])

	for pair in f:
		for x in pair:
			print(x.getValue())
		print('\n')

# Tests for Factor:

# The following test are more for figuring out, how Factors work

def test_std_factor_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [Y, Z])
	p = Relation('p', [a, b])

	try:
		f1 = StdFactor('f1', [r, q, p], [D('0.1'), D('0.2'), D('0.3')]) # fails
	except IllegalArgumentError:
		print('Das schlug fehl!')

	f1 = StdFactor('f1', [r, q, p], [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]) # should work

	t1 = f1.getTuple(0)
	print('\n')
	print(type(t1.getElementAt(0)))
	print(t1.getSize())

	print('\n')
	for i in range(t1.getSize()):
		print(t1.getElementAt(i).getValue())

	print('\n')
	for t in f1:
		for i in range(t.getSize()):
			print(t.getElementAt(i).getValue())
		print('\n')

def test_std_factor_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [Y, Z])
	p = Relation('p', [a, b])

	f1 = StdFactor('f1', [r, q, p], [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')])
	f2 = StdFactor('f2', [r, q], [D('0.5'), D('0.5'), D('0.5'), D('0.5')])
	f3 = StdFactor('f3', [q, p], [D('0.1'), D('0.1'), D('0.2'), D('0.2')])

	print(f1.getValues())
	f4 = f1.pow(2, 1)
	print(f4.getValues())
	f5 = f2.multiply(f3)

	print('\n')
	for prv in f5.getVariables():
		print(prv.getName())
	print(f2.getValues())
	print(f3.getValues())
	print(f5.getValues())

	f6 = f1.sumOut(q)
	print('\n')
	for prv in f6.getVariables():
		print(prv.getName())
	print(f6.getValues())


# Tests by takiyama

def test_sum_out_first_var():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)
	X = Variable('X', pop)
	Y = Variable('Y', pop)

	f = Relation('f', [X])
	g = Relation('g', [X, Y])

	vars1 = [f, g]

	vals = [D('0.1'), D('0.2'), D('0.3'), D('0.4')]

	factor = StdFactor('F', vars1, vals)
	result = factor.sumOut(f)

	ansVars = [g]
	ansVals = [D('0.1') + D('0.3'), D('0.2') + D('0.4')]

	answer = StdFactor('F', ansVars, ansVals)
	print(result == answer) # True

def test_sum_out_second_var():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)
	X = Variable('X', pop)
	Y = Variable('Y', pop)

	f = Relation('f', [X])
	g = Relation('g', [X, Y])

	vars1 = [f, g]

	vals = [D('0.1'), D('0.2'), D('0.3'), D('0.4')]

	factor = StdFactor('F', vars1, vals)
	result = factor.sumOut(g)

	ansVars = [f]
	ansVals = [D('0.1') + D('0.2'), D('0.3') + D('0.4')]

	answer = StdFactor('F', ansVars, ansVals)
	print(result == answer) # True

def test_sum_out_counting_formula():
	population = []
	for i in range(1,4):
		population.append(Constant('x' + str(i)))
	pop1 = Population(population)
	pop2 = Population(population[:2])

	A = Variable('A', pop2)
	B = Variable('B', pop1)

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, set(), f)

	vars1 = [cf, h]

	vals = [D('1'), D('10'), D('100'), D('1000'), D('10000'), D('100000')]

	factor = StdFactor('F', vars1, vals)

	result = factor.sumOut(cf)

	ansVars = [h]
	ansVals = [D('10201'), D('102010')]

	answer = StdFactor('F', ansVars, ansVals)

	print(result == answer) # True

def test_pow_exponent_2():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop1 = Population(population)
	pop2 = Population(population[:3])

	A = Variable('A', pop1)
	B = Variable('B', pop2)

	f = Relation('f', [A])
	h = Relation('h', [B])

	vars1 = [f, h]
	vals = [D('2'), D('3'), D('4'), D('0')]

	factor = StdFactor('F', vars1, vals)
	result = factor.pow(2, 1)

	ansVars = [f, h]
	ansVals = [D('4'), D('9'), D('16'), D('0')]

	answer = StdFactor('F', ansVars, ansVals)
	print(result == answer) # True


# Histogram tests

def test_histogram_1():
	F = Bool(False)
	T = Bool(True)
	h = Histogram([F, T])
	print(h.getSize()) # 2
	print(h.containsBucket(F)) # True
	print(h.containsBucket(2)) # False
	h.setCount(F, 6)
	h.setCount(T, 8)
	print(h.getCount(F)) # 6
	print(h.getCount(T)) # 8
	h.addCount(F, 4)
	print(h.getCount(F)) # 10
	print(h.containsValue(8)) # True
	print(h.containsValue(7)) # False

	g = h.combine(T)
	print(g.getCount(T)) # 9
	print(g.getCount(F)) # 10

	print(h == g) # False
	f = copy(h)
	print(f == h) # True

	print(h.getCount(T)) # 8
	print(h.getCount(F)) # 10


# Test CountingFormulas

def test_counting_formula_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])
	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, Z, a])
	q = Relation('q', [X, Y])
	p = Relation('p', [Y, Z])

	cf = CountingFormula(X, set(), r)
	print(cf.getConstraints()) # set()
	print(cf.getName()) # r

	for v in cf.getParameters():
		print(v.getName()) # Y, Z

	print('\n')
	for v in cf.getTerms():
		print(v.getName()) # X, Y, Z, a

	print('\n')
	print(cf.getBoundVariable().getName()) # X
	print(cf.getPrvCodomainSize()) # 2
	print(cf.containsTerm(a)) # False
	print(cf.containsTerm(Y)) # True
	print(cf.containsTerm(Z)) # True
	print(cf.containsTerm(X)) # False
	print(cf.containsTerm(b)) # False

	F = Bool(False)
	T = Bool(True)
	h = Histogram([F, T])
	h.setCount(F, 10)
	h.setCount(T, 5)
	print('\n')
	print(cf.getSumOutCorrection(h))


# tests by takiyama

def test_substitution_Ax1_simple_cf():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)
	A = Variable('A', pop)
	f = Relation('f', [A])
	cf = CountingFormula(A, set(), f)

	x1 = A.getPopulation().getIndividualAt(0)
	s = Substitution([Binding(A, x1)])

	result = cf.applySubstitution(s)
	answer = CountingFormula(A, set(), f)

	print(result == answer) # True

def test_substitution_Bx1_simple_cf():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)
	A = Variable('A', pop)
	f = Relation('f', [A])
	cf = CountingFormula(A, set(), f)

	B = Variable('B', pop)
	x = Constant('x1')
	s = Substitution([Binding(B, x)])

	result = cf.applySubstitution(s)
	answer = CountingFormula(A, set(), f)

	print(result == answer) # True

def test_substitution_Ax1_complex_cf():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)

	f = Relation('f', [A, B])
	x1 = Constant('x1')
	c = InequalityConstraint(A, x1)
	cf = CountingFormula(A, {c}, f)

	s = Substitution([Binding(A, x1)])

	result = cf.applySubstitution(s)
	answer = CountingFormula(A, {c}, f)

	print(result == answer) # True

def test_substitution_AB_BC_complex_cf():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)
	f = Relation('f', [A, B])
	x1 = Constant('x1')
	c = InequalityConstraint(A, x1)
	cf = CountingFormula(A, {c}, f)

	D = Variable('C', pop)
	s = Substitution([Binding(A, B), Binding(B, D)])

	cf.applySubstitution(s)
	result = cf.applySubstitution(s)

	f = Relation('f', [B, D])
	c = InequalityConstraint(B, x1)
	answer1 = CountingFormula(B, {c}, f)

	f = Relation('f', [D, D])
	c = InequalityConstraint(D, x1)
	answer2 = CountingFormula(D, {c}, f)

	print(result == answer1 or result == answer2) # True

def test_substitution_AB_Bx1_complex_cf():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)
	f = Relation('f', [A, B])
	x1 = Constant('x1')
	c = InequalityConstraint(A, x1)
	cf = CountingFormula(A, {c}, f)

	s = Substitution([Binding(A, B), Binding(B, x1)])

	result = cf.applySubstitution(s)

	f = Relation('f', [A, x1])
	answer1 = CountingFormula(A, {c}, f)

	f = Relation('f', [B, B])
	c = InequalityConstraint(B, x1)
	answer2 = CountingFormula(B, {c}, f)

	print(result == answer1 or result == answer2) # True


# Tests for Prvs

def test_are_unifiable():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, a])
	q = Relation('q', [Y, a])
	p = Relation('r', [X, X, Y])
	s = Relation('r', [X, Y])

	print(Prvs.areUnifiable(r, q)) # False
	print(Prvs.areUnifiable(r, p)) # False
	print(Prvs.areUnifiable(r, s)) # True

def test_push_equations():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, Y, a])
	q = Relation('q', [Y, b, a])

	eq = Prvs.pushEquations(r, q)
	for e in eq:
		print(e.getFirstTerm().getName(), '=', e.getSecondTerm().getName()) # X=Y, Y=b, a=a

def test_mgu_1():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	rXYa = Relation('r', [X, Y, a])
	rXXX = Relation('r', [X, X, X])

	mgu = Prvs.mgu(rXXX, rXYa)

	for key in mgu:
		print(mgu.getReplacement(key).getName(), '/', key.getName()) # a/Y, a/X

def test_are_disjoint_1():
	a = Constant('a')
	b = Constant('b')
	pop = Population([a, b])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	rXYa = Relation('r', [X, Y, a])
	rXXX = Relation('r', [X, X, X])
	rXa = Relation('r', [X, a])
	rXXb = Relation('r', [X, X, b])
	qX = Relation('q', [X])

	print(Prvs.areDisjoint(rXYa, rXXX)) # False
	print(Prvs.areDisjoint(rXYa, rXa)) # True
	print(Prvs.areDisjoint(rXYa, rXXb)) # True
	print(Prvs.areDisjoint(rXYa, qX)) # True


# tests by takiyama

def test_mgu():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	X1 = Variable('X1', pop)
	X2 = Variable('X2', pop)
	X4 = Variable('X4', pop)

	c1 = X1.getPopulation().getIndividualAt(1)

	f1 = Relation('f', [X1, X2])
	f2 = Relation('f', [c1, X4])

	result = Prvs.mgu(f1, f2)

	for t in result.getVariables():
		print(t.getName(), result.getReplacement(t).getName())

	X1_1 = Binding(X1, X1.getPopulation().getIndividualAt(1))
	X2_X4 = Binding(X2, X4)

	answer = Substitution([X1_1, X2_X4])

	for t in answer.getVariables():
		print(t.getName(), result.getReplacement(t).getName())

	print(result == answer) # True

def test_set_intersection_1():
	population = []
	for i in range(1,11):
		population.append(Constant('lot' + str(i)))
	pop = Population(population)
	Lot = Variable('Lot', pop)
	sprinkler = Relation('sprinkler', [Lot])
	lot1 = Lot.getPopulation().getIndividualAt(0)
	constraints = {InequalityConstraint(Lot, lot1)}
	random_variable_set = RandomVariableSet(sprinkler, constraints)
	sprinkler1 = Relation('sprinkler', [lot1])
	print(Prvs.areDisjoint(random_variable_set, sprinkler1)) # True

def test_set_intersection_2():
	population = []
	for i in range(1,11):
		population.append(Constant('lot' + str(i)))
	pop = Population(population)
	Lot = Variable('Lot', pop)
	sprinkler = Relation('sprinkler', [Lot])
	lot1 = Lot.getPopulation().getIndividualAt(0)
	random_variable_set = RandomVariableSet(sprinkler, set())
	sprinkler1 = Relation('sprinkler', [lot1])
	print(Prvs.areDisjoint(random_variable_set, sprinkler1)) # False

def test_simple_multiplication():
	pop = []
	for i in range(10):
		pop.append(Constant('x' + str(i+1)))
	X = Variable('X', Population(pop))
	Y = Variable('Y', Population(pop))

	f = Relation('f', [X])
	h = Relation('h', [X, Y])

	vars1 = [f]
	vals1 = [D('0.1'), D('0.2')]

	factor1 = StdFactor('F1', vars1, vals1)

	vars2 = [f, h]

	vals2 = [D('0.1'), D('0.2'), D('0.3'), D('0.4')]

	factor2 = StdFactor('F2', vars2, vals2)

	result = factor1.multiply(factor2)

	ans_vars = [f, h]
	ans_vals = [D('0.1')*D('0.1'), D('0.1')*D('0.2'), D('0.2')*D('0.3'), D('0.2')*D('0.4')]

	answer = StdFactor('F', ans_vars, ans_vals)

	print(result == answer) # True

def test_multiplication_by_1():
	constant = ConstantFactor()

	f = Relation('f')
	h = Relation('h')
	vars1 = [f, h]

	vals1 = [D('1.0'), D('2.0'), D('3.0'), D('4.0')]
	factor = StdFactor('f', vars1, vals1)
	result = factor.multiply(constant)
	expected = factor

	print(expected == result) # True