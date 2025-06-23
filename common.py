from modules import *
'''
A second cfove utils, to avoid source files
getting too big.

	Classes
	-------
		Builder
		Counter
		Distribution
		DoubleDispatchParfactor
		Marginal
		MultiplicationChecker
		Parfactor
		ParfactorDecorator
		ParfactorVisitor
		Replaceable
		Scanner
		Simplifier
		SplitResult
		Splitter
		StdDistribution
		StdMarginal
		StdMarginalBuilder
		StdParfactor
		StdParfactorBuilder
		VisitableParfactor
'''

# TODO: test: Counter, Simplifier, MultiplicationChecker

###########
# Builder #
###########

class Builder:
	'''
	Abstract class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Builder class
		'''
		pass

	def build(self):
		'''
		Returns an instance of the object being built.

			Returns
			-------
				:
					an instance of the object being built
		'''
		pass

###############
# Replaceable #
###############

class Replaceable:
	'''
	Represents object over which
	Substitution is applicable.

	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Replaceable class.
		'''
		pass

	def applySubstitution(self, s):
		'''
		Applies the specified Substitution over the object.

			Parameters
			----------
				s : Substitution
					the substitution to apply

			Returns
			-------
				:
					the object that results from the application
					of the specified substitution to this object
		'''
		pass

############
# Marginal #
############

class Marginal:
	'''
	Represents the marginal Sum_&Gamma J(&Phi), where &Gamma is
	a set of Random variables and J(&Phi) is a Distribution.

	Abstract class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Marginal class
		'''
		pass

	def getDistribution(self):
		'''
		Returns the distribution of this marginal (before summing out
		the eliminable variables).

			Returns
			-------
				: Distribution
					the distribution of this marginal
		'''
		pass

	def getEliminables(self):
		'''
		Returns the set of PRVs to eliminate.

			Returns
			-------
				: { RandomVariableSet }
					the set of PRVs to eliminate
		'''
		pass

	def getPreservable(self):
		'''
		Returns the set of variables to preserve.
		Complement of eliminables.

			Returns
			-------
				: { RandomVariableSet }
					the set of variables to preserve
		'''
		pass

	def isEmpty(self):
		'''
		Checks if this elimination is empty.

			Returns
			-------
				: bool
					True iff this elimination is empty
		'''
		pass

	def getSize(self):
		'''
		Returns the number of parfactors in the marginal.

			Returns
			-------
				: int
					the number of parfactors in the marginal
		'''
		pass

####################
# ParfactorVisitor #
####################

class ParfactorVisitor:
	'''
	Visitor for Parfactors

	This visitor is used to check whether it is possible
	to apply some operation between two parfactors without
	the need to know which types of parfactors are involved in
	the verification.

	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the ParfactorVisitor class
		'''
		pass

	def visit(self, p1, p2):
		'''
		Visits the specified Parfactors
			Paramters
			---------
				p1 : Parfactor
					the first Parfactor to visit
				p2 : Parfactor
					the second Parfactor to visit
		'''
		pass

##################################
# DoubleDispatchParfactorVisitor #
##################################

class DoubleDispatchParfactorVisitor:
	'''
	This visitor is used to check whether it is possible to apply some
	operation to a Parfactor without the need to know
	which types of parfactors are involved in the verification.

	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the DoubleDispatchParfactorVisitor class
		'''
		pass

	def visit(self, p):
		'''
		Visits the specified parfactor.

			Parameters
			----------
				p : Parfactor
					the Parfactor to visit
		'''
		pass

######################
# VisitableParfactor #
######################

class VisitableParfactor:
	'''
	Provides an interface to implement Visitor Pattern.

	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the VisitableParfactor class
		'''
		pass

	def accept(self, visitor, p):
		'''
		Accepts the specified visitor.

			Parameters
			----------
				visitor : ParfactorVisitor
					the visitor of this parfactor
				p : Parfactor
					the other parfactor to be visited by
					this visitor
		'''
		pass

#############
# Parfactor #
#############

class Parfactor(VisitableParfactor, Replaceable):
	'''
	Abstract class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Parfactor class
		'''
		pass

	# Getters

	def getConstraints(self):
		'''
		Returns the set of all constraints of this parfactor.

			Returns
			-------
				: { Constraint }
					the set of all constraints of this parfactor
		'''
		pass

	def getFactor(self):
		'''
		Returns the Factor assiciated with this parfactor.

			Returns
			-------
				: Factor
					the Factor assiciated with this parfactor
		'''
		pass

	def getVariables(self):
		'''
		Returns the set of variables in PRVs
		from this parfactor.

			Returns
			-------
				: { Variable }
					the set of variables in PRVs
					from this parfactor
		'''
		pass

	def getPrvs(self):
		'''
		Returns the set of all Prvs in this parfactor

			Returns
			-------
				: [ Prv ]
					a list of all Prvs in this parfactor
		'''
		pass

	def getSize(self):
		'''
		Returns the number of factors this parfactor represents.

			Returns
			-------
				: int
					the number of factors this parfactor represents
		'''
		pass

	def applySubstitution(self):
		pass

	def containsPrv(self, prv):
		'''
		Returns if the specified Prv exists in this parfactor.

			Paramters
			---------
				prv : Prv
					the prv to search

			Returns
			-------
				: bool
					True iff the specified Prv exists in this parfactor
		'''
		pass

	def isConstant(self):
		'''
		Checks if the parfactor is constant. (Neutral
		element in Multiplication).

			Returns
			-------
				: bool
					True iff this parfactor is constant
		'''
		pass

	def isCountable(self, lv):
		'''
		Checks if the specified variable can
		be counted in this parfactor.

		A variable is countable when it occusr free in
		only one PRV in the parfactor.

			Parameters
			----------
				lv : Variable
					the variable to test for countability

			Returns
			-------
				: bool
					True iff the specified variable can
					be counted in this parfactor
		'''
		pass

	def isExpandable(self, cf, s):
		'''
		Checks if the specified Prv can be
		expanded on the specified substitution.

			Parameters
			----------
				cf : Prv
					the PRV to be expanded
				s : Substitution
					the substitution to expand the 
					counting formula on.

			Returns
			-------
				: bool
					True iff he specified Prv can be
					expanded on the specified substitution
		'''
		pass

	def isMultipliable(self, other):
		'''
		Checks if this parfactor can be multiplied by the
		specified parfactor.

			Parameters
			----------
				other : the parfactor to multiply with

			Returns
			-------
				: bool
					True iff this parfactor can be multiplied by the
					specified parfactor
		'''
		pass

	def isSplittable(self, s):
		'''
		Checks if this parfactor can be split on the
		specified Substitution.

			Parameters
			----------
				s : Substitution
					the substitution to split this parfactor on

			Returns
			-------
				: bool
					True iff f this parfactor can be split on the
					specified Substitution
		'''
		pass

	def isEliminable(self, prv):
		'''
		Checks if the specified PRV can be eliminated from
		this parfactor.

			Parameters
			----------
				prv : Prv
					the PRV to eliminate

			Returns
			-------
				: bool
					True iff the specified PRV can be eliminated from
					this parfactor
		'''
		pass

	def countVariable(self, lv):
		'''
		Returns the result of eliminating the specified Variable form
		this parfactor.

			Parameters
			----------
				lv : Variable

			Returns
			-------
				: Parfactor
		'''
		pass
	
	def expand(self, cf, t):
		'''
		Returns the result of expanding the specified counting formula
		on the specified term in this parfactor.

			Parameters
			----------
				cf : Prv
					the counting formula to expand
				t : Term
					the term on which to expand the counting formula
					usually a constant

			Returns
			-------
				: Parfactor
					the result of expanding the specified counting formula
					on the specified term in this parfactor
		'''
		pass

	def multiply(self, other):
		'''
		Returns the result of mutiplying this parfactor
		with the specified other parfactor.

			Parameters
			----------
				other : Parfactor
					the parfactor to multiply by

			Returns
			-------
				: Parfactor
					the result of mutiplying this parfactor
					with the specified other parfactor
		'''
		pass

	def multiplicationHelper(self, other):
		'''
		Returns the result of mutiplying this parfactor
		with the specified other parfactor.

		This method is a complement to multiply
		when its caller is a StdParfactor.

			Parameters
			----------
				other : Parfactor
					the parfactor to multiply by

			Returns
			-------
				: Parfactor
					the result of mutiplying this parfactor
					with the specified other parfactor
		'''
		pass

	def splitOn(self, s):
		'''
		Splits this parfactor on the specified substitution.

			Parameters
			----------
				s : Substitution
					the substitution upon which this parfactor
					is to be split

			Returns
			-------
				: SplitResult

			Raises
			------
				IllegalArgumentError
					if this parfactor is not splittable on
					the specified substitution
		'''
		pass

	def sumOut(self, prv):
		'''
		Eliminates the specified Prv and returns the result.

			Parameters
			----------
				prv : Prv
					the PRV to eliminate

			Returns
			-------
				: Parfactor
					the result of eliminating the specified PRV
					from this parfactor.
		'''
		pass

	def simplifyVariables(self):
		pass

######################
# ParfactorDecorator #
######################

class ParfactorDecorator(Parfactor):
	'''
	Implements a decorator pattern for
	Parfactor.

	Abstract class
	'''

	# Constructors

	def __init__(self):
		'''
		Constructor of ParfactorDecorator
		'''
		pass

	def getVariables(self):
		pass

#######################
# StdParfactorBuilder #
#######################

class StdParfactorBuilder(Builder):
	'''
	Attributes
	----------
		restrictions : { Constraint }
		prvs : [ Prv ]
		values : [ Decimal ]
	'''

	# Constructor

	__slots__ = ('_restrictions', '_prvs', '_values')

	def __init__(self, p=None):
		'''
		Constructor of the StdParfactorBuilder class

			Parameters
			----------
				p : Parfactor
		'''
		self._restrictions = set()
		self._prvs = []
		self._values = []
		if p != None:
			self.addConstraints(p.getConstraints())
			self.addVariables(p.getPrvs())
			self.addValues(p.getFactor().getValues())
			# TODO: this does not feel correct
			self.setFactor(p.getFactor())

	def addConstraints(self, c):
		for restriction in c:
			self._restrictions.add(restriction)
		return self

	def addVariables(self, prvs):
		for prv in prvs:
			self._prvs.append(prv)
		return self

	def addValues(self, v):
		for value in v:
			self._values.append(value)
		return self

	def setFactor(self, f):
		self.addVariables(f.getVariables())
		self.addValues(f.getValues())
		return self

	def getFactor(self):
		'''
		Returns the factor defined by PRVs and values of this builder.

		If no values were set, returns a constant factor.

		If no variables were set, returns an empty factor.

			Returns
			-------
				the factor defined by PRVs and values of this builder
		'''
		variables = copy(self._prvs)
		# TODO: richtig?
		factor = ConstantFactor(variables)
		if not self._values:
			pass
		else:
			try:
				factor = StdFactor('', variables, self._values)
			except IllegalArgumentError:
				raise ValueError()
		return factor

	def build(self):
		return StdParfactor(copy(self._restrictions), self.getFactor())

	def buildRaw(self):
		return StdParfactor(copy(self._restrictions), self.getFactor())

################
# StdParfactor #
################

class StdParfactor(Parfactor):
	'''
		Attributes
		----------
			constraints : { Constraint }
			factor : Factor
	'''

	# Constructor

	__slots__ = ('_constraints', '_factor')

	def __init__(self, constraints, factor):
		'''
		Constructor of the StdParfactor class

			Parameters
			----------
				constraints : { Constraint }
					a set of constraints on variables
				factor : Factor
					a factor from the cartesian product
					of ranges of parameterized random variables
					to the reals
		'''
		self._constraints = copy(constraints)
		self._factor = StdFactor(factor.getName(), factor.getVariables(), factor.getValues())

	# Getters

	def getConstraints(self):
		return copy(self._constraints)

	def getFactor(self):
		return self._factor

	def getVariables(self):
		prvs = self._factor.getVariables()
		logical_variables = set()
		for prv in prvs:
			for lv in prv.getParameters():
				logical_variables.add(lv)
		return logical_variables

	def getPrvs(self):
		return self._factor.getVariables()

	def getSize(self):
		if not self.isInNormalForm():
			raise ValueError('Parfactor must be in normal form')
		size = 1
		to_visit = copy(self._constraints)
		for lv in self.getVariables():
			size = size * lv.numberOfIndividualsSatisfyingConstraints(to_visit)
			to_visit = self.removeConstraintsInvolvingTerm(to_visit, lv)
		return size

	def removeConstraintsInvolvingTerm(self, constraints, t):
		'''
		Returns the specified set of constraints with all constraints that
		contain the specified term removed.

			Parameters
			----------
				constraints : { Constraint }
					a set of constraints
				t : Term
					the term to search for in constraints

			Returns
			-------
				constraints : { Constraint }
					the specified set of constraints with all
					constraints that contain the specified term removed.
		'''
		all_constraints = copy(constraints)
		for c in all_constraints:
			if c.containsTerm(t):
				# TODO: Dangerous! But since all_constraints
				#		is a recent copy, it SHOULD be safe.
				constraints.remove(c)
		return constraints

	def applySubstitution(self, s):
		substituted_constraints = Sets.applySubstitution(s, self._constraints)
		substituted_factor = self._factor.applySubstitution(s)
		return StdParfactor(substituted_constraints, substituted_factor)

	def containsPrv(self, prv):
		# TODO: deviates from original
		#		again: extra careful
		return prv in self._factor.getVariables()

	def isConstant(self):
		has_no_constraints = not self._constraints
		has_constant_factor = self._factor.isConstant()
		return has_no_constraints and has_constant_factor

	def isCountable(self, lv):
		return self._factor.occurrences(lv) == 1

	def isExpandable(self, cf, s):

		if s.getSize() != 1:
			return False

		bind = s.asList()[0]
		replaced = bind.getFirstTerm()
		t = bind.getSecondTerm()

		is_counting_formula = not cf.getBoundVariable().isEmpty()
		belongs_here = cf in self._factor.getVariables()
		is_in_normal_form = self.isInNormalForm()
		is_countable = not self.constraintsContainTerm(cf.getConstraints(), t)
		is_orthogonal = self.isOrthogonal(cf, t)
		replaces_bound = replaced == cf.getBoundVariable()
		is_constant_from_bound = False
		if t.isConstant():
			is_constant_from_bound = cf.getBoundVariable().getPopulation().containsIndividual(t)

		return is_counting_formula and belongs_here and is_in_normal_form and is_countable and is_orthogonal and replaces_bound and is_constant_from_bound

	def isInNormalForm(self):
		'''
		Checks if this parfactor is in normal form.

		A parfactor is in normal form if, for each inequality constraint
		(X != Y) in C, we have epsilon_X^C - {Y} = epsilon_Y^C - {X}.
		X and Y are variables.

			Returns
			-------
				: bool
					True iff this parfactor is in normal form
		'''
		for c in self._constraints:
			if c.getFirstTerm().isVariable() and c.getSecondTerm().isVariable():
				x = c.getFirstTerm()
				y = c.getSecondTerm()
				ex = x.excludedSet(self._constraints)
				ey = y.excludedSet(self._constraints)
				# TODO: deviates from original
				#		being extra careful
				exc = copy(ex)
				eyc = copy(ey)
				for z in exc:
					if z == y:
						ex.remove(z)
				for z in eyc:
					if z == x:
						ey.remove(z)
				if ex != ey:
					return False
		return True

	def constraintsContainTerm(self, constraints, t):
		'''
		Checks if the specified term is in at least one of
		the constraints from the specified set.

			Parameters
			----------
				constraints : { Constraint }
					a set of constraints
				t : Term
					the term to search in constraints from the set

			Returns
			-------
				: bool
					True iff he specified term is in at least one of
					the constraints from the specified set
		'''
		for c in constraints:
			if c.containsTerm(t):
				return True
		return False

	def isOrthogonal(self, cf, t):
		'''
		Checks if the specified term is orthogonal to all
		constraints in the specified counting formula.

		A term t is orthogonal to a constraint in a counting formula
		when, for each variable Y that appears in constraints C_A,
		the constraint Y != t appears in C_i (constraint from this parfactor).

			Parameters
			----------
				cf : Prv
					a counting formula #_A:C_A[f(...,A,...)]
				t : Term
					the term to check

			Returns
			-------
				: bool
					True iff the specified term is orthogonal to all
					constraints in the specified counting formula
		'''
		for y in cf.getBoundVariable().excludedSet(cf.getConstraints()):
			if y.isVariable():
				ey = y.excludedSet(self._constraints)
				if t not in ey:
					return False
		return True

	def isMultipliable(self, other):
		parfactors = MultiplicationChecker()
		self.accept(parfactors, other)
		return parfactors.areMultipliable()

	def isSplittable(self, s):
		is_splittable = False
		if s.getSize() != 1:
			is_splittable = False
		else:
			b = s.getFirstBinding()
			x = b.getFirstTerm()
			t = b.getSecondTerm()

			# TODO: Deviates from original
			#		being extra careful
			is_appliable = x in self.getVariables()
			is_not_in_constraints = not self.constraintsContainTerm(self._constraints, t)
			is_valid_substitution = b.isValid()
			is_logical_variable = True
			if t.isVariable():
				# TODO: Deviates from original
				#		being extra careful
				is_logical_variable = t in self.getVariables()

			is_splittable = is_appliable and is_not_in_constraints and is_valid_substitution and is_logical_variable
		return is_splittable

	def isEliminable(self, prv):
		lvs = set()
		for v in self._factor.getVariables():
			for t in v.getParameters():
				lvs.add(t)
		# TODO: Deviates from original
		#		being extra careful
		return lvs.issubset(prv.getParameters())

	def countVariable(self, lv): 
		if not self.isCountable(lv):
			raise IllegalArgumentError()
		return Counter(self).countVariable(lv)

	def expand(self, cf, t):
		cf_index = self._factor.getVariables().index(cf)
		pop = cf.getBoundVariable().individualsSatisfyingConstraints(cf.getConstraints())
		if pop.getSize() == 1:
			expanded_prv = cf.toStdPrv()
			prvs = Lists.replace(self.getPrvs(), cf, expanded_prv)
			expanded = StdParfactorBuilder().addConstraints(self.getConstraints()).addVariables(prvs).addValues(self._factor.getValues()).build()
			return expanded

		vars1 = self.getExpandedVariables(cf, t)
		new_structure = ConstantFactor(vars1)
		taken_out = vars1[cf_index + 1]
		#new_size = self._factor.getSize() * len(taken_out.getCodomain())
		vals = []

		for pair in new_structure:
			combined = self.combine(pair, cf_index, cf_index + 1)
			vals.append(self._factor.getValueOfTuple(combined))

		vars1[cf_index] = vars1[cf_index].simplify()

		expanded = StdParfactorBuilder().addConstraints(self._constraints).addVariables(vars1).addValues(vals).build()

		return expanded

	def getExpandedVariables(self, cf, t):
		'''
		Creates the new set of PRVS for expand(Prv, Term).

		Let c = #_A:CA [f(...,A,...)] and
			c' = #_A:(CA U {A != t}) [f(...,A,...)]

		Then V' = V - {c} U {c'}

			Parameters
			----------
				cf : Prv
					the counting formula to expand
				t : Term
					the term to be taken out from the counting formula

			Returns
			-------
				new set of PRVS for expand(Prv, Term)
		'''
		vars1 = copy(self._factor.getVariables())
		cf_index = vars1.index(cf)

		expanded = cf.removeTerm(t)
		taken_out = cf.takeOutTerm(t)

		vars1[cf_index] = expanded
		vars1.insert(cf_index + 1, taken_out)

		return vars1

	def combine(self, t, i, j):
		'''
		Returns the combination of elements at the specified indexes in the
		specified tuple. The combined element is put in position i
		and position j is removed.

			Parameters
			----------
				t : Tuple
					the tuple to manipulate
				i : int
					the index of the counting formula
				j : int
					the index of a 'taken out' PRV

			Returns
			-------
				pair : Tuple
					The combination of elements at the specified indexes
					in the specified tuple. 
		'''
		pair = Tuple(copy(t._values))
		new_histogram = t.getElementAt(i).combine(t.getElementAt(j))
		pair = pair.setElementAt(i, new_histogram)
		pair = pair.removeElementAt(j)

		return pair

	def multiply(self, other):
		return other.multiplicationHelper(self)

	def multiplicationHelper(self, other):
		union = Sets.union(other.getConstraints(), self._constraints)
		fixfj = other.getFactor().multiply(self._factor)
		g = StdParfactorBuilder().addConstraints(union).addVariables(fixfj.getVariables()).addValues(fixfj.getValues()).build()

		gi_size = other.getSize()
		gj_size = self.getSize()
		g_size = g.getSize()

		fi = other.getFactor().pow(gi_size, g_size)
		fj = self._factor.pow(gj_size, g_size)
		fixfj_corrected = fi.multiply(fj)

		product = StdParfactorBuilder().addConstraints(union).addVariables(fixfj_corrected.getVariables()).addValues(fixfj_corrected.getValues()).build()

		return product

	def splitOn(self, s):
		return Splitter(self, s).split(self)

	def sumOut(self, prv):
		sum_out = self._factor.sumOut(prv)
		g = StdParfactorBuilder().addConstraints(self._constraints).setFactor(sum_out).build()

		g_size = g.getSize()
		this_size = self.getSize()

		corrected = sum_out.pow(this_size, g_size)
		summed_out = StdParfactorBuilder().addConstraints(self._constraints).setFactor(corrected).build()

		return summed_out

	def simplifyVariables(self):
		parfactor = Simplifier(self)
		return parfactor.simplify()

	def accept(self, visitor, p):
		# Only the StdParfactor version is implemented
		# obviously!
		visitor.visit(self, p)

	# Equality, Hash, String

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, StdParfactor):
			return False
		return self._constraints == other._constraints and self._factor == other._factor

	def __hash__(self):
		constraints = frozenset(self._constraints)
		return hash((constraints, self._factor))

	def __str__(self):
		result = ''
		for prv in self.getPrvs():
			result += str(prv)
			result += '\n'
			#if not prv.getBoundVariable().isEmpty():
			#	result += '#:' + prv.getBoundVariable().getName() + '['
			#result += (prv.getName() + '(')
			#for t in prv.getTerms():
			#	result += (t.getName() + ', ')
			#result = result.rstrip(', ')
			#if not prv.getBoundVariable().isEmpty():
			#	result += ')]\n'
			#else:
			#	result += (')\n')
		result += '\n'
		for c in self.getConstraints():
			result += str(c)
			result += '\n'
			#result += (c.getFirstTerm().getName() + ' != ' + c.getSecondTerm().getName() + '\n')
		result += '\n'
		for x in self._factor.getValues():
			result += (str(x))
			result += '\n'
		return result

###########
# Scanner #
###########

class Scanner(ParfactorDecorator):
	'''
		Attributes
		----------
			p : Parfactor
	'''

	# Constructor

	__slots__ = ('_p')

	def __init__(self, p):
		'''
		Constructor of the Scanner class

			Parameters
			----------
				p : Parfactor
		'''
		self._p = p

	def getVariables(self):
		# Remark: Like elsewhere, we replaced sets
		# with lists here
		logical_variables = []
		# Warning getVariables() refers to PRVs here!
		for prv in self._p.getFactor().getVariables():
			for param in prv.getParameters():
				if param not in logical_variables:
					logical_variables.append(param)
			if not prv.getBoundVariable().isEmpty():
				if prv.getBoundVariable() not in logical_variables:
					logical_variables.append(prv.getBoundVariable())
		return logical_variables

	def getConstraints(self):
		return self._p.getConstraints()

	def getFactor(self):
		return self._p.getFactor()

	def getPrvs(self):
		return self._p.getPrvs()

	def applySubstitution(self, s):
		return self._p.applySubstitution(s)

	def containsPrv(self, prv):
		return self._p.contains(prv)

	def isConstant(self):
		return self._p.isConstant()

	def isCountable(self, lv):
		return self._p.isCountable(lv)

	def isExpandable(self, cf, s):
		return self._p.isExpandable(cf, s)

	def isMultipliable(self, other):
		return self._p.isMultipliable(other)

	def isSplittable(self, s):
		return self._p.isSplittable(s)

	def isEliminable(self, prv):
		return self._p.isEliminable(prv)

	def count(self, lv):
		return self._p.count(lv)

	def expand(self, cf, t):
		return self._p.expand(cf, t)

	def multiply(self, other):
		return self._p.multiply(other)

	def multiplicationHelper(self, other):
		return self._p.multiplicationHelper(other)

	def splitOn(self, s):
		return self._p.splitOn(s)

	def sumOut(self, prv):
		return self._p.sumOut(prv)

	def simplifyVariables(self):
		return self._p.simplifyVariables()

	def accept(self, visitor, p):
		self._p.accept(visitor, p)

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, Scanner):
			return False
		return self._p == other._p

	def __hash__(self):
		return hash(self._p)

#########################
# MultiplicationChecker #
#########################

class MultiplicationChecker(ParfactorVisitor):
	'''
	Encapsulates the algorithm to check for multiplication between
	Parfactors.

		Attributes
		----------
			areMultipliable : bool
	'''

	# Constructor

	__slots__ = ('_areMultipliable')

	def __init__(self):
		'''
		Constructor of the MultiplicationChecker class
		'''
		self._areMultipliable = False

	def visit(self, p1, p2):
		self._areMultipliable = True
		for prv1 in p1.getPrvs():
			for prv2 in p2.getPrvs():
				rvs1 = RandomVariableSet(prv1, Sets.union(prv1.getConstraints(), p1.getConstraints()))
				rvs2 = RandomVariableSet(prv2, Sets.union(prv2.getConstraints(), p2.getConstraints()))
				if not Prvs.areDisjoint(rvs1, rvs2) and rvs1 != rvs2:
					self._areMultipliable = False
					break

	def areMultipliable(self):
		'''
		Returns the status of a mulitplication check.

			Returns
			-------
				the status of a mulitplication check
		'''
		return self._areMultipliable

################
# Distribution #
################

class Distribution:
	'''
	A set of parfactors that represents a joint probability distribution.
	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Distribution class
		'''
		pass

	def addParfactor(self, p):
		'''
		Returns a distribution with the specified parfactor added.
		The order of the elements in the distribution may not be preserved.

			Parameters
			----------
				p : Parfactor
					the parfactor to add to this distribution

			Returns
			-------
				: Distribution
					a copy of this distribution with the specified parfactor added.
		'''
		pass

	def addAll(self, d):
		'''
		Returns a distribution that is the result of the union of the
		specified distribution and this distribution.
		Dublications are removed.

			Parameters
			----------
				d : Distribution
					the distribution to unify with this distribution
			
			Returns
			-------
				: Distribution
					the union of the specified distribution and this distribution
		'''
		pass

	def contains(self, o):
		'''
		Returns True iff this distribution contains the specified element.

			Parameters
			----------
				o :
					Element whose presence in this set is to be tested

			Returns
			-------
				: bool
					True iff this distribution contains the specified element
		'''
		pass

	def containsAll(self, d):
		'''
		Checks if this distribution contains all of the
		elements of the specified distribution.

			Parameters
			----------
				d : Distribution
					distribution to be checked

			Returns
			-------
				: bool
					True iff f this distribution contains all of the
					elements of the specified distribution		
		'''
		pass

	def isEmpty(self):
		'''
		Checks if this set contains no elements.

			Returns
			-------
				: bool
					True iff this set contains no elements
		'''
		pass

	def getSize(self):
		'''
		Returns the number of elements in this distribution.

			Returns
			-------
				: int
					the number of elements in this distribution
		'''
		pass

	def toSet(self):
		'''
		Returns a set containing all elements of this distribution.

			Returns
			-------
				: set
					a set containing all elements of this distribution
		'''
		pass

	def applySubstitution(self, s):
		'''
		Returns the result of applying the specified substituion to
		all parfactors in this distribution.

			Parameters
			----------
				s : Substitution
					the specified substituion

			Returns
			-------
				: Distribution
					the result of applying the specified substituion to
					all parfactors in this distribution
		'''
		pass

###################
# StdDistribution #
###################

def StdDistributionOf(c):
	'''
	Creates a distribution with the specified collection
	of Parfactors.

		c : iterable
			an iterable collection
			of Parfactors
	'''
	if None in c:
		raise TypeError()
	dist = set(c)
	return StdDistribution(dist)

class StdDistribution(Distribution):
	'''
	Standard implementation of Distribution

		Attributes
		----------
			pSet : { Parfactor }
	'''

	# Constructor

	__slots__ = ('_pSet')

	def __init__(self, p=set()):
		'''
		Constrictor of the StdDistribution class

			Parameters
			----------
				p : { Parfactor }
					a set of parfactors whose elements
					will compose this distribution.
		'''
		self._pSet = copy(p)

	# Iterator

	def __iter__(self):
		'''
		Iterates over pSet
		'''
		for p in self._pSet:
			yield(p)

	# static methods

	of = staticmethod(StdDistributionOf)

	def addAllToPSet(self, c):
		for p in c:
			self._pSet.add(p)

	def addParfactor(self, p):
		new_set = copy(self._pSet)
		if p not in new_set:
			new_set.add(p)
		return StdDistribution(new_set)

	def addAll(self, d):
		return StdDistribution(Sets.union(set(d), self._pSet))

	def contains(self, o):
		return o in self._pSet

	def containsAll(self, d):
		# TODO: Deviates from original
		for p in set(d):
			if p not in self._pSet:
				return False
		return True

	def isEmpty(self):
		return not self._pSet

	def getSize(self):
		return len(self._pSet)

	def toSet(self):
		return copy(self._pSet)

	def applySubstitution(self, s):
		return StdDistribution(Sets.applySubstitution(s, self._pSet))

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, StdDistribution):
			return False
		return self._pSet == other._pSet

	def __hash__(self):
		return hash(self._pSet)

######################
# StdMarginalBuilder #
######################

class StdMarginalBuilder(Builder):
	'''
		Attributes
		----------
			parfactors : [ Parfactor ]
			preservable : RandomVariableSet
	'''

	# Constructor

	__slots__ = ('_parfactors', '_preservable')

	def __init__(self, capacity=0):
		'''
		Constructor of the StdMarginalBuilder class

			Parameters
			----------
				capacity : int
					irrelevant for Python
					but may avoid some port inconsistencies
					# TODO: remove eventually
		'''
		self._parfactors = set()
		self._preservable = RandomVariableSet(Relation(''), set())

	def setParfactors(self, parfactors):
		'''
		Sets the distribution from this marginal to the
		specified parfactors.

			Parameters
			----------
				parfactors :
					an iterable object of parfactors

			Returns
			-------
				: StdMarginalBuilder
					the builder with the specified parfactors
		'''
		for p in parfactors:
			if p not in self._parfactors:
				self._parfactors.add(p)
		return self

	def addMarginal(self, marginal):
		'''
		Adds parfactors from the specified marginal to this builder.

			Parameters
			----------
				marginal : Marginal

			Returns
			-------
				: StdMarginalBuilder
					this builder with parfactors from the
					specified marginal
		'''
		for p in marginal.getDistribution():
			self._parfactors.add(p)
		self._preservable = marginal.getPreservable()
		return self

	def addParfactor(self, parfactor):
		'''
		Adds the specified parfactor to builder's distribution and
		returns the modified builder.

			Parameters
			----------
				parfactor : Parfactor
					the parfactor to add

			Returns
			-------
				: StdMarginalBuilder
					this builder with the specified parfactor added
		'''
		self._parfactors.add(parfactor)
		return self

	def setPreservable(self, rv_set):
		'''
		Adds the specified random variable se to this builder
		and returns the modified builder.

			Parameters
			----------
				rv_set : RandomVariableSet
					the random variable set to preserve
					(the sone that will not be eliminated)

			Returns
			-------
				: StdMarginalBuilder
					this builder with the specified random variable set added
		'''
		self._preservable = rv_set
		return self

	def replaceParfactor(self, old_one, new_one):
		'''
		Replaces the specified old parfactor with the specified new parfactor
		and returns the modified builder.
		If the parfactor does not exist, returns this builder unmodified.

			Parameters
			----------
				old_one : Parfactor
				new_one : Parfactor

			Returns
			-------
				this builder with the old parfactor replaced
				with the new one
		'''
		temp = copy(self._parfactors)	
		self._parfactors.remove(old_one)
		if temp != self._parfactors:
			self._parfactors.add(new_one)
		return self

	def removeParfactor(self, removeable):
		'''
		Removes the specified parfactor from the set of parfactors 
		in this builder. If the parfactor does not exist,
		returns this builder unmodified.

			Parameters
			----------
				removeable : Parfactor
					the parfactor to remove

			Returns
			-------
				: StdMarginalBuilder
					this builder with the specified parfactor removed
		'''
		temp = copy(self._parfactors)
		for p in temp:
			if p == removeable:
				self._parfactors.remove(p)
				break
		return self
	
	def getDistribution(self):
		'''
			Returns
			-------
				: Distribution
					the set of parfactors
					from this builder as a distribution
		'''
		return StdDistribution.of(self._parfactors)

	def build(self):
		return StdMarginal(self)

###############
# StdMarginal #
###############

class StdMarginal(Marginal):
	'''
		Attributes
		----------
			parfactors : Distribution
			preservable : RandomVariableSet
	'''

	# Constructor

	__slots__ = ('_parfactors', '_preservable')

	def __init__(self, builder):
		'''
		Constructor of the StdMarginal class

			Parameters
			----------
				builder : StdMarginalBuilder
		'''
		self._parfactors = builder.getDistribution()
		self._preservable = builder._preservable

	# Iterator

	def __iter__(self):
		'''
		Iterates over all parfactors.
		'''
		for p in self._parfactors:
			yield(p)

	# Getters

	def getEliminables(self):
		eliminables = set()
		for p in self._parfactors:
			for prv in p.getPrvs():
				if not Prvs.areDisjoint(prv, self._preservable.getPrv()):
					# If the PRV from the parfactor represents a set of random
					# variables that is not disjoint with the set of random
					# variables represented by 'preservable', then it cannot
					# be eliminated.

					# TODO: pass should be correct here
					#		but i will keep this comment just in case.
					pass
				else:
					s = RandomVariableSet(prv, p.getConstraints())
					if s not in eliminables:
						eliminables.add(s)

		return eliminables

	def getPreservable(self):
		return self._preservable

	def getDistribution(self):
		return StdDistribution.of(self._parfactors._pSet)

	def isEmpty(self):
		return self._parfactors.isEmpty()

	def getSize(self):
		return self._parfactors.getSize()

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, StdMarginal):
			return False
		return self._parfactors == other._parfactors and self._preservable == other._preservable

	def __hash__(self):
		return hash((self._parfactors, self._preservable))

###############
# SplitResult #
###############

class SplitResult:
	'''
	Represents the result of a split operation over Parfactors.

	Splitting a parfactor on a substitution always results in at least two
	other parfactors: The result of applying the substitution to the parfactor
	and the residue. The residue may or may not be composed of more than one parfactor.

		Attributes
		----------
			marginal : Marginal
			result : Parfactor
			residue : Distribution
	'''

	# Constructor

	__slots__ = ('_marginal', '_result', '_residue')

	def __init__(self, result, marginal):
		'''
		Constructor of the SplitResult class

			Parameters
			----------
				result : Parfactor
				marginal : Marginal
		'''
		self._result = result
		self._marginal = marginal
		self._residue = marginal.getDistribution()

	# Getters

	def getResult(self):
		'''
		Returns the result from the split.

			Returns
			-------
				result : Parfactor
					the result from the split
		'''
		return self._result

	def getResidue(self):
		'''
		Returns the residual parfactors.

			Returns
			-------
				residue : Distribution
					the residual parfactors
		'''
		return self._residue

	def getDistribution(self):
		'''
		Returns a distribution by the result and residual parfactors

			Returns
			-------
				distribution : Distribution
					a distribution by the result and residual parfactors
		'''
		return self._residue.addParfactor(self._result)

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, SplitResult):
			return False
		return self._result == other._result and self._marginal == other._marginal

	def __hash__(self):
		return hash((self._result, self._marginal))

############
# Splitter #
############

class Splitter:
	'''
	Encapsulates the splitting algorithm.

	Splitting a parfactor 'breaks' a Parfactor in two.

		Attributes
		----------
			splittable : Parfactor
			substitution : Substitution
	'''

	# Constructor

	__slots__ = ('_splittable', '_substitution')

	def __init__(self, splittable, substitution):
		'''
		Constructor of the Splitter class

			Parameters
			----------
				splittable : Parfactor
				substitution : Substitution
		'''
		self._splittable = splittable
		self._substitution = substitution

	def split(self, p):
		'''
		Splits a parfactor on the specified substitution.  The result of
		splitting StdParfactor g on substitution [X/t] will
		have two parfactors:
		g[X/t], the parfactor g after applying substitution [X/t];
		g' = <C U {X != t}, V, F>, the residual parfactor.
		'''
		# TODO: Careful: Contains one more argument p : Parfactor
		#		than original, as parfactor methods are not visible
		#		from Splitter.
		#		Might be removed later on.
		if not p.isSplittable(self._substitution):
			raise IllegalArgumentError('parfactor is not splittable on substitution')
		result = self._splittable.applySubstitution(self._substitution)
		residue = self.getResidue()
		# TODO: richtig?
		split = SplitResult(result, StdMarginalBuilder().setParfactors({residue}).build())
		return split

	def getResidue(self):
		'''
		Returns a Parfactor equal to this one with the specified constraint
		added.
		'''
		b = self._substitution.getFirstBinding()
		c = b.toInequalityConstraint()
		constraints = self._splittable.getConstraints()
		constraints.add(c)
		return StdParfactorBuilder().addConstraints(constraints).addVariables(self._splittable.getPrvs()).addValues(self._splittable.getFactor().getValues()).build()

###########
# Counter #
###########

class Counter:
	'''
	Encapsulates counting algorithm.

	Counting a free variable eliminates it from the parfactor
	using a counting formula.

		Attributes
		----------
			parfactor : Parfactor
				the parfactor being modifed
			counted : Prv
				PRV that contains the variable being counted
			bound : Variable
				variable being counted
			constraintsOnBound : { Constraint }
				subset of constraints that contains the bound variable
			countingFormula : Prv
				counting formula that replaces the PRV 'counted'
			countedIndex : int
				index of 'counted' in the list of PRVs
			values : [ Decimal ]
				values from the result
			variables : [ Prv ]
				variables in the result
			constraints : { Constraint }
				constraints in the result
	'''

	# Constructor

	__slots__ = ('_parfactor', '_counted', '_bound', '_constraintsOnBound', '_countingFormula', '_countedIndex', '_values', '_variables', '_constraints')

	def __init__(self, p):
		'''
		Constructor of the Counter class

			Parameters
			----------
				p : Parfactor
					the parfactor on which counting will take place
		'''
		self._parfactor = p
		self._counted = Relation('')
		self._bound = Variable('', Population())
		self._constraintsOnBound = set()
		self._countingFormula = Relation('')
		self._countedIndex = 0
		self._values = self._parfactor.getFactor().getValues()
		self._variables = self._parfactor.getPrvs()
		self._constraints = self._parfactor.getConstraints()

	def countVariable(self, lv):
		'''
		Counts the specified free variable in the parfactor.

			Parameters
			----------
				lv : Variable
					the variable to count

			Returns
			-------
				: Parfactor
					the result of the counting
		'''
		# TODO: make sure all of the below methods
		#		are implementedand correct
		self.setBound(lv)
		self.partitionOnBound()
		self.setPrvOnBound()
		self.setCountingFormulaOnBound()
		self.replaceCountedWithCountingFormula()
		self.setValues()
		return StdParfactorBuilder().addConstraints(self._constraints).addVariables(self._variables).addValues(self._values).build()

	def setBound(self, lv):
		'''
		Sets the free variable to be bound during count

			Parameters
			----------
				lv : Variable
		'''
		# TODO: is copy wise here?
		self._bound = Variable(lv.getName(), lv.getPopulation())

	def partitionOnBound(self):
		'''
		Splits constraints from this parfactor in two subsets,
		one that involves the bound variable
		and another that does not.
		'''
		for c in self._parfactor.getConstraints():
			if c.containsTerm(self._bound):
				self._constraintsOnBound.add(c)
		# TODO: Deviates from original
		self._constraints = Sets.difference(self._constraints, self._constraintsOnBound)

	def setPrvOnBound(self):
		'''
		Searches the PRV in parfactor being processed that contains
		the variable as a parameters. This method assumes that
		there is only one PRV satisfying this condition.
		'''
		self._counted = self._parfactor.getFactor().getVariableHavingTerm(self._bound)
		self._countedIndex = self._variables.index(self._counted)
	
	def setCountingFormulaOnBound(self):
		'''
		Builds the counting formula that will replace PRV on bound
		in the new parfactor.
		'''
		self._countingFormula = CountingFormula(self._bound, self._constraintsOnBound, self._counted)

	def replaceCountedWithCountingFormula(self):
		'''
		Replaces the old PRV being counted with its corresponding counting
		formula.
		'''
		self._variables[self._countedIndex] = self._countingFormula

	def setValues(self):
		'''
		Builds the list that defines the values in the new parfactor.
		'''
		# TODO: richtig? pruefen!
		self._values = []
		new_structure = ConstantFactor(self._variables)

		for pair in new_structure:
			value = D('1')
			for e in self._counted.getCodomain():
				old = pair.setElementAt(self._countedIndex, e)
				count = self._countingFormula.getCount(pair.getElementAt(self._countedIndex), e)
				value = value * (self._parfactor.getFactor().getValueOfTuple(old) ** D(count))
			self._values.append(value)

##############
# Simplifier #
##############

class Simplifier:
	'''
	Encapsulates the simplification algorithm.

	Simplifying a parfactor ist the process of replacing all variables
	constraint to a single individual with this individual.

		Attributes
		----------
			parfactor : Parfactor
			unaryConstraints : { Constraint }
			constraints : { Constraints }
			variables : [ Prv ]
				Careful! again variables refers to PRVs!
	'''

	# Constructor

	__slots__ = ('_parfactor', '_unaryConstraints', '_constraints', '_variables')

	def __init__(self, parfactor):
		'''
		Constructor of the Simplifier class

			Paramteters
			-----------
				parfactor : Parfactor
		'''
		self._parfactor = parfactor
		self._constraints = copy(parfactor.getConstraints())
		self._variables = copy(parfactor.getPrvs())
		self._unaryConstraints = self.getUnaryConstraints()

	def getUnaryConstraints(self):
		'''
		Returns the subset of unary constraints from the set of constraints
		'''
		unary = set()
		for constraint in self._constraints:
			if constraint.isUnary():
				if constraint not in unary:
					unary.add(constraint)
		return unary

	def simplify(self):
		'''
		Replaces all logical variables (Remark: not PRVs!)
		constrained to a single individual with this individual
		'''
		self.simplifyVariablesWithPopulationOne()

		queue = self.getVariablesInConstraints()

		while not not queue:
			# TODO: This does not work correctly in some corner cases
			logical_variable = queue.pop(0)
			#population_size = logical_variable.numberOfIndividualsSatisfyingConstraints(self._unaryConstraints)
			population_size = logical_variable.individualsSatisfyingConstraints(self._unaryConstraints).getSize()
			if population_size == 0:
				# TODO: Richig? nochmal pruefen.
				return StdParfactor(set(), ConstantFactor())
			elif population_size == 1:
				sub = self.getSubstitution(logical_variable)
				queue += list(self.variablesInBinaryConstraintsInvolving(logical_variable))
				self._constraints = Sets.applySubstitution(sub, self._constraints)
				self._unaryConstraints = self.getUnaryConstraints()
				self._variables = Lists.applySubstitution(sub, self._variables)
			else:
				pass
		result = StdParfactorBuilder().addConstraints(self._constraints).addVariables(self._variables).addValues(self._parfactor.getFactor().getValues()).buildRaw()
		return result

	def getVariablesInConstraints(self):
		'''
		Add logical variables from parfactor's constraints to a list.
		'''
		buffer = []
		for c in self._parfactor.getConstraints():
			for lv in c.getVariables():
				if lv not in buffer:
					buffer.append(lv)
		return buffer

	def getSubstitution(self, lv):
		'''
		When a logical variable is constrained to a single individual,
		builds the substituion that replaces the logical variable by this
		individual.
		'''
		lone_guy = next(iter(lv.individualsSatisfyingConstraints(self._unaryConstraints)))
		bind = Binding(lv, lone_guy)
		return Substitution([bind])

	def variablesInBinaryConstraintsInvolving(self, lv):
		'''
		Returns the set of logical variables belonging to binary constraints
		that involve the specified logical variable.
		'''
		binary_constraints = copy(self._constraints)
		binary_constraints = Sets.difference(binary_constraints, self._unaryConstraints)

		other_variables = set()
		for binary in binary_constraints:
			if binary.containsTerm(lv) and binary.getFirstTerm() == lv:
				other_variables.add(binary.getSecondTerm())
			elif binary.containsTerm(lv) and binary.getSecondTerm() == lv:
				other_variables.add(binary.getFirstTerm())
		return other_variables

	def simplifyVariablesWithPopulationOne(self):
		p = Scanner(self._parfactor)
		bind_list = []
		for v in p.getVariables():
			if v.getPopulation().getSize() == 1:
				c = v.getPopulation().getIndividualAt(0)
				bind = Binding(v, c)
				bind_list.append(bind)
		substitution = Substitution(bind_list)
		self._variables = Lists.applySubstitution(substitution, self._variables)
