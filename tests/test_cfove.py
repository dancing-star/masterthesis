from modules import *


# Tests for CountingConvert

def test_counting_convert_1():
	a = Constant('a')
	b = Constant('b')

	pop = Population([a, b])
	X = Variable('X', pop)
	Y = Variable('Y', pop)

	r = Relation('r', [X, Y])
	q = Relation('q', [Y])

	f = StdFactor('f', [r, q], [D('1'), D('1'), D('1'), D('1')])
	g = StdParfactor(set(), f)
	rvs = RandomVariableSet(r, set())
	inp = StdMarginalBuilder().setParfactors({g}).setPreservable(rvs).build()

	cc = CountingConvert(inp, g, X)
	result = cc.run()

	print(result.getDistribution().getSize()) # 1
	result_parfactor = next(iter(result.getDistribution().toSet()))
	result_formulas = result_parfactor.getFactor().getVariables() # CountingFormula
	print(len(result_formulas)) # 2
	print(result_formulas[0].getName()) # r
	print(result_formulas[1].getName()) # q
	print(isinstance(result_formulas[0], CountingFormula)) # True
	print(isinstance(result_formulas[1], CountingFormula)) # False
	print(result_formulas[0].getBoundVariable().getName()) # X
	for x in result_formulas[0].getParameters():
		print(x.getName()) # Y


# Tests for Shatter

def test_mutable_queue_1():
	queue = MutableQueue([0, 1, 2, 3])
	iterator = queue.iterator()
	while iterator.hasNext(queue._queue):
		print(iterator.next(queue._queue)._values) # [0,1], [0,2], [0,3], [1,2], [2,3]

def test_mutable_queue_2():
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')
	d = Constant('d')
	queue = MutableQueue([a, b, c, d, a])
	iterator = queue.iterator()

	for t in queue._queue:
		print(t.getName()) # a, b, c, d, a
	queue.remove(Tuple([a, c]))

	print('\n')
	for t in queue._queue:
		print(t.getName()) # b, d, a

def test_shatter_1():
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
	marginal = StdMarginalBuilder().setParfactors([pf]).setPreservable(RandomVariableSet(r, set())).build()
	shatter = Shatter(marginal)
	m = shatter.simplifyVariables(marginal)

	for pf in m:
		print(pf) # ra, qabZ

def test_shatter_2():
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
	marginal = StdMarginalBuilder().setParfactors([pf]).setPreservable(RandomVariableSet(r, set())).build()
	shatter = Shatter(marginal)

	shatter.renameAllVariables()

	# TODO: Names not consistent. Check later if this matters
	for pf in shatter._marginal:
		for prv in pf.getPrvs():
			print(prv.getName())
			for t in prv.getTerms():
				print(t.getName())
			print('\n')

	old = []
	for pf in shatter._marginal:
		old.append(pf.applySubstitution(NameGenerator.getOldNames()))

	for pf in old:
		for prv in pf.getPrvs():
			print(prv.getName())
			for t in prv.getTerms():
				print(t.getName()) # rX, qXYZ
			print('\n')

def test_shatter_3():
	pop = []
	for i in range(15):
		pop.append(Constant('lot' + str(i+1)))
	Lot = Variable('Lot', Population(pop))
	lot1 = Constant('lot1')

	rain = Relation('rain')
	sprinkler = Relation('sprinkler', [Lot])
	wet_grass = Relation('wet_grass', [Lot])
	wet_grass_lot1 = Relation('wet_grass', [lot1])
	sprinkler_lot1 = Relation('sprinkler', [lot1])

	Lot_lot1 = InequalityConstraint(Lot, lot1)

	f1 = [D('0.8'), D('0.2')]
	f2 = [D('0.6'), D('0.4')]
	f3 = [D('1.0'), D('0.0'), D('0.2'), D('0.8'), D('0.1'), D('0.9'), D('0.01'), D('0.99')]
	f4 = [D('0.0'), D('1.0')]

	g1 = StdParfactorBuilder().addVariables([rain]).addValues(f1).build()
	g2 = StdParfactorBuilder().addVariables([sprinkler]).addValues(f2).build()
	g3 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addValues(f3).build()
	g4 = StdParfactorBuilder().addVariables([wet_grass_lot1]).addValues(f4).build()
	#g5 = StdParfactorBuilder().addVariables([rain, sprinkler_lot1, wet_grass_lot1]).addValues(f3).build()
	#g6 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addConstraints({Lot_lot1}).addValues(f3).build()
	#g7 = StdParfactorBuilder().addVariables([sprinkler_lot1]).addValues(f2).build()
	#g8 = StdParfactorBuilder().addVariables([sprinkler]).addConstraints({Lot_lot1}).addValues(f2).build()

	marginal = StdMarginalBuilder().setParfactors([g1, g2, g3, g4]).build()

	shatter = Shatter(marginal)
	marginal_size = shatter._marginal.getDistribution().getSize()
	print('\n')
	print(marginal_size) # 4

	shatter._marginal = shatter.simplifyVariables(shatter._marginal)
	print('\n')
	print('-------------')
	print('\n')
	for pf in shatter._marginal:
		for prv in pf.getPrvs():
			print(prv.getName())
			for lv in prv.getTerms():
				print(lv.getName()) # rain, sprinklerLot, rain, sprinklerLot, wet_grassLot, wet_grasslot1 
			print('\n')

	shatter.renameAllVariables()
	print('\n')
	print('-------------')
	print('\n')
	for pf in shatter._marginal:
		for prv in pf.getPrvs():
			print(prv.getName())
			for lv in prv.getTerms():
				print(lv.getName()) # rain, sprinklerX1, rain, sprinklerX2, wet_grassX2, wet_grasslot1 
			print('\n')

	queue = MutableQueue(shatter._marginal.getDistribution().toSet())
	it = queue.iterator()
	# (g1, g2) ~> rain + sprinkler
	# (g1, g3) ~> rain + rain, sprinkler, wet_grass
	# (g1, g4) ~> rain + wet_grass
	# (g2, g3) ~> sprinkler + rain, sprinkler, wet_grass
	# (g2, g4) ~> sprinkler + wet_grass
	# (g3, g4) ~> rain, sprinkler, wet_grass + wet_grass
	print('\n')
	print('-------------')
	print('\n')
	while it.hasNext(queue._queue):
		pair = it.next(queue._queue)
		for prv in pair.getElementAt(0).getPrvs():
			print(prv.getName())
		print('+++++++++')
		for prv in pair.getElementAt(1).getPrvs():
			print(prv.getName())
		print('\n')
		print('***************')
		print('\n')

	result = shatter.unify(g1, g2)

	print('\n')
	print('-------------')
	print('\n')
	print(result.isEmpty()) # True

	result = shatter.unify(g1, g3)

	print('\n')
	print('-------------')
	print('\n')
	print(result.isEmpty()) # True

def test_split_1():
	# Split on substitution
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r = Relation('r', [X, Y])
	q = Relation('q', [X, Y, Z])

	vals = [D('1.0'), D('1.0'), D('1.0'), D('1.0')]

	Yc = InequalityConstraint(Y, c)

	pf = StdParfactorBuilder().addVariables([r, q]).addConstraints({Yc}).addValues(vals).build()
	s = Substitution([Binding(X, a), Binding(Y, Z), Binding(Z, b)])

	input1 = StdMarginalBuilder().build()
	shatter = Shatter(input1)

	result = shatter.splitOnSubstitution(pf, s)

	print(result._result)
	print('\n')
	for p in result._residue:
		print(str(p) + '\n') 	# r(a, b), q(a, b, b), {}
									# r(X, Y), q(X, Y, Z), {Y!=c, X!=a}
									# r(a, Y), q(a, Y, Z), {Y!=c, Y!=Z}
									# r(a, Z), q(a, Z, Z), {Z!=c, Z!=b}

def test_split_2():
	# Split on constraints
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r = Relation('r', [X, Y])
	q = Relation('q', [X, Y, Z])

	vals = [D('1.0'), D('1.0'), D('1.0'), D('1.0')]

	Yc = InequalityConstraint(Y, c)
	Xa = InequalityConstraint(X, a)
	YZ = InequalityConstraint(Y, Z)
	Zb = InequalityConstraint(Z, b)

	pf = StdParfactorBuilder().addVariables([r, q]).addConstraints({Yc}).addValues(vals).build()
	split = SplitResult(pf, StdMarginalBuilder().build())

	input1 = StdMarginalBuilder().build()
	shatter = Shatter(input1)

	result = shatter.splitOnConstraints(split, {Xa, YZ, Zb})

	print(result._result)
	print('\n')
	for p in result._residue:
		print(str(p) + '\n')	# r(X, Y), q(X, Y, Z), {Y!=c, Y!=Z, X!=a, Z!=b}
									# r(a, Y), q(a, Y, Z), {Y!=c}
									# r(X, Z), q(X, Z, Z), {Z!=c, X!=a}
									# r(X, Y), q(X, Y, b), {Y!=c, Y!=b, X!=a}

	# Remark: Works technically, but result depends on order in which {Xa, YZ, Zb} is iteratet
	# Takiyama uses sets here. Is this correct? Does not seem so.
	# TODO: Check if this is correct.

def test_unify_1():
	# Split on substitution
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a, b, c]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r1 = Relation('r', [X, Y, Z])
	r2 = Relation('r', [Y, X, a])
	q = Relation('q', [X])

	vals1 = [D('1.0'), D('1.0'), D('1.0'), D('1.0')]
	vals2 = [D('1.0'), D('1.0')]

	Yc = InequalityConstraint(Y, c)

	pf1 = StdParfactorBuilder().addVariables([r1, q]).addConstraints({Yc}).addValues(vals1).build()
	pf2 = StdParfactorBuilder().addVariables([r2]).addValues(vals2).build()
	s = Substitution([Binding(X, a), Binding(Y, Z), Binding(Z, b)])

	input1 = StdMarginalBuilder().build()
	shatter = Shatter(input1)

	mgu = Prvs.mgu(r1, r2)
	for binding in mgu.asList():
		print(binding.getFirstTerm().getName(), '->', binding.getSecondTerm().getName()) # Z->a, Y->X

	print('\n\n')

	result = shatter.unifyOnPrvs(pf1, r1, pf2, r2)
	for p in result:
		print(p)
		print('\n---------------------\n')	# r(X, X, a), q(X), {X!=c}
											# r(X, Y, Z), q(X), {Y!=c, Z!=a}
											# r(X, Y, a), q(X), {Y!=c, Y!=X}
											# r(c, c, a), {}
											# r(Y, X, a), {Y!=X}
											# r(X, X, a), {X!=c}

def test_global_sum_out_1():
	# Syntactic test
	a = Constant('a')
	b = Constant('b')
	c = Constant('c')

	X = Variable('X', Population([a, b, c]))
	Y = Variable('Y', Population([a, b, c]))
	Z = Variable('Z', Population([a, b, c]))

	r = Relation('r', [X, Y])
	q = Relation('q', [Z])

	vals1 = [D('0.5'), D('0.5'), D('1.0'), D('0.0')]
	vals2 = [D('0.75'), D('0.25')]

	g = StdParfactorBuilder().addVariables([r, q]).addValues(vals1).build()
	h = StdParfactorBuilder().addVariables([q]).addValues(vals2).build()

	print(g.isMultipliable(h)) # True

	rv = RandomVariableSet(r, set())
	m = StdMarginalBuilder().setParfactors([g, h]).build()
	gs = GlobalSumOut(m, rv)

	cf = CountingFormula(Z, set(), q)
	f = StdParfactorBuilder().addVariables([r, cf]).addValues(vals1 + vals1).build()
	print(f)

	print(gs.cost())
	print(gs._isPossible)

def test_global_sum_out_2():
	lot1 = Constant('lot1')
	lot2 = Constant('lot2')
	lot3 = Constant('lot3')
	lot4 = Constant('lot4')
	lot5 = Constant('lot5')
	pop = Population([lot1, lot2, lot3, lot4, lot5])
	Lot = Variable('Lot', pop)

	cloudy = Relation('cloudy')
	rain = Relation('rain')
	wet_grass = Relation('wet_grass', [Lot])
	sprinkler = Relation('sprinkler', [Lot])
	cloudy2 = copy(cloudy)

	vals1 = [D('0.5'), D('0.5')]
	vals2 = [D('0.8'), D('0.2'), D('0.2'), D('0.8')]
	vals3 = [D('1.0'), D('1.0')]
	vals4 = [D('0.5'), D('0.5'), D('0.9'), D('0.1')]
	vals5 = [D('1.0'), D('0.0'), D('0.1'), D('0.9'), D('0.1'), D('0.9'), D('0.01'), D('0.99')]

	p1 = StdParfactorBuilder().addVariables([cloudy]).addValues(vals1).build()
	p2 = StdParfactorBuilder().addVariables([cloudy, rain]).addValues(vals2).build()
	p3 = StdParfactorBuilder().addVariables([wet_grass]).addValues(vals3).build()
	p4 = StdParfactorBuilder().addVariables([cloudy2, sprinkler]).addValues(vals4).build()
	p5 = StdParfactorBuilder().addVariables([sprinkler, rain, wet_grass]).addValues(vals5).build()

	print(cloudy == cloudy2) # True

	f1 = StdFactor('f1', [cloudy], vals1)
	f4 = StdFactor('f4', [cloudy, sprinkler], vals4)
	product = f4.multiply(f1)
	print([cloudy2, sprinkler].index(cloudy))
	print(f1.getMapOfCommonVariables(f1, f4))

	rv = RandomVariableSet(cloudy, set())
	m = StdMarginalBuilder().setParfactors([p1, p2, p3, p4, p5]).build()
	result = GlobalSumOut(m, rv) # No Error

	p6 = p4.multiply(p1)
	print(p6)

# Tests for CFOVE

def test_cfove_1():
	# Syntactic Test
	a1 = Constant('a1')
	a2 = Constant('a2')
	a3 = Constant('a3')
	a4 = Constant('a4')
	pop = Population([a1, a2, a3, a4])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	a = Relation('a', [X])
	b = Relation('b', [Y])

	f = StdFactor('f', [b, a], [D('1'), D('2'), D('4'), D('5')])
	g = StdParfactor(set(), f)
	rvs = RandomVariableSet(b, set())
	inp = StdMarginalBuilder().setParfactors({g}).setPreservable(rvs).build()	
	cfove = CFOVE(inp)

	result = cfove.run()
	print(result) # StdParfactor object at ...
	print(result.getFactor()) # StdFactor object at ...
	print(result.getFactor().getValues())
	for prv in result.getFactor().getVariables():
		print(prv.getName())
	normalizing_factor = float(sum(result.getFactor().getValues()))
	print(float(result.getFactor().getValues()[-1]) / normalizing_factor)

def test_cfove_2():
	# Syntactic Test
	a1 = Constant('a1')
	a2 = Constant('a2')
	pop = Population([a1, a2])

	X = Variable('X', pop)
	Y = Variable('Y', pop)

	a = Relation('a', [X])
	b = Relation('b', [X, Y])
	c = Relation('c', [Y])

	f1 = StdFactor('f1', [c], [D('0.2'), D('0.8')])
	f2 = StdFactor('f2', [b, c], [D('0.7'), D('0.4'), D('0.3'), D('0.6')])
	# F, F, F -> 1
	# F, F, T -> 0
	# F, T, F -> 0
	# F, T, T -> 0
	# T, F, F -> 0
	# T, F, T -> 1
	# T, T, F -> 1
	# T, T, T -> 1
	f3 = StdFactor('f3', [a, Relation('b', [X, a1]), Relation('b', [X, a2])], [D('1.0'), D('0.0'), D('0.0'), D('0.0'), D('0.0'), D('1.0'), D('1.0'), D('1.0')])

	g1 = StdParfactor(set(), f1)
	g2 = StdParfactor(set(), f2)
	g3 = StdParfactor(set(), f3)

	rvs = RandomVariableSet(a, set())

	input1 = StdMarginalBuilder().setParfactors({g1, g2, g3}).setPreservable(rvs).build()
	cfove = CFOVE(input1)
	result = cfove.run()

	print(result)

# Tests by Takiyama

# MacroOperation tests

def test_shatter():
	pop = []
	for i in range(15):
		pop.append(Constant('lot' + str(i+1)))
	Lot = Variable('Lot', Population(pop))
	lot1 = Constant('lot1')

	rain = Relation('rain')
	sprinkler = Relation('sprinkler', [Lot])
	wet_grass = Relation('wet_grass', [Lot])
	wet_grass_lot1 = Relation('wet_grass', [lot1])
	sprinkler_lot1 = Relation('sprinkler', [lot1])

	Lot_lot1 = InequalityConstraint(Lot, lot1)

	f1 = [D('0.8'), D('0.2')]
	f2 = [D('0.6'), D('0.4')]
	f3 = [D('1.0'), D('0.0'), D('0.2'), D('0.8'), D('0.1'), D('0.9'), D('0.01'), D('0.99')]
	f4 = [D('0.0'), D('1.0')]

	g1 = StdParfactorBuilder().addVariables([rain]).addValues(f1).build()
	g2 = StdParfactorBuilder().addVariables([sprinkler]).addValues(f2).build()
	g3 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addValues(f3).build()
	g4 = StdParfactorBuilder().addVariables([wet_grass_lot1]).addValues(f4).build()
	g5 = StdParfactorBuilder().addVariables([rain, sprinkler_lot1, wet_grass_lot1]).addValues(f3).build()
	g6 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addConstraints({Lot_lot1}).addValues(f3).build()
	g7 = StdParfactorBuilder().addVariables([sprinkler_lot1]).addValues(f2).build()
	g8 = StdParfactorBuilder().addVariables([sprinkler]).addConstraints({Lot_lot1}).addValues(f2).build()

	marginal = StdMarginalBuilder().setParfactors([g1, g2, g3, g4]).build()

	shatter = Shatter(marginal)

	result = shatter.run()
	expected = StdMarginalBuilder().setParfactors([g1, g4, g5, g6, g7, g8]).build()

	print(expected == result) # True

def test_simple_tricky_shatter():
	x1 = Constant('x1')
	x2 = Constant('x2')
	A = Variable('A', Population([x1, x2]))

	f = Relation('f', [A])
	f_x1 = Relation('f', [x1])
	f_x2 = Relation('f', [x2])

	val = [D('0'), D('1')]
	g1 = StdParfactorBuilder().addVariables([f]).addValues(val).build()
	g2 = StdParfactorBuilder().addVariables([f_x1]).addValues(val).build()
	g3 = StdParfactorBuilder().addVariables([f_x2]).addValues(val).build()

	input1 = StdMarginalBuilder(2).setParfactors([g1, g2]).build()
	shatter = Shatter(input1)
	result = shatter.run()
	expected = StdMarginalBuilder().setParfactors([g2, g2, g3]).build()

	print(expected == result) # True

def test_shatter_with_counting_formula():
	n = 3
	pop = []
	for i in range(n):
		pop.append(Constant('x' + str(i+1)))
	pop1 = Population(pop)
	X = Variable('X', pop1)
	Y = Variable('Y', pop1)

	x1 = Constant('x1')

	X_x1 = InequalityConstraint(X, x1)

	b = Relation('b', [X])
	c = Relation('c', [X])
	e = Relation('e', [X])
	e_X1 = Relation('e', [x1])
	r = Relation('r', [X, Y])
	r_x1_Y = Relation('r', [x1, Y])
	cf = CountingFormula(Y, set(), r)
	cf_x1 = CountingFormula(Y, set(), r_x1_Y)

	g1 = StdParfactorBuilder().addVariables([cf, e]).build()
	g2 = StdParfactorBuilder().addVariables([b, e, c]).addConstraints({X_x1}).build()
	g3 = StdParfactorBuilder().addVariables([cf, e]).addConstraints({X_x1}).build()
	g4 = StdParfactorBuilder().addVariables([cf_x1, e_X1]).build()

	input1 = StdMarginalBuilder().setParfactors({g1, g2}).build()

	shatter = Shatter(input1)
	result = shatter.run()
	expected = StdMarginalBuilder().setParfactors({g2, g3, g4}).build()

	print(expected == result) # True

def test_full_expand():
	pop = []
	for i in range(3):
		pop.append(Constant('x' + str(i+1)))
	A = Variable('A', Population(pop))
	B = Variable('B', Population(pop))

	x1 = Constant('x1')
	x2 = Constant('x2')
	x3 = Constant('x3')

	A_x1 = InequalityConstraint(A, x1)
	A_x2 = InequalityConstraint(A, x2)
	A_x3 = InequalityConstraint(A, x3)

	f_A = Relation('f', [A])
	f_x2 = Relation('f', [x2])
	f_x3 = Relation('f', [x3])
	h_B = Relation('h', [B])
	cf = CountingFormula(A, {A_x1}, f_A)

	g1 = StdParfactorBuilder().addVariables([f_A]).addValues([D('0.4'), D('0.6')]).build()
	g2 = StdParfactorBuilder().addVariables([cf, h_B]).addValues([D('1.0'), D('2.0'), D('3.0'), D('4.0'), D('5.0'), D('6.0')]).build()
	g3 = StdParfactorBuilder().addVariables([f_A]).addConstraints({A_x2, A_x3}).addValues([D('0.4'), D('0.6')]).build()
	g4 = StdParfactorBuilder().addVariables([f_x2]).addValues([D('0.4'), D('0.6')]).build()
	g5 = StdParfactorBuilder().addVariables([f_x3]).addValues([D('0.4'), D('0.6')]).build()
	g6 = StdParfactorBuilder().addVariables([f_x3, f_x2, h_B]).addValues([D('1.0'), D('2.0'), D('3.0'), D('4.0'), D('3.0'), D('4.0'), D('5.0'), D('6.0')]).build()

	marginal = StdMarginalBuilder(2).setParfactors([g1, g2]).build()

	full_expand = FullExpand(marginal, g2, cf)

	result = full_expand.run()
	expected = StdMarginalBuilder().setParfactors([g3, g4, g5, g6]).build()

	for p in result:
		print(str(p) + '\n-------------------\n')

	# REMARK: This test technically fails, as the resulting parfacors
	#		  contain f(x1) rather than f(A) : {A!=x2, A!=x3}.
	#		  Taking into account the variable simplification at the end
	#		  of Shatter, this however seems correct, as the domain of A
	#		  only contains x1, x2, x3.
	#		  Clearly those to parfactors are equivalent, so this should not
	#		  be a big deal. Nevertheless it raises the question, what takiyama
	#		  was doing.
	print(expected == result) # True

def test_propositionalize():
	lot1 = Constant('lot1')
	lot2 = Constant('lot2')
	lot3 = Constant('lot3')

	pop = Population([lot1, lot2, lot3])
	Lot = Variable('Lot', pop)

	rain = Relation('rain')
	sprinkler = Relation('sprinkler', [Lot])
	wet_grass = Relation('wet_grass', [Lot])
	wet_grass_lot1 = Relation('wet_grass', [lot1])
	wet_grass_lot2 = Relation('wet_grass', [lot2])
	wet_grass_lot3 = Relation('wet_grass', [lot3])
	sprinkler_lot1 = Relation('sprinkler', [lot1])
	sprinkler_lot2 = Relation('sprinkler', [lot2])
	sprinkler_lot3 = Relation('sprinkler', [lot3])

	f1 = [D('0.8'), D('0.2')]
	f2 = [D('0.6'), D('0.4')]
	f3 = [D('1.0'), D('0.0'), D('0.2'), D('0.8'),D('0.1'), D('0.9'), D('0.01'), D('0.99')]
	f4 = [D('0.0'), D('1.0')]

	g1 = StdParfactorBuilder().addVariables([rain]).addValues(f1).build()
	g2 = StdParfactorBuilder().addVariables([sprinkler]).addValues(f2).build()
	g3 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addValues(f3).build()
	g4 = StdParfactorBuilder().addVariables([wet_grass_lot1]).addValues(f4).build()

	g2_1 = StdParfactorBuilder().addVariables([sprinkler_lot1]).addValues(f2).build()
	g2_2 = StdParfactorBuilder().addVariables([sprinkler_lot2]).addValues(f2).build()
	g2_3 = StdParfactorBuilder().addVariables([sprinkler_lot3]).addValues(f2).build()

	g3_1 = StdParfactorBuilder().addVariables([rain, sprinkler_lot1, wet_grass_lot1]).addValues(f3).build()
	g3_2 = StdParfactorBuilder().addVariables([rain, sprinkler_lot2, wet_grass_lot2]).addValues(f3).build()
	g3_3 = StdParfactorBuilder().addVariables([rain, sprinkler_lot3, wet_grass_lot3]).addValues(f3).build()

	marginal = StdMarginalBuilder().setParfactors([g1, g2, g3, g4]).build()
	propositionalize = Propositionalize(marginal, g3, Lot)

	result = propositionalize.run()
	expected = StdMarginalBuilder().setParfactors([g1, g4, g2_1, g2_2, g2_3, g3_1, g3_2, g3_3]).build()

	for p in result:
		print(str(p) + '\n-------------------\n')

	# REMARK: This test technically fails, as in addition to the parfactors
	#		  in 'expected', it yields another constant parfactor (see printing
	#		  of results above). A quick semantical check of the propositionalize
	#		  operation yields that this is the correct result, contradicting
	#		  takiyama's claims. Overall, this should not matter, as constant
	#		  Parfactors behave neutral in Multiplication. Nevertheless it is
	#		  weird and slightly concerning.
	print(expected == result) # True

def test_simple_counting_convert():
	pop = []
	for i in range(16):
		pop.append(Constant('lot' + str(i+1)))
	Lot = Variable('Lot', Population(pop))
	lot1 = Constant('lot1')
	Lot_lot1 = InequalityConstraint(Lot, lot1)

	rain = Relation('rain')
	wet_grass = Relation('wet_grass', [Lot])
	formula = CountingFormula(Lot, {Lot_lot1}, wet_grass)

	f1 = [D('0.8'), D('0.2')]
	f5 = [D('2.0'), D('3.0'), D('5.0'), D('7.0')]
	f6 = [D('0.32'), D('0.936')]
	f7 = [D('32768'), D('49152'), D('73728'), D('110592'), D('165888'), D('248832'), D('373248'),
		  D('559872'), D('839808'), D('1259712'), D('1889568'), D('2834352'), D('4251528'), D('6377292'), 
		  D('9565938'), D('14348907'), D('30517578125.0'), D('42724609375.0'), D('59814453125.0'), 
		  D('83740234375.0'), D('117236328125.0'), D('164130859375.0'), D('229783203125.0'),
		  D('321696484375.0'), D('450375078125.0'), D('630525109375.0'), D('882735153125.0'),
		  D('1235829214375.0'), D('1730160900125.0'), D('2422225260175.0'), 
		  D('3391115364245.0'), D('4747561509943.0')]

	g1 = StdParfactorBuilder().addVariables([rain]).addValues(f1).build()
	g9 = StdParfactorBuilder().addVariables([rain, wet_grass]).addConstraints({Lot_lot1}).addValues(f5).build()
	g11 = StdParfactorBuilder().addVariables([rain]).addValues(f6).build()
	g12 = StdParfactorBuilder().addVariables([rain, formula]).addValues(f7).build()

	input1 = StdMarginalBuilder().setParfactors([g1, g9, g11]).build()
	counting_convert = CountingConvert(input1, g9, Lot)

	result = counting_convert.run()
	expected = StdMarginalBuilder().setParfactors([g1, g11, g12]).build()

	print(expected == result) # True

def test_global_sum_out():
	pop = []
	for i in range(10):
		pop.append(Constant('lot' + str(i+1)))
	Lot = Variable('Lot', Population(pop))
	lot1 = Constant('lot1')

	Lot_lot1 = InequalityConstraint(Lot, lot1)

	rain = Relation('rain')
	another_rain = Relation('another_rain')
	sprinkler = Relation('sprinkler', [Lot])
	sprinkler_lot1 = Relation('sprinkler', [lot1])
	wet_grass = Relation('wet_grass', [Lot])
	wet_grass_lot1 = Relation('wet_grass', [lot1])

	f1 = [D('1'), D('2')]
	f2 = [D('2'), D('3')]
	f3 = [D('1'), D('2'), D('3'), D('4'), D('5'), D('6'), D('7'), D('8')]
	f6 = [D('3'), D('5')]
	f7 = [D('2'), D('3'), D('5'), D('7')]
	f8 = [D('56'), D('79')]
	f9 = [D('11'), D('16'), D('31'), D('36')]

	g1 = StdParfactorBuilder().addVariables([rain]).addValues(f1).build()
	g4 = StdParfactorBuilder().addVariables([wet_grass_lot1]).addValues(f1).build()
	g5 = StdParfactorBuilder().addVariables([rain, sprinkler_lot1, wet_grass_lot1]).addValues(f3).build()
	g6 = StdParfactorBuilder().addVariables([rain, sprinkler, wet_grass]).addValues(f3).addConstraints({Lot_lot1}).build()
	g7 = StdParfactorBuilder().addVariables([sprinkler_lot1]).addValues(f2).build()
	g8 = StdParfactorBuilder().addVariables([sprinkler]).addValues(f2).addConstraints({Lot_lot1}).build()
	g9 = StdParfactorBuilder().addVariables([rain, wet_grass]).addValues(f9).addConstraints({Lot_lot1}).build()
	g10 = StdParfactorBuilder().addVariables([rain, wet_grass_lot1]).addValues(f9).build()
	g11 = StdParfactorBuilder().addVariables([rain]).addValues(f6).build()
	g12 = StdParfactorBuilder().addVariables([rain, another_rain]).addValues(f7).build()
	g13 = StdParfactorBuilder().addVariables([another_rain]).addValues(f8).build()

	# Constraint simplified
	input1 = StdMarginalBuilder(2).setParfactors([g6, g8]).build()

	constraints = {Lot_lot1}
	eliminables = RandomVariableSet(sprinkler, constraints)
	global_sum_out = GlobalSumOut(input1, eliminables)
	result = global_sum_out.run()

	expected = StdMarginalBuilder(5).setParfactors([g9]).build()

	print(expected == result) # True

	# No Constraints
	input1 = StdMarginalBuilder(5).setParfactors([g1, g4, g5, g7, g9]).build()

	constraints = {}
	eliminables = RandomVariableSet(sprinkler_lot1, constraints)
	global_sum_out = GlobalSumOut(input1, eliminables)
	result = global_sum_out.run()

	expected = StdMarginalBuilder(4).setParfactors([g1, g4, g9, g10]).build()

	print(expected == result) # True