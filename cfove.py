from modules import *

'''
This module implements all steps of the C-FOVE algorithm.

	Classes
	-------
		CFOVE
		CountingConvert
		ImpossibleOperation
		FinalMultiplication
		FullExpand
		GlobalSumOut
		MacroOperation
		MutableQueue
		MutableQueueIterator
		Propositionalize
		Shatter
'''

##################
# MacroOperation #
##################

class MacroOperation:
	'''
	Represents a MacroOperation in C-FOVE

	Abstract Class
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the MacroOperation class
		'''
		pass

	def run(self):
		'''
		Executes the macro-Operation-

			Returns
			-------
				: Marginal
					the resulting marginal after applying
					the macro-operation.
		'''
		pass

	def cost(self):
		'''
		Returns this operation cost.
		The cost is the size of parfactors it creates.

			Returns
			-------
				: int
					This operation cost
		'''
		pass

	def numberOfRandomVariablesEliminated(self):
		'''
		Returns the number of random variables (i.e. PRVs) that are
		eliminated if this operation is executed.

			Returns
			-------
				: int
					the number of random variables that are
					eliminated if this operation is executed
		'''
		pass

###################
# CountingConvert #
###################

class CountingConvert(MacroOperation):
	'''
	This operation eliminates a free variable from a Parfactor.
	This is done using the Counting operation.

		Attributes
		----------
			marginal : Marginal
				Marginal that contains the parfactor being counted
			countableParfactor : Parfactor
				Parfactor being counted
			freeVariable : Variable
				Variable being counted
			prvToCount : Prv
				PRV that contains the free Variable
	'''

	# Constructor

	__slots__ = ('_marginal', '_countableParfactor', '_freeVariable', '_prvToCount')

	def __init__(self, marginal, countable, freeVariable):
		'''
		Constructor of the CountingConvert Classes

			Parameters
			----------
				marginal : Marginal
				countable : Parfactor
				freeVariable : Variable
		'''
		self._marginal = marginal
		self._countableParfactor = countable
		self._freeVariable = freeVariable
		self._prvToCount = countable.getFactor().getVariableHavingTerm(freeVariable)

	def run(self):
		result_builder = StdMarginalBuilder()
		result_builder.addMarginal(self._marginal).removeParfactor(self._countableParfactor)

		counted = self._countableParfactor.countVariable(self._freeVariable)
		result_builder.addParfactor(counted)

		return result_builder.build()

	def cost(self):
		if self._countableParfactor.isCountable(self._freeVariable):
			f = self._countableParfactor.getFactor().getSize()
			r = len(self._prvToCount.getCodomain())
			h = self.getNumberOfHistograms()
			return int(f / r * h)
		else:
			return 2147483647

	def getNumberOfHistograms(self):
		'''
		Returns the number of histograms created when converting the
		standard PRV to a counting formula.
		'''
		domain = self._freeVariable.numberOfIndividualsSatisfyingConstraints(self._countableParfactor.getConstraints())
		range1 = len(self._prvToCount.getCodomain()) - 1
		number_of_histograms = int(MathUtils.combination(domain + range1, range1))
		return number_of_histograms

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Counting Convert'

##############
# FullExpand #
##############

class FullExpand(MacroOperation):
	'''
	This operation represents the expandsion of a counting formula
	for all individuals from its bound variable	satisfying its constraints.

	After all expansions, the Shatter macro operation is invoked
	to guarantee that all PRVs represent equal or disjoint sets of random variables.

		Attributes
		----------
			marginal : Marginal
				the maringal in which the parfactor to be expanded is containes
			expandableParfactor : Parfactor
				the parfactor to be fully expanded
			expandableVariable : Prv
				the counting formula that will be expanded
	'''

	# Constructor

	__slots__ = ('_marginal', '_expandableParfactor', '_expandableVariable')

	def __init__(self, marginal, expandable, countingFormula):
		'''
		Constructor of the FullExpand class

			Parameters
			----------
				marginal : Marginal
				expandable : Parfactor
				countingFormula : Prv
		'''
		self._marginal = marginal
		self._expandableParfactor = expandable
		self._expandableVariable = countingFormula

	def run(self):
		expanded = self.fullExpand()
		result_builder = StdMarginalBuilder()
		result_builder.addMarginal(self._marginal).replaceParfactor(self._expandableParfactor, expanded)
		result = Shatter(result_builder.build()).run()
		return result

	def fullExpand(self):
		'''
		Returns the result of fully expanding the expandable parfactor on
		individuals from expandable variable.

			Raises
			------
				ValueError
		'''
		to_expand = self._expandableParfactor
		expandable = self._expandableVariable

		prv_index = to_expand.getFactor().getVariables().index(expandable)

		if prv_index == -1:
			raise ValueError()

		population = self.getBoundedIndividuals()

		for individual in population:
			expandable = to_expand.getFactor().getVariables()[prv_index]
			bound = expandable.getBoundVariable()
			b = Binding(bound, individual)
			s = Substitution([b])
			if to_expand.isExpandable(expandable, s):
				to_expand = to_expand.expand(expandable, individual)

		return to_expand

	def getBoundedIndividuals(self):
		'''
		Returns the number of individuals from the bounded logical variable
		satisfying counting formula's constraints
		'''
		return self._expandableVariable.getBoundVariable().individualsSatisfyingConstraints(self._expandableVariable.getConstraints())

	def cost(self):
		cost = 2147483647
		if self.isPossible():
			factor = self._expandableParfactor.getFactor().getSize()
			counting_formula = len(self._expandableVariable.getCodomain())
			prv = self._expandableVariable.getPrvCodomainSize()
			domain = self.getBoundedIndividuals().getSize()

			res_size = int(factor / counting_formula) * (prv ** domain)
			# TODO: richtig?
			if res_size < 2147483647 - 1:
				cost = res_size
			else:
				cost = 2147483647 - 1
		return cost

	def isPossible(self):
		'''
			Returns
			-------
				: bool
		'''
		is_possible = False
		population = self.getBoundedIndividuals()
		if population.getSize() != 0:
			someone = population.getIndividualAt(0)
			bound = self._expandableVariable.getBoundVariable()
			b = Binding(bound, someone)
			s = Substitution([b])
			is_possible = self._expandableParfactor.isExpandable(self._expandableVariable, s)
		return is_possible

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Full Expand'

################
# GlobalSumOut #
################

class GlobalSumOut(MacroOperation):
	'''
		Attributes
		----------
			marginal : Marginal
				the marginal where elimination will take place
			eliminables : RandomVariableSet
				the set of random variables to eliminate
			cost : int
			isPossible : bool
	'''

	# Constructor

	__slots__ = ('_marginal', '_eliminables', '_cost', '_isPossible')

	def __init__(self, marginal, eliminables):
		'''
		Constructor of the GlobalSumOut class

			Parameters
			----------
				marginal : Marginal
				eliminables : RandomVariableSet
		'''
		#for p in marginal:
		#	print(p.toString() + '\n---------------\n')
		#print(eliminables._prv.toString() + '\n---------------\n')
		#print(eliminables._constraints)
		self._marginal = marginal
		self._eliminables = eliminables
		self.calculateFeasibility()

	def calculateFeasibility(self):
		'''
		Calculates the feasibility of this operation. This operation is possible
		if all parfactors involving the variables being eliminated can be
		multiplied and those variables can be summed out from the product.
		'''
		self.setCost(2147483647)

		elim = RandomVariableSet(self._eliminables.getPrv().getCanonicalForm(), self._eliminables.getConstraints())
		if Prvs.areDisjoint(elim, self._marginal.getPreservable()):

			# TODO: richtig?
			queue = list(self._marginal.getDistribution().toSet())
			result = StdParfactorBuilder().build()
			for candidate in queue:
				if self.containsEliminable(candidate):
					if result.isMultipliable(candidate):
						result = result.multiply(candidate)
					else:
						return

			if result.isEliminable(self._eliminables):
				f = result.getFactor().getSize()
				v = len(self._eliminables.getCodomain())
				self.setCost(int(f / v))

	def setCost(self, c):
		'''
		Updates cost and isPossible.
	
			Parameters
			----------
				c : int
		'''
		if c < 2147483647:
			self._cost = c
			self._isPossible = True
		else:
			self._cost = 2147483647
			self._isPossible = False

	def containsEliminable(self, candidate):
		'''
		Returns True if the specified parfactor contains the set
		of variables to eliminate.
		'''
		elim = RandomVariableSet(self._eliminables.getPrv().getCanonicalForm(), Sets.union(self._eliminables.getPrv().getConstraints(), self._eliminables.getConstraints()))
		variables = candidate.getPrvs()
		for prv in variables:
			rvs = RandomVariableSet(prv.getCanonicalForm(), candidate.getConstraints())
			if rvs == elim:
				return True
		return False

	def run(self):
		if self._isPossible:
			result = StdParfactorBuilder().build()

			marginal_result = StdMarginalBuilder()
			marginal_result.addMarginal(self._marginal)

			for candidate in self._marginal:
				if self.containsEliminable(candidate):
					result = result.multiply(candidate)
					marginal_result.removeParfactor(candidate)

			try:
				result = result.sumOut(self._eliminables.getPrv())
			except IllegalArgumentError:
				# TODO: richtig?
				result = StdParfactorBuilder().build()

			if not result.isConstant():
				marginal_result.addParfactor(result)

			return marginal_result.build()

		else:
			return self._marginal

	def cost(self):
		return self._cost

	def numberOfRandomVariablesEliminated(self):
		if self.cost() == 2147483647:
			return 0
		else:
			return self._eliminables.getPrv().getGroundSetSize(self._eliminables.getConstraints())

	def __str__(self):
		return 'Global Sum Out'

####################
# Propositionalize #
####################

class Propositionalize(MacroOperation):
	'''
	This operation executes a split on a parfactor for every
	constant in the population of a free variable that appears in this
	parfactor.

	After all the splits the Shatter macro operation is invoked to
	guarantee that all PRVs represent equal or dijoint sets of random variables.

		Attributes
		----------
			marginal : Marginal
			propositionalizable : Parfactor
			freeVariable : Variable
	'''

	# Constructor

	__slots__ = ('_marginal', '_propositionalizable', '_freeVariable')

	def __init__(self, marginal, propositionalizable, freeVariable):
		'''
		Constructor of the Propositionalize class

			Parameters
			----------
				marginal : Marginal
				propositionalizable : Parfactor
				freeVariable : Variable
		'''
		self._marginal = marginal
		self._propositionalizable = propositionalizable
		self._freeVariable = freeVariable

	def run(self):
		splittable = self._propositionalizable

		result_builder = StdMarginalBuilder()
		result_builder.addMarginal(self._marginal).removeParfactor(self._propositionalizable)

		population = self.getIndividuals()
		for individual in population:
			sub = Substitution([Binding(self._freeVariable, individual)])
			if splittable.isSplittable(sub):
				split_result = splittable.splitOn(sub)
				result_builder.addParfactor(split_result.getResult())
				if split_result.getResidue().getSize() == 1:
					splittable = next(iter(split_result.getResidue()))
				else:
					raise ValueError('Split result has more than 1 residue!')
			else:
				result_builder.addParfactor(splittable)

		result = Shatter(result_builder.build()).run()
		return result

	def getIndividuals(self):
		'''
		Returns a free variable population that satisfies constraints
		from the parfactor being propositionalized.
		'''
		return self._freeVariable.individualsSatisfyingConstraints(self._propositionalizable.getConstraints())

	def cost(self):
		return 2147483647 - 1

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Propositionalize'

########################
# MutableQueueIterator #
########################

class MutableQueueIterator:
	'''
	I have not figured out, how this iterator would be
	integrated into MutableQueue the 'Python way' yet.
	So until then, this will have to do. It should work.

		Attributes
		----------
			i : int
			j : int
	'''

	# Constructor

	__slots__ = ('_i', '_j')

	def __init__(self):
		'''
		Cosntructor of the MutableQueueIterator class
		'''
		self.reset()

	def reset(self):
		self._i = -1
		self._j = 0

	def hasNext(self, queue):
		'''
			Parameters
			----------
				queue : list

			Returns
			-------
				: bool
		'''
		return (self._i < len(queue) - 2) or (self._j < len(queue) - 1)

	def next(self, queue):
		'''
			Parameters
			---------- 
				queue : list

			Returns
			-------
				: Tuple
		'''
		if self._i == -1 and self._j == 0:
			self._i += 1
			self._j += 1
		else:
			self._j += 1
			if self._j == len(queue):
				self._i += 1
				if self._i != len(queue) - 1:
					self._j = self._i + 1

		t = Tuple([queue[self._i], queue[self._j]])

		return t

	def remove(self):
		raise NotImplementedError()

################
# MutableQueue #
################

class MutableQueue:
	'''
		Attributes
		----------
			queue : list
				the queue
			iterator : MutableQueueIterator
				iterator that returns pairs of parfactor from the queue
	'''

	# Constructor

	__slots__ = ('_queue', '_iterator')

	def __init__(self, c):
		'''
		Constructor of the MutableQueue class

			Parameters
			----------
				c :
					an iterable object

			Raises
			------
				IllegalArgumentError
					if length of c is less than 2 
		'''
		if len(c) < 2:
			raise IllegalArgumentError()
		self._queue = list(c)
		self._iterator = MutableQueueIterator()

	def add(self, c):
		'''
			Parameters
			----------
				c :
					an iterable object
		'''
		for x in c:
			self._queue.append(x)
			self._iterator.reset()

	def remove(self, t):
		'''
		Tries to remove the elements in the specified tuple from the queue.
		Elements that are not in the queue are not removed.

			Paramteres
			----------
				t : Tuple
		'''
		removed_item = False
		for i in range(t.getSize()):
			# TODO: richtig?
			try:
				for o in self._queue:
					if o == t.getElementAt(i):
						self._queue.remove(o)
						removed_item = True
			except ValueError:
				pass

		if removed_item:
			self._iterator.reset()

	def iterator(self):
		return self._iterator

	def toSet(self):
		# Remark: Despite the name, we make this
		# return a list and not a set..
		return copy(self._queue)

###########
# Shatter #
###########

class Shatter(MacroOperation):
	'''
	This operation makes all the necessary splits and expansions to
	guarantee that the sets of random variables represented by PRVs
	in each parfactor of the given set are equal or disjoint.

	This operation is used before multiplication and elimination
	on parfactors.

		Attributes
		----------
			marginal : Marginal
	'''

	# Constructor

	__slots__ = ('_marginal')

	def __init__(self, marginal):
		'''
		Constructor of the Shatter class

			Parameters
			----------
				marginal : Marginal
		'''
		self._marginal = marginal

	def run(self):
		marginal_size = self._marginal.getDistribution().getSize()
		if marginal_size < 2:
			return self._marginal
		self._marginal = self.simplifyVariables(self._marginal)
		self.renameAllVariables()

		queue = MutableQueue(self._marginal.getDistribution().toSet())
		# TODO: richtig?
		it = queue.iterator()
		while it.hasNext(queue._queue):
			pair = it.next(queue._queue)
			unified_set = self.unify(pair.getElementAt(0), pair.getElementAt(1))
			if not unified_set.isEmpty():
				queue.remove(pair)
				queue.add(unified_set.getDistribution().toSet())

		shattered = Sets.applySubstitution(NameGenerator.getOldNames(), queue.toSet())

		NameGenerator.reset()

		result = StdMarginalBuilder().setParfactors(shattered).setPreservable(self._marginal.getPreservable()).build()

		result = self.simplifyVariables(result)

		return result

	def simplifyVariables(self, marginal):
		'''
		Replaces variables constrained to a single constant with this
		constant in all parfactors in the distribution.

			Parameters
			----------
				marginal : Marginal

			Returns
			-------
				: Marginal
		'''
		m = StdMarginalBuilder(self._marginal.getSize())
		for p in marginal:
			m.addParfactor(p.simplifyVariables())

		query = marginal.getPreservable()
		return m.setPreservable(query).build()

	def renameAllVariables(self):
		'''
		Renames variabels in parfactors. This is done to avoid repetition
		of all variable name from different parfactors.
		'''
		m = StdMarginalBuilder(self._marginal.getSize())
		for p in self._marginal:
			m.addParfactor(self.renameVariables(p))
		query = self._marginal.getPreservable()
		self._marginal = m.setPreservable(query).build()

	def renameVariables(self, p):
		'''
		Renames variables from the specified parfactor.
		Names are generated by NameGenerator.

			Parameters
			----------
				p : Parfactor

			Returns
			-------
				: Parfactor
		'''
		scanned = Scanner(p)
		return p.applySubstitution(NameGenerator.renameVariables(scanned.getVariables()))

	def unify(self, p1, p2):
		'''
		Tries to unify two parfactors. This method returns
		the first opportunity where a pair of PRVs unify.

			Parameters
			----------
				p1 : Parfactor
				p2 : Parfactor

			Returns
			-------
				: Marginal
		'''
		for prv1 in p1.getPrvs():
			for prv2 in p2.getPrvs():
				result = self.unifyOnPrvs(p1, prv1, p2, prv2)
				if not result.isEmpty():
					return result
		return StdMarginalBuilder().build()

	def unifyOnPrvs(self, p1, prv1, p2, prv2):
		'''
		Unifies p1 and p2 on variables prv1 and prv2.

			Parameters
			----------
				p1 : Parfactor
				prv1 : Prv
				p2 : Parfactor
				prv2 : Prv

			Returns
			-------
				: Marginal
		'''
		index_of_prv1 = p1.getPrvs().index(prv1)
		index_of_prv2 = p2.getPrvs().index(prv2)

		result = StdMarginalBuilder()

		try:
			mgu = Prvs.mgu(prv1, prv2)
			# TODO: Check if this is correct
			all_constraints = Sets.union( Sets.union(p1.getConstraints(), p2.getConstraints()), Sets.union(prv1.getConstraints(), prv2.getConstraints()) )
			if (not mgu.isEmpty()) and mgu.isConsistentWithConstraints(all_constraints):

				first_split = self.splitOnSubstitution(p1, mgu)
				second_split = self.splitOnSubstitution(p2, mgu)

				prv2 = second_split.getResult().getPrvs()[index_of_prv2]
				all_constraints = Sets.union(second_split.getResult().getConstraints(), prv2.getConstraints())
				first_split_on_constraints = self.splitOnConstraints(first_split, all_constraints)

				prv1 = first_split.getResult().getPrvs()[index_of_prv1]
				all_constraints = Sets.union(first_split.getResult().getConstraints(), prv1.getConstraints())
				second_split_on_constraints = self.splitOnConstraints(second_split, all_constraints)

				union = Sets.union(first_split_on_constraints.getDistribution().toSet(), second_split_on_constraints.getDistribution().toSet())
				result.setParfactors(union)
				result.setPreservable(self._marginal.getPreservable())
			else:
				# PRVs do not unify
				pass
		except IllegalArgumentError:
			# PRVs represent disjoint sets of random variables
			pass

		return result.build()

	def splitOnSubstitution(self, parfactor, mgu):
		'''
		Returns the result of splitting the specified parfactor on the
		specified MGU.

			Parameters
			----------
				parfactor : Parfactor
					the parfactor to split
				mgu : Substitution
					the most general Unifier to split this parfactor.

			Returns
			-------
				: SplitResult
					the result of splitting the specified parfactor on the
					specified MGU
		'''
		result = parfactor
		residues = StdMarginalBuilder()
		for bind in mgu.asList():
			scanner = Scanner(result)
			if bind.getFirstTerm() in scanner.getVariables():

				result = self.expand(result, Substitution([bind]))

				bind_as_sub = Substitution([bind])
				if result.isSplittable(bind_as_sub):
					split = result.splitOn(bind_as_sub)
					result = split.getResult()
					residues.setParfactors(split.getResidue())
				else:
					result = result.applySubstitution(bind_as_sub)
		return SplitResult(result, residues.build())

	def splitOnConstraints(self, split_result, constraints):
		'''
		Returns the result of splitting the specified parfactor on the
		specified constraints.
		The only difference is that constraints are converted to substitutions
		and splits are made on residues.

			Parameters
			----------
				split_result : SplitResult
				constraints : { Constraint }
		'''
		residue = split_result.getResult()
		by_product = StdMarginalBuilder()
		by_product.setParfactors(split_result.getResidue())
		for constraint in constraints:
			constraint_as_sub = self.convertToSubstitution(constraint)
			residue = self.expand(residue, constraint_as_sub)
			if residue.isSplittable(constraint_as_sub):
				split = residue.splitOn(constraint_as_sub)
				residue = next(iter(split.getResidue()))
				by_product.setParfactors([split.getResult()])
		return SplitResult(residue, by_product.build())

	def expand(self, parfactor, sub):
		'''
		Returns the result of expanding all counting formulas from the
		specified parfactor on the specified term. Expansion is made only if
		conditions for expansions are met.

			Parameters
			----------
				parfactor : Parfactor
				sub : Substitution

			Returns
			-------
				parfactor : Parfactor
		'''
		variables = parfactor.getPrvs()
		for prv in variables:
			if parfactor.isExpandable(prv, sub):
				term = sub.getReplacement(prv.getBoundVariable())
				parfactor = parfactor.expand(prv, term)
		return parfactor

	def convertToSubstitution(self, constraint):
		'''
			Parameters
			----------
				constraint : Constraint

			Returns
			-------
				constraints_as_sub : Substitution
		'''
		#constraint_as_sub = None
		try:
			constraint_as_sub = Substitution([constraint.toBinding()])
		except ValueError:
			constraint_as_sub = Substitution([constraint.toInverseBinding()])
		return constraint_as_sub

	def cost(self):
		return 2147483647

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Shatter'

#######################
# FinalMultiplication #
#######################

class FinalMultiplication(MacroOperation):
	'''
		Attributes
		----------
			marginal : Marginal
	'''

	# Constructor

	__slots__ = ('_marginal')

	def __init__(self, m):
		'''
		Constructor of the FinalMultiplication class

			Parameters
			----------
				m : Marginal
		'''
		self._marginal = m

	def run(self):
		product = StdParfactorBuilder().build()

		for candidate in self._marginal:
			product = product.multiply(candidate)
		result = StdMarginalBuilder(1).setParfactors([product]).build()

		return result

	def cost(self):
		cost = 2147483647
		if self.marginalHasOnlyPreservable():
			# TODO: Should be correct,
			#		But leave this comment
			#		just in case.
			if not self._marginal.isEmpty():
				cost = next(iter(self._marginal)).getFactor().getSize()
		return cost

	def marginalHasOnlyPreservable(self):
		'''
		Returns
		-------
			: bool
		'''
		for p in self._marginal:
			for prv in p.getPrvs():
				rvs = RandomVariableSet(prv, p.getConstraints())
				if Prvs.areDisjoint(rvs, self._marginal.getPreservable()):
					return False
		return True

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Final Multiplication'

#######################
# ImpossibleOperation #
#######################

class ImpossibleOperation(MacroOperation):
	'''
	Dummy operation. Not supposed to be executed.
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the ImpossibleOperation class
		'''
		pass

	def run(self):
		'''
			Raises
			------
				NotImplementedError
					Always
		'''
		raise NotImplementedError()

	def cost(self):
		return 2147483647

	def numberOfRandomVariablesEliminated(self):
		return 0

	def __str__(self):
		return 'Impossible Operation'

#########
# CFOVE #
#########

class CFOVE:
	'''
	IMPORTANT! The ConvertToStdParfactor method is missing
			   for obvious reasons.

		Attributes
		----------
			input : Marginal
			result : Marginal
			currentOperation : MacroOperation
	'''

	# Constructor

	__slots__ = ('_input', '_result', '_currentOperation')

	def __init__(self, parfactors):
		'''
		Constructor of the CFOVE class

			Parameters
			----------
				parfactors : Marginal
		'''
		self._input = parfactors
		result = self._input
		self._result = self.performInitialShattering(result)
		self._currentOperation = Shatter(self._result)

	def performInitialShattering(self, arg):
		'''
		Shatters the specified marginal on the query (preservable of the marginal).
		After that shatters all parfactors in the marginal to guarantee that for
		each pair of PRVs in different parfactors, sets of randomg variables
		represented by them are either equal or disjoint.

			Parameters
			----------
				arg : Marginal
					the marginal to shatter

			Returns
			-------
				result : Marginal
					the specified marginal shattered
		'''
		query = StdParfactorBuilder().addVariables([arg.getPreservable().getPrv()]).addConstraints(arg.getPreservable().getConstraints()).build()
		result = StdMarginalBuilder().addMarginal(arg).addParfactor(query).build()
		# TODO: Is creating a new 'result' correct here?
		result = Shatter(result).run()
		return result

	def run(self):
		'''
		Runs the C-FOVE algorithm and returns the result.

			Returns
			-------
				: Parfactor
					the result of running the C-FOVE algorithm on the marginal
					specified when creating this instance.
		'''
		while self.thereAreVariablesToEliminate():
			self.runStep()
			self.resetCurrentOperation()

		self.evaluateFinalMultiplication()
		try:
			self.runStep()
		except NotImplementedError:
			raise ValueError()

		return next(iter(self._result))

	def thereAreVariablesToEliminate(self):
		'''
		Checks if there are variables to eliminate in the marginal.
		All random variables that are not in the query must be eliminated.

			Returns
			-------
				: bool
		'''
		return not not self._result.getEliminables()

	def runStep(self):
		'''
		Returns the result of running one step of the algorithm.
		A step consists of choosing a macro operation and executing it.

			Returns
			-------
				result : Marginal
					the result of running one step of the operation
		'''
		self.chooseMacroOperation()
		print(self._currentOperation)
		self.executeMacroOperation()
		return self._result

	def chooseMacroOperation(self):
		'''
		Chooses the macro operation to execute. The chosen operation must have
		a smaller cost than the current operation.
		'''
		for p in self._result:
			for prv in p.getPrvs():
				self.evaluateFullExpand(p, prv)
				self.evaluateGlobalSumOut(prv, p.getConstraints())
			for lv in p.getVariables():
				self.evaluateCountingConvert(p, lv)
				self.evaluatePropositionalize(p, lv)

	def evaluateGlobalSumOut(self, prv, c):
		'''
			Parameters
			----------
				prv : Prv
				c : { Constraint }
		'''
		eliminables = RandomVariableSet(prv, c)
		candidate = GlobalSumOut(self._result, eliminables)
		self.compareAndUpdate(candidate)

	def evaluateFullExpand(self, p, prv):
		'''
			Parameters
			----------
				p : Parfactor
				prv : Prv
		'''
		candidate = FullExpand(self._result, p, prv)
		self.compareAndUpdate(candidate)

	def evaluateCountingConvert(self, p, v):
		'''
			Parameters
			----------
				p : Parfactor
				v : Variable
		'''
		candidate = CountingConvert(self._result, p, v)
		self.compareAndUpdate(candidate)

	def evaluatePropositionalize(self, p, v):
		'''
			Parameters
			----------
				p : Parfactor
				v : Variable
		'''
		candidate = Propositionalize(self._result, p, v)
		self.compareAndUpdate(candidate)

	def evaluateFinalMultiplication(self):
		candidate = FinalMultiplication(self._result)
		self.compareAndUpdate(candidate)

	def compareAndUpdate(self, candidate):
		'''
		Compares the candidate macro operation with current operation and
		updates current if candidate's cost is smaller.
		In case of draw, the operation that eliminates more random variables is
		chosen.
		In case of another draw, the current operation is kept.

			Parameters
			----------
				candidate : MacroOperation
		'''
		candidate_cost = candidate.cost()
		current_cost = self._currentOperation.cost()
		candidate_eliminables = candidate.numberOfRandomVariablesEliminated()
		current_eliminables = self._currentOperation.numberOfRandomVariablesEliminated()

		cost_is_smaller = (candidate_cost < current_cost)
		eliminables_more = (candidate_eliminables > current_eliminables)
		eliminables_the_same = (candidate_eliminables == current_eliminables)

		if eliminables_more or (eliminables_the_same and cost_is_smaller):
			self._currentOperation = candidate
		else:
			pass

	def executeMacroOperation(self):
		'''
		Executes the current macro operation.
		'''
		self._result = self._currentOperation.run()

	def resetCurrentOperation(self):
		'''
		Resets the current Macro operation for the next step
		of the algorithm.
		'''
		self._currentOperation = ImpossibleOperation()

	def getResult(self):
		return self._result

	def getCurrentOperation(self):
		return self._currentOperation
