from modules import *


# Tests for Parfactors

def test_std_parfactor_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]
	#q_values = [D('0.1'), D('0.2'), D('0.1'), D('0.2'), D('0.1'), D('0.2'), D('0.1'), D('0.2')]
	#p_values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_F = StdParfactor(constraints, F)

	for c in par_F.getConstraints():
		print(c.getFirstTerm().getName(), '!=', c.getSecondTerm().getName()) # X != b, Y != c, Z != a
	print('\n')

	print(par_F.getFactor().getName()) # F
	for lv in par_F.getVariables():
		print(lv.getName()) # X, Y, Z
	print('\n')

	for prv in par_F.getPrvs():
		print(prv.getName()) # r, q, p
	print('\n')

	for val in par_F.getFactor().getValues():
		print(val) # 0.1, 0.2, ..., 0.8
	print(par_F.getFactor().getValues()) # [D('0.1'), D('0.2'), ..., D('0.8')]
	print('\n')

	print(par_F.getSize()) # 8
	print('\n')

	for c in par_F.getConstraints():
		print(c.getFirstTerm().getName(), '!=', c.getSecondTerm().getName()) # X != b, Y != c, Z != a
	print('\n')
	for c in par_F.removeConstraintsInvolvingTerm(par_F.getConstraints(), a):
		print(c.getFirstTerm().getName(), '!=', c.getSecondTerm().getName()) # X != b, Y != c
	print('\n')

	print(par_F.isCountable(X)) # False
	print(par_F.getFactor().occurrences(X)) # 2
	print('\n')

	s = Relation('s', [X, Z])
	G = StdFactor('G', [r, s], [D('0.1'), D('0.2'), D('0.3'), D('0.4')])
	par_G = StdParfactor(set(), G)

	print(par_G.isCountable(X)) # False
	print(par_G.getFactor().occurrences(X)) # 2
	print(par_G.isCountable(Y)) # True
	print(par_G.getFactor().occurrences(Y)) # 1
	print('\n')
	
	print(par_F.containsPrv(r)) # True
	print(par_F.containsPrv(s)) # False
	print('\n')

	print(par_F.isConstant()) # False
	print(par_G.isConstant()) # False
	H = StdFactor('H', [r], [D('1.0'), D('1.0')])
	par_H = StdParfactor(set(), H)
	print(par_H.isConstant()) # True
	print('\n')

	print(par_F.constraintsContainTerm({InequalityConstraint(X, b), InequalityConstraint(Y, c)}, b)) # True
	print(par_F.constraintsContainTerm({InequalityConstraint(X, b), InequalityConstraint(Y, c)}, a)) # False
	print(par_F.constraintsContainTerm({InequalityConstraint(X, b), InequalityConstraint(Y, c)}, X)) # True
	print(par_F.constraintsContainTerm({InequalityConstraint(X, b), InequalityConstraint(Y, c)}, Z)) # False

def test_std_parfactor_2():
	n = 2
	population = []
	for i in range(1, n+1):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)
	C = Variable('C', pop)

	x1 = Constant('x1')

	f = Relation('f', [A, B])
	h = Relation('h', [C])
	
	f2 = [D('3'), D('5')]
	f3 = [D('3'), D('5'), D('7'), D('11')]

	g5 = StdParfactorBuilder().addVariables([f, h]).addValues(f3).build()
	g6 = StdParfactorBuilder().addVariables([f]).addValues(f2).build()

	result = g5.multiply(g6) # Only test, if multiplication works syntactically thus far.

	for p in result.getFactor().getVariables():
		print(p.getName())
		for t in p.getTerms():
			print(t.getName())
		print('\n')

	print(result.getFactor().getValues())
	print(not result._constraints) # True


def test_is_in_normal_form_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, Z])

	XY = InequalityConstraint(X, Y)
	Xa = InequalityConstraint(X, a)
	Ya = InequalityConstraint(Y, a)

	f = StdParfactorBuilder().addConstraints([XY]).addVariables([r]).addValues([D('0.5'), D('0.5')]).build()
	g = StdParfactorBuilder().addConstraints([XY, Ya]).addVariables([r]).addValues([D('0.5'), D('0.5')]).build()
	h = StdParfactorBuilder().addConstraints([XY, Ya, Xa]).addVariables([r]).addValues([D('0.5'), D('0.5')]).build()

	print(f.isInNormalForm()) # True
	print(g.isInNormalForm()) # False
	print(h.isInNormalForm()) # True


def test_scanner_1():
	a = Constant('a')
	pop = Population([a])
	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, a])
	q = Relation('q', [Z])

	pf1 = StdParfactorBuilder().addVariables([r, q]).addValues([D('0'), D('1'), D('0'), D('1')]).build()
	scanner1 = Scanner(pf1)

	vars1 = scanner1.getVariables()
	for lv in vars1:
		print(lv.getName()) # X, Y, Z

	cf = CountingFormula(Y, set(), r)
	pf2 = StdParfactorBuilder().addVariables([r, q]).addValues([D('0'), D('1'), D('0'), D('1')]).build()
	scanner2 = Scanner(pf2)
	vars2 = scanner2.getVariables()

	print('\n')
	for lv in vars2:
		print(lv.getName()) # X, Y, Z


def test_is_orthogonal_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, Z])
	q = Relation('q', [])

	Xa = InequalityConstraint(X, a)
	Xb = InequalityConstraint(X, b)
	Ya = InequalityConstraint(Y, a)
	Yb = InequalityConstraint(Y, b)

	XY = InequalityConstraint(X, Y)
	YZ = InequalityConstraint(Y, Z)
	ZY = InequalityConstraint(Z, Y)

	cf_1 = CountingFormula(X, {XY}, r)
	cf_2 = CountingFormula(X, {Xa}, r)

	pf1 = StdParfactorBuilder().addVariables([q]).addConstraints({Xa}).addValues([D('0'), D('1')]).build()
	pf2 = StdParfactorBuilder().addVariables([q]).addConstraints({Xa, Ya}).addValues([D('0'), D('1')]).build()
	pf3 = StdParfactorBuilder().addVariables([q]).addConstraints({YZ}).addValues([D('0'), D('1')]).build()
	pf4 = StdParfactorBuilder().addVariables([q]).addConstraints({ZY}).addValues([D('0'), D('1')]).build()

	pf5 = StdParfactorBuilder().addVariables([q]).addConstraints({XY}).addValues([D('0'), D('1')]).build()
	pf6 = StdParfactorBuilder().addVariables([q]).addConstraints({Xb, Yb}).addValues([D('0'), D('1')]).build()

	print(pf1.isOrthogonal(cf_1, a)) # False
	print(pf2.isOrthogonal(cf_1, a)) # True
	print(pf3.isOrthogonal(cf_1, Z)) # True
	print(pf3.isOrthogonal(cf_1, Z)) # True
	print('\n')

	print(pf5.isOrthogonal(cf_2, X)) # True
	print(pf5.isOrthogonal(cf_2, Z)) # True
	print(pf6.isOrthogonal(cf_2, b)) # True
	print(pf6.isOrthogonal(cf_2, c)) # True


def test_is_countable_1():
	a = Constant('a')
	pop = Population([a])
	X = Variable('X', pop)
	
	r = Relation('r', [X])
	q = Relation('q', [X])
	
	pf1 = StdParfactorBuilder().addVariables([r]).addValues([D('0'), D('1')]).build()
	pf2 = StdParfactorBuilder().addVariables([r, q]).addValues([D('0'), D('1'), D('0'), D('1')]).build()

	print(pf1.isCountable(X)) # True
	print(pf2.isCountable(X)) # False


def test_is_expandable_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, Z])
	q = Relation('q')

	XY = InequalityConstraint(X, Y)
	Xa = InequalityConstraint(X, a)
	Xb = InequalityConstraint(X, b)
	Ya = InequalityConstraint(Y, a)

	s = Substitution([Binding(X, a)])

	cf1 = CountingFormula(X, {XY}, r)
	cf2 = CountingFormula(X, {XY, Xa}, r)
	cf3 = CountingFormula(Y, {XY}, r)

	pf1 = StdParfactorBuilder().addVariables([q, cf1]).addConstraints({XY, Xa, Ya}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()
	pf2 = StdParfactorBuilder().addVariables([q, r]).addConstraints({XY, Xa, Ya}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()
	pf3 = StdParfactorBuilder().addVariables([q]).addConstraints({XY, Xa, Ya}).addValues([D('0.5'), D('0.5')]).build()
	pf4 = StdParfactorBuilder().addVariables([q, cf1]).addConstraints({XY, Xa, Xb, Ya}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()
	pf5 = StdParfactorBuilder().addVariables([q, cf2]).addConstraints({XY, Xa, Ya}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()
	pf6 = StdParfactorBuilder().addVariables([q, cf1]).addConstraints({XY}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()
	pf7 = StdParfactorBuilder().addVariables([q, cf3]).addConstraints({XY, Xa, Ya}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()

	print(pf1.isExpandable(cf1, s)) # True
	print(pf2.isExpandable(cf1, s)) # False
	print(pf3.isExpandable(cf1, s)) # False
	print(pf4.isExpandable(cf1, s)) # False
	print(pf5.isExpandable(cf1, s)) # False
	print(pf6.isExpandable(cf1, s)) # False
	print(pf7.isExpandable(cf1, s)) # False


# Tests for Simplifier

def test_simplifier_1():
	# REMARK: This test fails, because the constraint 'X != Z' is a corner case
	# for which the Simplification algorithm does not work.
	# However: For FLBNs, this corner case will never appear, so we're good.
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r = Relation('r', [X])
	q = Relation('q', [X, Y, Z])

	XZ = InequalityConstraint(X, Z)
	Ya = InequalityConstraint(Y, a)
	Yc = InequalityConstraint(Y, c)

	pf = StdParfactorBuilder().addVariables([r, q]).addConstraints({XZ, Ya, Yc}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()

	simplifier = Simplifier(pf)

	for c in simplifier._unaryConstraints:
		print(c.getFirstTerm().getName(), '!=', c.getSecondTerm().getName()) # Y!=a, Y!=c
	simplifier.simplifyVariablesWithPopulationOne()

	print('\n')
	for prv in simplifier._variables:
		print(prv.getName())
		for t in prv.getTerms():
			print(t.getName()) # ra, qaYZ
		print('\n')

	buffer = simplifier.getVariablesInConstraints()

	for lv in buffer:
		print(lv.getName()) # X, Y, Z

	other = simplifier.variablesInBinaryConstraintsInvolving(X)

	print('\n')
	for lv in other:
		print(lv.getName()) # Z


def test_simplifier_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r = Relation('r', [X])
	q = Relation('q', [X, Y, Z])

	XZ = InequalityConstraint(X, Z)
	Ya = InequalityConstraint(Y, a)
	Yc = InequalityConstraint(Y, c)

	pf = StdParfactorBuilder().addVariables([r, q]).addConstraints({XZ, Ya, Yc}).addValues([D('0.5'), D('0.5'), D('0.5'), D('0.5')]).build()

	simplifier = Simplifier(pf)

	pfs = simplifier.simplify()

	print('\n')
	for prv in pfs.getPrvs():
		print(prv.getName())
		for t in prv.getTerms():
			print(t.getName()) # ra, qabZ
		print('\n')


# Tests by takiyama

def test_split():
	population = []
	for i in range(1,11):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)

	x1 = Constant('x1')

	f = Relation('f', [A, B])
	h = Relation('h', [B])
	f1 = Relation('f', [A, x1])
	h1 = Relation('h', [x1])

	ab = InequalityConstraint(A, B)
	a0 = InequalityConstraint(A, x1)
	b0 = InequalityConstraint(B, x1)

	vals = [D('0.2'), D('0.3'), D('0.5'), D('0.7')]

	input1 = StdParfactorBuilder().addConstraints({ab}).addVariables([f, h]).addValues(vals).build()

	binding = Binding(B, x1)
	sub = Substitution([binding])
	output = input1.splitOn(sub)

	result = StdParfactorBuilder().addConstraints({a0}).addVariables([f1, h1]).addValues(vals).build()
	residue = StdParfactorBuilder().addConstraints({ab, b0}).addVariables([f, h]).addValues(vals).build()

	marginal = StdMarginalBuilder().setParfactors([residue]).build()	
	answer = SplitResult(result, marginal)

	print(output == answer) # True

class Color(RangeElement):
	'''
	Color class for the multiplication test
	'''
	def __init__(self):
		super().__init__()

	def equals(self, other):
		return self == other

GREEN = Color()
ORANGE = Color()
RED = Color()

def test_multiplication():
	n = 5
	m = 6

	population_ab = []
	population_c = []

	for i in range(1, n+1):
		population_ab.append(Constant('x' + str(i)))
	for i in range(1, m+1):
		population_c.append(Constant('y' + str(i)))

	pop_ab = Population(population_ab)
	pop_c = Population(population_c)

	A = Variable('A', pop_ab)
	B = Variable('B', pop_ab)
	C = Variable('C', pop_c)

	f = Relation('f', [A, B])
	h = Relation('h', [B])

	e_range = [GREEN, ORANGE, RED]
	e_param = [C]
	e = Relation('e', e_param)
	e._codomain = e_range

	AB = InequalityConstraint(A, B)

	g1vals = [D('1.0'), D('2.0'), D('3.0'), D('4.0')]
	g1 = StdParfactorBuilder().addConstraints([AB]).addVariables([f,h]).addValues(g1vals).build()

	g2vals = [D('1.0'), D('2.0'), D('3.0'), D('4.0'), D('5.0'), D('6.0')]
	g2 = StdParfactorBuilder().addVariables([e,h]).addValues(g2vals).build()

	product = g1.multiply(g2)

	# Answer
	ans_vals = []
	for i in range(len(g1vals)):
		alpha = g1vals[i]
		alpha_m = MathUtils.mathUtilsPow(alpha, 1, m)
		j = i % 2
		while j < len(g2vals):
			beta = g2vals[j]
			beta_n = MathUtils.mathUtilsPow(beta, 1, n - 1)
			ans_vals.append(alpha_m * beta_n)
			j = j + 2
	answer = StdParfactorBuilder().addConstraints([AB]).addVariables([f, h, e]).addValues(ans_vals).build()

	print(product == answer) # True


def test_multiplication_conditions():
	n = 2
	population = []
	for i in range(1, n+1):
		population.append(Constant('x' + str(i)))
	pop = Population(population)

	A = Variable('A', pop)
	B = Variable('B', pop)
	C = Variable('C', pop)

	x1 = Constant('x1')

	f = Relation('f', [A, B])
	f_A_x1 = Relation('f', [A, x1])
	h = Relation('h', [C])
	cf1 = CountingFormula(A, set(), f)
	cf2 = CountingFormula(A, set(), f_A_x1)

	f1 = [D('2'), D('4'), D('6')]
	f2 = [D('3'), D('5')]
	f3 = [D('3'), D('5'), D('7'), D('11')]

	g1 = StdParfactorBuilder().addVariables([cf1]).addValues(f1).build()
	g2 = StdParfactorBuilder().addVariables([f]).addValues(f2).build()
	g3 = StdParfactorBuilder().addVariables([cf2]).addValues(f1).build()
	g4 = StdParfactorBuilder().addVariables([f_A_x1]).addValues(f2).build()
	g5 = StdParfactorBuilder().addVariables([f, h]).addValues(f3).build()
	g6 = StdParfactorBuilder().addVariables([f]).addValues(f2).build()
	
	print(g1.isMultipliable(g2)) # False
	print(g3.isMultipliable(g4)) # False
	print(not g5.isMultipliable(g6)) # False
	print(g5.isMultipliable(g5)) # False
	# TODO: Last one should return False, however it doesn't. Why?
	# Note: After checking the semantic of the methods involving
	# isMultipliable, it seems that "g5.isMultipliable(g5)" is supposed to be true
	# However, takiyama says, it is supposed to be false. This is very strange.

def test_sum_out_counting_formula_with_cardinality_1():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	A = Variable('A', Population([x1]))
	B = Variable('B', Population([x1, x2, x3]))

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, set(), f)

	vals = [D('1.0'), D('10.0'), D('100.0'), D('1000.0')]
	input1 = StdParfactorBuilder().addVariables([cf, h]).addValues(vals).build()

	result = input1.sumOut(cf)

	ans_vals = [D('101.0'), D('1010.0')]
	answer = StdParfactorBuilder().addVariables([h]).addValues(ans_vals).build()

	print(result == answer) # True

def test_sum_out_counting_formula_with_cardinality_2():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	A = Variable('A', Population([x1, x2]))
	B = Variable('B', Population([x1, x2, x3]))

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, set(), f)

	vals = [D('1.0'), D('10.0'), D('100.0'), D('1000.0'), D('10000.0'), D('100000.0')]
	input1 = StdParfactorBuilder().addVariables([cf, h]).addValues(vals).build()

	result = input1.sumOut(cf)

	ans_vals = [D('10201.0'), D('102010.0')]
	answer = StdParfactorBuilder().addVariables([h]).addValues(ans_vals).build()

	print(result == answer) # True

def test_sum_out_counting_formula_with_cardinality_10():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')
	x4 = Constant('x4')
	x5 = Constant('x5')
	x6 = Constant('x6')
	x7 = Constant('x7')
	x8 = Constant('x8')
	x9 = Constant('x9')
	x10 = Constant('x10')

	A = Variable('A', Population([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]))
	B = Variable('B', Population([x1, x2, x3]))

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, set(), f)

	vals = [D('1.0') for i in range(22)]
	input1 = StdParfactorBuilder().addVariables([cf, h]).addValues(vals).build()

	result = input1.sumOut(cf)

	ans_vals = [D('1024.0'), D('1024.0')]
	answer = StdParfactorBuilder().addVariables([h]).addValues(ans_vals).build()

	print(result == answer) # True

def test_sum_out_counting_formula():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	A = Variable('A', Population([x1, x2, x3]))
	B = Variable('B', Population([x1, x2, x3]))

	f = Relation('f', [A])
	h = Relation('h', [B])

	AB = InequalityConstraint(A, B)
	cf = CountingFormula(A, {AB}, f)

	vals = [D('1.0'), D('10.0'), D('100.0'), D('1000.0'), D('10000.0'), D('100000.0')]
	input1 = StdParfactorBuilder().addVariables([cf, h]).addValues(vals).build()

	result = input1.sumOut(cf)

	ans_vals = [D('10201.0'), D('102010.0')]
	answer = StdParfactorBuilder().addVariables([h]).addValues(ans_vals).build()

	print(result == answer) # True

def test_expansion():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	A = Variable('A', Population([x1, x2, x3]))
	B = Variable('B', Population([x1, x2, x3]))

	f = Relation('f', [A])
	h = Relation('h', [B])	
	f_x2 = Relation('f', [x2])
	f_x3 = Relation('f', [x3])

	A_x1 = InequalityConstraint(A, x1)

	cf = CountingFormula(A, {A_x1}, f)

	input1 = StdParfactorBuilder().addVariables([cf, h]).addValues([D('0.2'), D('0.3'), D('0.5'), D('0.7'), D('0.11'), D('0.13')]).build()

	result = input1.expand(cf, x2)

	answer = StdParfactorBuilder().addVariables([f_x3, f_x2, h]).addValues([D('0.2'), D('0.3'), D('0.5'), D('0.7'), D('0.5'), D('0.7'), D('0.11'), D('0.13')]).build()

	print(result == answer) # True

def test_counting_without_constraints():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	pop = Population([x1, x2, x3])

	A = Variable('A', pop)

	f = Relation('f', [A])
	cf = CountingFormula(A, set(), f)

	input1 = StdParfactorBuilder().addVariables([f]).addValues([D('2'), D('3')]).build()

	result = input1.countVariable(A)

	answer = StdParfactorBuilder().addVariables([cf]).addValues([D('8'), D('12'), D('18'), D('27')]).build()

	print(result == answer) # True

def test_counting_exception():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	pop = Population([x1, x2, x3])

	A = Variable('A', pop)
	B = Variable('B', pop)

	f = Relation('f', [A])

	input1 = StdParfactorBuilder().addVariables([f]).addValues([D('2'), D('3')]).build()

	input1.countVariable(B) # fails

def test_counting_with_constraints():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	pop = Population([x1, x2, x3])

	A = Variable('A', pop)
	A_x1 = InequalityConstraint(A, x1)

	f = Relation('f', [A])
	cf = CountingFormula(A, {A_x1}, f)

	input1 = StdParfactorBuilder().addConstraints({A_x1}).addVariables([f]).addValues([D('2'), D('3')]).build()

	result = input1.countVariable(A)

	answer = StdParfactorBuilder().addVariables([cf]).addValues([D('4'), D('6'), D('9')]).build()

	print(result == answer) # True

def test_counting_without_constraints_and_two_variables():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	pop = Population([x1, x2, x3])

	A = Variable('A', pop)
	B = Variable('B', pop)

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, set(), f)

	input1 = StdParfactorBuilder().addVariables([f, h]).addValues([D('2'), D('3'), D('5'), D('7')]).build()

	result = input1.countVariable(A)

	answer = StdParfactorBuilder().addVariables([cf, h]).addValues([D('8'), D('27'), D('20'), D('63'), D('50'), D('147'), D('125'), D('343')]).build()

	print(answer == result) # True

def test_count():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	pop = Population([x1, x2, x3])

	A = Variable('A', pop)	
	B = Variable('B', pop)

	AB = InequalityConstraint(A, B)

	f = Relation('f', [A])
	h = Relation('h', [B])
	cf = CountingFormula(A, {AB}, f)

	input1 = StdParfactorBuilder().addConstraints({AB}).addVariables([f, h]).addValues([D('2'), D('3'), D('5'), D('7')]).build()

	result = input1.countVariable(A)

	vals = [D('4.0'), D('9.0'), D('10.0'), D('21.0'), D('25.0'), D('49.0')]
	answer = StdParfactorBuilder().addVariables([cf, h]).addValues(vals).build()

	print(result == answer) # True

def test_logical_variable_simplification_without_constraints():
	x1 = Constant('x1')
	A = Variable('A', Population([x1]))

	f = Relation('f', [A])
	f_x1 = Relation('f', [x1])

	input1 = StdParfactorBuilder().addVariables([f]).addValues([D('0'), D('1')]).build()
	result = input1.simplifyVariables()
	expected = StdParfactorBuilder().addVariables([f_x1]).addValues([D('0'), D('1')]).build()

	print(expected == result) # True

def test_logical_variable_simplification():
	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')
	x4 = Constant('x4')

	pop = Population([x1, x2, x3, x4])

	A = Variable('A', pop)
	B = Variable('B', pop)
	C = Variable('C', pop)

	f = Relation('f', [A, B])
	f_x4_x2 = Relation('f', [x4, x2])

	A_x1 = InequalityConstraint(A, x1)
	A_x2 = InequalityConstraint(A, x2)
	A_x3 = InequalityConstraint(A, x3)
	A_B = InequalityConstraint(A, B)
	A_C = InequalityConstraint(A, C)
	B_x1 = InequalityConstraint(B, x1)
	B_x3 = InequalityConstraint(B, x3)
	B_C = InequalityConstraint(B, C)
	C_x2 = InequalityConstraint(C, x2)
	C_x4 = InequalityConstraint(C, x4)

	input1 = StdParfactorBuilder().addConstraints({A_x1, A_x2, A_x3, A_B, A_C, B_x1, B_x3, B_C}).addVariables([f]).addValues([D('0.2'), D('0.3')]).build()
	result = input1.simplifyVariables()
	expected = StdParfactorBuilder().addConstraints({C_x2, C_x4}).addVariables([f_x4_x2]).addValues([D('0.2'), D('0.3')]).build()

	print(expected == result) # True

	print(result)

# Tests for StdParfactorBuilder

def test_std_parfactor_builder_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_empty = StdParfactorBuilder().build()
	print(par_empty.isConstant()) # True
	print('\n')

	par_F = StdParfactorBuilder().addConstraints(constraints).addVariables([r, q, p]).addValues(values).build()
	par_F_2 = StdParfactorBuilder().addConstraints(constraints).setFactor(F).build()

	print(par_F == par_F_2) # True
	print('\n')

	for c in par_F.getConstraints():
		print(c.getFirstTerm().getName(), '!=', c.getSecondTerm().getName()) # X != b, Y != c, Z != a
	print('\n')

	for lv in par_F.getVariables():
		print(lv.getName()) # X, Y, Z
	print('\n')

	for prv in par_F.getPrvs():
		print(prv.getName()) # r, q, p
	print('\n')

	print(par_F.getFactor().getValues()) # [D('0.1'), D('0.2'), ..., D('0.8')]
	print('\n')

	print(par_F.getSize()) # 8
	print('\n')


# Tests for StdDistribution:

def test_std_distribution_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)
	G = StdFactor('G', [r, q], values[:4])
	H = StdFactor('H', [r, p], values[:4])

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_F = StdParfactor(constraints, F)
	par_G = StdParfactor(constraints, G)
	par_H = StdParfactor(constraints, H)

	d = StdDistribution.of({par_F, par_G})

	for pf in d:
		print(pf.getFactor().getName()) # F, G
	print('\n')

	print(d.contains(par_F)) # True
	print(d.contains(par_H)) # False
	print(d.getSize()) # 2
	print(d.containsAll({par_F, par_G, par_H})) # False
	print('\n')

	d.addAllToPSet({par_H})
	print(d.contains(par_H)) # True
	print('\n')
	print(d.getSize()) # 3
	print(d.containsAll({par_F, par_G, par_H})) # True

	print(d.isEmpty()) # False


# Tests for StdMarginal(Builder):

def test_std_marginal_builder_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)
	G = StdFactor('G', [r, q], values[:4])
	H = StdFactor('H', [r, p], values[:4])

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_F = StdParfactor(constraints, F)
	par_G = StdParfactor(constraints, G)
	par_H = StdParfactor(constraints, H)

	rv_set = RandomVariableSet(r, constraints)

	marginal_builder = StdMarginalBuilder().setParfactors([par_F, par_G]).setPreservable(rv_set)

	for pf in marginal_builder._parfactors:
		print(pf.getFactor().getName()) # F, G
	print(marginal_builder._preservable.getPrv().getName()) # r
	print('\n')

	marginal_builder.addParfactor(par_H)
	for pf in marginal_builder._parfactors:
		print(pf.getFactor().getName()) # F, G, H
	print('\n')

	marginal_builder.removeParfactor(par_G)
	for pf in marginal_builder._parfactors:
		print(pf.getFactor().getName()) # F, H
	print('\n')

	marginal_builder.replaceParfactor(par_H, par_G)
	for pf in marginal_builder._parfactors:
		print(pf.getFactor().getName()) # F, G
	print('\n')

	d = marginal_builder.getDistribution()

	for pf in d:
		print(pf.getFactor().getName()) # F, G

def test_std_marginal_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)
	G = StdFactor('G', [r, q], values[:4])
	H = StdFactor('H', [r, p], values[:4])

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_F = StdParfactor(constraints, F)
	par_G = StdParfactor(constraints, G)
	par_H = StdParfactor(constraints, H)

	rv_set = RandomVariableSet(r, constraints)

	m = StdMarginalBuilder().setParfactors([par_F, par_G]).setPreservable(rv_set).build()

	for pf in m:
		print(pf.getFactor().getName()) # F, G
	print('\n')

	print(m.isEmpty()) # False
	print(StdMarginalBuilder().build().isEmpty()) # True
	print(m.getSize()) # 2
	print(m.getPreservable().getPrv().getName()) # r
	print('\n')

	e = m.getEliminables()
	for rv_set in e:
		print(rv_set.getPrv().getName()) # What does this do?
		for t in rv_set.getPrv().getTerms():
			print(t.getName())
		print('\n')


# Tests for SplitResult

def test_split_result_1():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	pop = Population([a, b, c])

	X = Variable('X', pop)
	Y = Variable('Y', pop)
	Z = Variable('Z', pop)

	r = Relation('r', [X, Y, c])
	q = Relation('q', [X, b, Z])
	p = Relation('p', [a, Y, Z])

	values = [D('0.1'), D('0.2'), D('0.3'), D('0.4'), D('0.5'), D('0.6'), D('0.7'), D('0.8')]

	F = StdFactor('F', [r, q, p], values)
	G = StdFactor('G', [r, q], values[:4])
	H = StdFactor('H', [r, p], values[:4])

	constraint1 = InequalityConstraint(X, b)
	constraint2 = InequalityConstraint(Y, c)
	constraint3 = InequalityConstraint(Z, a)

	constraints = {constraint1, constraint2, constraint3}

	par_F = StdParfactor(constraints, F)
	par_G = StdParfactor(constraints, G)
	par_H = StdParfactor(constraints, H)

	rv_set = RandomVariableSet(r, constraints)

	m1 = StdMarginalBuilder().setParfactors([par_F, par_G, par_H]).setPreservable(rv_set).build()
	m2 = StdMarginalBuilder().setParfactors([par_H, par_G]).setPreservable(rv_set).build()
	
	sr_1 = SplitResult(par_F, m1)
	sr_1_1 = SplitResult(par_F, m1)
	sr_2 = SplitResult(par_F, m2)

	print(sr_1.getResult().getFactor().getName()) # F
	print('\n')

	for p in sr_1.getResidue():
		print(p.getFactor().getName()) # F, G, H
	print('\n')

	for p in sr_1.getDistribution():
		print(p.getFactor().getName()) # F, G, H
	print('\n')

	for p in sr_2.getDistribution():
		print(p.getFactor().getName()) # F, G, H
	print('\n')

	print(sr_1 == sr_1_1) # True
	print(sr_1 == sr_2) # False
