from modules import *
'''
This module provides all the classes and methods
extending the already given FLBN formalism
that are required to run the C-FOVE lifted inference algorithm
on FLBNs.
	
	Classes
	-------
		ConstantFactor
		CountingFormula
		Factor
		Histogram
		NameGenerator
		Prvs
		RandomVariableSet
		StdFactor
		Tuple
'''

#########
# Tuple #
#########

class Tuple:
	'''
		Attributes
		----------
			values : list
			size : int
	'''

	# Constructor

	__slots__ = ('_values', '_size')

	def __init__(self, values=[]):
		'''
		Constructor of the Tuple class

			Parameters
			----------
				values : list
		'''
		self._values = copy(values)
		self._size = len(values)

	# Iterator

	def __iter__(self):
		'''
		Iterates over all the elements of values.
		'''
		for x in self._values:
			yield(x)

	# Getters

	# renamed from get()
	def getElementAt(self, index):
		'''
		Returns the element at the specified position in this Tuple

			Parameters
			----------
				index : int
					Index of the element to return

			Returns
			-------
				values[index]
					Element at the specified position of this tuple
		'''
		return self._values[index]

	def subTuple(self, indexes):
		'''
		Returns a sub-tuple of this tuple, given by the specified
		indexes

			Parameters
			----------
				indexes : [ int ]

			Returns
			-------
				: Tuple
					A sub-tuple of this tuple
		'''
		temp = []
		for i in range(len(indexes)):
			temp.append(self.getElementAt(indexes[i]))
		return Tuple(temp)

	def getSize(self):
		'''
		Returns the number of elements in this tuple.

			Returns
			-------
				size : int
					the number of elements in this tuple
		'''
		return self._size

	def isEmpty(self):
		'''
		Returns True if this tuple contains no elements or is None,
		False otherwise-

			Returns
			-------
				True, iff this tuple has no elements or is None.
		'''
		return self._values == None or not self._values

	# Setters

	def removeElementAt(self, index):
		'''
		Removes the element at the specified index. All values to the right
		of the index will be shifted to the left.

			Parameters
			----------
				index : int
					the index of the element to be removed

			Returns
			-------
				: Tuple
					a copy of this tuple with the element specified removed
		'''
		new_values = copy(self._values)
		del new_values[index]
		return Tuple(new_values)

	def setElementAt(self, index, element):
		'''
		Replaces the element at the specified position in this tuple with the
		specified element. The tuple is not modified, a new tuple is generated instead.

			Parameters
			----------
				index : int
					index of the element to replace
				element :
					Element to be stored at the specified position

			Returns
			-------
				: Tuple
					new tuple with the element at the specified position replaced
					by the specified element
		'''
		temp = copy(self._values)
		temp[index] = element
		return Tuple(temp)

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, Tuple):
			return False
		if self._size != other.getSize():
			return False
		for i in range(self._size):
			if self._values[i] != other.getElementAt(i):
				return False
		return True

	def __hash__(self):
		return hash((self._values, self._size))

##########
# Factor #
##########

class Factor:
	'''
	Represents a Factor in the C-FOVE algorithm.
	Abstract class. Can be either StdFactor or ConstantFactor
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the Factor class
		'''
		pass

	def getIndex(self, pair):
		'''
		Returns the index of a tuple.

			Parameters
			----------
				pair : Tuple
					the tuple to search

			Returns
			-------
				: int
					The index of a tuple in this factor
		'''
		pass

	def getTuple(self, index):
		'''
		Returns the value of the tuple specified by its index.

			Parameters
			----------
				index : int
					The index of a tuple in this factor

			Returns
			-------
				the value of the tuple specified by its index
		'''
		pass

	def getValueOfIndex(self, index):
		'''
		Returns the value of the Tuple specified by the index.

			Parameters
			----------
				index : int
					index of the tuple in this factor

			Returns
			-------
				Value of the Tuple specified by its index
		'''
		pass

	def getValueOfTuple(self, pair):
		'''
		Returns the value of the specified Tuple.

			Parameters
			----------
				pair : Tuple
					tue tuple whose value is to return

			Returns
			-------
				: Decimal
					the value of the specified tuple
		'''
		pass

	def getSize(self):
		'''
		Returns the number of values in this Factor, whicch is the same as the
		number of tuples in this factor.

			Returns
			-------
				: int
					the number of values in this Factor
		'''
		pass

	def getName(self):
		'''
		Returns the name of this factor.

			Returns
			-------
				name : str
					the name of this factor
		'''
		pass

	def getVariables(self):
		'''
		Returns the list of Prvs associated with this factor. This
		list has the same order in which Prvs were inserted when creating
		this factor.

			Returns
			-------
				variables : [ Prv ]
					The list of Prvs associated with this factor, in order
		'''
		pass

	def getValues(self):
		'''
		Returns the values of all tuples, in the order they were created.

			Returns
			-------
				values : [ Decimal ]
					list containing all values of this factor in order
		'''
		pass

	def containsTerm(self, t):
		'''
		Checks if the specified Term is in this factor.

			Parameters
			----------
				t : Term
					the term to search for

			Returns
			-------
				: bool
					True iff the specified Term is in this factor
		'''
		pass

	def occurrences(self, t):
		'''
		Returns the number of occurrences of the specified Term in
		Prvs from this factor.

			Parameters
			----------
				t : Term
					the term to search for

			Returns
			-------
				: int
					the number of occurrences of the specified Term in
					Prvs from this factor
		'''
		pass

	def getVariableHavingTerm(self, t):
		'''
		Returns the first occurrence of a PRV in this factor having the
		specified term, according to the order returned by the iterator
		of variables in this factor.

			Parameters
			----------
				t : Term
					the term to search for

			Returns
			-------
				: Prv
					the first occurrence of a PRV in this factor
					having the specified term
		'''
		pass

	def isSubFactorOf(self, factor):
		'''
		Returns if this factor is a sub-factor of the specified factor.

		Factor F1 is a sub-factor of factor F2 if the set of Prvs from
		F1 is a subset of the set of Prvs from F2.

			Parameters
			----------
				factor : Factor

			Returns
			-------
				: bool
					if this factor is a sub-factor of the specified factor
		'''
		pass

	def isConstant(self):
		'''
		Returns if this factor is constant.
		Constant factors return the value 1 for all tuples of this factor.

			Returns
			-------
				: bool
					True iff this factor is constant
		'''
		pass

	def isEmpty(self):
		'''
		Returns if this factor is empty.
		An empty factor has no variables or values.

			Returns
			-------
				: bool
					True iff this factor is empty
		'''
		pass

	def applySubstitution(self, s):
		'''
		Returns the result of applying the specified substitution to this
		Factor. The substitution is applied to PRVs of this Factor, but its
		values are not modified.

			Parameters
			----------
				s : Substitution
					the substitution to apply

			Returns
			-------
				: Factor
					the result of applying the specified substitution to this Factor
		'''
		pass

	def setValue(self, pair, value):
		'''
		Returns a copy of this factor with the value of the specified tuple
		replaced by the specified value.

			Parameters
			----------
				pair : Tuple
					the tuple whos value must be modified

				value : Decimal
					the new value of the tuple

			Returns
			-------
				: Factor
					a copy of this factor with the value of the specified tuple
					replaced by the specified value
		'''
		pass

	def sumOut(self, prv):
		'''
		Sums out a random variable from a factor.

			Parameters
			----------
				prv : the Prv to be summed out

			Returns
			-------
				: Factor
					a factor with the specified Prv summed out		
		'''
		pass

	def pow(self, p, q):
		'''
		Returns this factor raised by p/q

		Raising a factor to some exponent is the same as raising its values to
		that exponent.

			Parameters
			----------
				p : int
					Numerator of the exponent
				q : int
					Denominator of the exponent

			Returns
			-------
				: Factor
					the value of this factor raised by p/q
		'''
		pass

	def multiply(self, factor):
		'''
		Multiplies this factor with the specified factor.

			Parameters
			----------
				factor : Factor
					the second factor to be multiplied

			Returns
			-------
				: Factor
					the multiplication of this factor with
					the specified other factor
		'''
		pass

	def reorder(self, reference):
		'''
		Returns this factor reordered using the specified factor as reference.
		The returned factor will have the same Prv order as the reference, with
		values reordered in order to not modify the distribution it represents.

			Parameters
			----------
				reference : Factor
					a reference factor that dictates the new PRV order

			Returns
			-------
				: Factor
					this factor reordered using the specified factor as reference

			Raises
			------
				IllegalArgumentError
					If the reference does not have the same PRVs as this factor
		'''
		pass

#############
# StdFactor #
#############

# IMPORTANT!!!
# Tuples in StdFactors represent all possible values
# in the conjoined domain of the PRVs!!!

# Should always return 2^len(variables) for us,
# as our codomain is always Bool, at least in the case
# of Prv = Formula.
def StdFactorGetSize(variables):
	'''
	Returns the expected size a Factor

		Parameters
		----------
			formulas : [ Formula ]
				a list of formulas

		Returns
		-------
			size : int
				expected size of factor
	'''
	size = 1
	if not variables:
		size = 0
	for prv in variables:
		size = size * len(prv.getCodomain())
	return size

class StdFactor(Factor):
	'''
	Represents a StdFactor for the C-FOVE algorithm.
	StdFactors are table representations of Joint distributions.
	Inherits from Factor.

	Values are indexed based on the order of variables (columns)
	and the order of the range of each variable.

	For this and other Factor classes, we will adopt takiyamas terminology.
	Thus 'variables' refers to 'Parametrized Random Variables' (PRVs) in this
	case, that is Formulas and CountingFormulas for us
	and NOT objects of the Variable class. Always keep that in mind!

		Attributes
		----------
			name : str
				name of the Factor
			variables : [ Prv ]
				List of PRVs
				Must be ordered
			values : [ Decimal ]
				List of decimals
				Must be ordered
			size : int
	'''

	# Constructor

	__slots__ = ('_name', '_variables', '_values', '_size')

	def __init__(self, name, variables, values):
		'''
		Constructor of the StdFactor class

			Parameters
			----------
				name : str
					name of the Factor
				variables : [ Prv ]
					List of relations
				values : [ Decimal ]
					List of decimals

			Raises
			------
				IllegalArgumentError
					If wrong number of values was received.
		'''
		self._name = name
		self._variables = copy(variables)
		self._values = copy(values)
		self._size = StdFactorGetSize(variables) # better call it like this, might clash with non-static method

		if len(values) != 0 and len(values) != self._size:
			raise IllegalArgumentError('Wrong number of values. Expected:', self._size, ', received:', len(values))

	# static methods

	getSize = staticmethod(StdFactorGetSize)

	# Iterator

	def __iter__(self):
		'''
		Iterates over Tuples of this factor.
		'''
		# TODO: Is this correct?
		for i in range(self._size):
			yield(self.getTuple(i))

	# Getters

	# Iterates over all entries of the given Tuple.
	# In our case codomainSize = 2:
	# If pair = (False, True), then:
	#
	# index <- 0
	# r <- 1
	# i <- 1
	# Loop begins
	# index <- index + r * i = 0 + 1 * 1 = 1
	# r <- r * 2 = 1 * 2 = 2
	# i <- 0
	# index <- index + r * i = 1 + 2 * 0 = 1
	# r <- r * 2 = 2 * 2 = 4
	# i <- -1
	# Loop ends
	#
	# Nope, I don't get it what this is supposed to be.
	def getIndex(self, pair):
		if pair.isEmpty():
			raise IllegalArgumentError('This tuple is empty!')
		index = 0
		r = 1
		i = pair.getSize() - 1
		#print(len(self._variables))
		#print(pair.getSize())
		#print(i)
		while i >= 0:
			index = index + r * self.getIndexOf(i, pair)
			r = r * self.getCodomainSize(i)
			i -= 1
		return index

	# Takes a tuple 'pair' and an index i as argument.
	# The tuple contains RangeElements (for us: Bool)
	#
	# - Takes the i-th entry of pair
	# - Takes the i-th Prv in variables <- This is very weird. Why the i-th?
	# - Gets the Codomain of the i-th Prv
	# - Gets and returns the index of the Above codomain at which the i-th entry of
	#	pair is located.
	def getIndexOf(self, i, pair):
		'''
		Returns the index of the range element that occupies the specified
		position in the tuple.

			Parameters
			----------
				i : int
					the position in the tuple

				pair : Tuple
					a tuple of RangeElement

			Returns
			-------
				: int
		'''
		return self._variables[i].getCodomain().index(pair.getElementAt(i))
		
	def getCodomainSize(self, i):
		'''
		Returns the codomain size of the PRV at
		the specified index.

			Parameters
			----------
				i : int
					index in this factor

			Returns
			-------
				: int
					codomain size of the PRV at
					the specified index
		'''
		return len(self._variables[i].getCodomain())

	def getCodomainElementAt(self, range_index, prv_index):
		'''
		Return the RangeElement at range_index
		for the PRV at prv_index.
		'''
		return self._variables[prv_index].getCodomain()[range_index]

	def getTuple(self, index):
		values = []
		j = len(self._variables) - 1
		while j > 0:
			domain_size = self.getCodomainSize(j)
			values.append(self.getCodomainElementAt(index % domain_size, j))
			index = int(index / domain_size)
			j -= 1
		values.append(self.getCodomainElementAt(index, 0))
		values.reverse()
		return Tuple(values)

	def getValueOfIndex(self, index):
		return self._values[index]

	def getValueOfTuple(self, pair):
		return self.getValueOfIndex(self.getIndex(pair))

	def getSize(self):
		return self._size

	def getName(self):
		return self._name

	def getVariables(self):
		return copy(self._variables)

	def getValues(self):
		return copy(self._values)

	def containsTerm(self):
		for prv in self._variables:
			if prv.containsTerm(t):
				return True
		return False

	def occurrences(self, t):
		count = 0
		for prv in self._variables:
			if prv.containsTerm(t):
				count += 1
		return count

	def getVariableHavingTerm(self, t):
		# TODO: Although Relations behave similar to StdPrvs for us,
		#		this might not be ideal.
		result = Relation('')
		for prv in self._variables:
			if prv.containsTerm(t):
				result = prv
		return result

	def isSubFactorOf(self, factor):
		if len(factor.getVariables()) < len(self._variables):
			return False
		for prv in self._variables:
			if not prv in factor.getVariables():
				return False
		return True

	def isConstant(self):
		for val in self._values:
			if val != D('1'):
				return False
		return True

	def isEmpty(self):
		no_variables = not self._variables
		no_values = not self._values
		return no_variables and no_values

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, StdFactor):
			return False
		return self._variables == other._variables and self._values == other._values

	def __hash__(self):
		return hash((*self._variables, *self._values))

	def applySubstitution(self, s):
		substituted_vars = []
		for prv in self._variables:
			# TODO: Careful! Remember that applying substitutions
			#		changes the prv. I still doubt that this is
			#		intended.
			substituted = prv.applySubstitution(s)
			substituted_vars.append(substituted)
		return StdFactor(self._name, substituted_vars, self._values)

	def setValue(self, pair, value):
		vals = copy(self._values)
		vals[self.getIndex(pair)] = value
		return StdFactor(self._name, self._variables, vals)

	def sumOut(self, prv):
		if not prv in self._variables:
			return self

		was_visited = [False for i in range(self._size)]

		vars1 = copy(self._variables)
		vars1.remove(prv)

		vals = []
		prv_index = self._variables.index(prv)
		for i in range(self._size):
			if not was_visited[i]:
				current = self.getTuple(i)
				sum1 = D('0')

				for e in prv.getCodomain():
					next1 = current.setElementAt(prv_index, e)
					correction = prv.getSumOutCorrection(e)
					sum1 = sum1 + (self.getValueOfTuple(next1) * correction)
					was_visited[self.getIndex(next1)] = True
				vals.append(sum1)
		return StdFactor(self._name, vars1, vals)

	def pow(self, p, q):
		new_values = []
		for base in self._values:
			new_values.append(MathUtils.mathUtilsPow(base, p, q))
		return StdFactor(self._name, self._variables, new_values)

	def multiply(self, factor):
		if self.isEmpty():
			return factor

		if factor.isEmpty():
			return self

		if self.isConstant():
			return factor

		if factor.isConstant():
			return self

		new_name = self.getName() + '*' + factor.getName()
		union = Lists.union(self.getVariables(), factor.getVariables())
		mult = []
		
		map_of_common_variables = self.getMapOfCommonVariables(self, factor)

		for t1 in self:
			for t2 in factor:
				if self.haveSameSubtuple(t1, t2, map_of_common_variables):
					mult.append(self.getValueOfTuple(t1) * factor.getValueOfTuple(t2))

		return StdFactor(new_name, union, mult)

	def getMapOfCommonVariables(self, f1, f2):
		'''
		Returns a mapping from indexes of variables in the first factor
		to the indexes of the variables that also appear in the second factor.

		e.g.
		if f1(x1,x2,x3,x4,x5) and f2(x5,x4,x1) are factors,
		then the mapping will be the matrix:

		0 3 4
		2 1 0

		as 	f1[0] = f2[2]
			f1[3] = f2[1]
			f1[4] = f2[1]

			Parameters
			----------
				f1 : Factor
				f2 : Factor

			Returns
			-------
				: int[][]
					mapping of indexes from common variables between f1 and f2
		'''
		mapping = [[0 for j in range(len(f1.getVariables()))] for i in range(2)]
		size = 0

		for prv1 in f1.getVariables():
			#if prv1 in f2.getVariables():
			if prv1 in f2.getVariables():
				mapping[0][size] = f1.getVariables().index(prv1)
				mapping[1][size] = f2.getVariables().index(prv1)
				size += 1
		return self.trim(mapping, size)

	def trim(self, matrix, size):
		'''
		Trims the specified matrix to the specified size.
		The length of the matrix is preserved.

			Parameters
			----------
				matrix : int[][]
					the matrix to trim
				size : int
					the limit of the size of each line of
					the matrix

			Returns
			-------
				m : int[][]
					the specified matrix trimmed to the specified size
		'''
		m = [[0 for j in range(size)] for i in range(len(matrix))]
		for j in range(size):
			m[0][j] = matrix[0][j]
			m[1][j] = matrix[1][j]
		return m

	def haveSameSubtuple(self, t1, t2, map1):
		'''
		Checks if both tuples have the same sub-tuple.
		The sub-tuple is defined according to a map.

			Parameters
			----------
				t1 : Tuple
					first tuple to check
				t2 : Tuple
					second tuple to check
				map1 : int[][]
					mapping that connects indexes representing the same PRV

			Returns
			-------
				: bool
					True iff tuples have the same values for the sub-tuple
		'''
		st1 = t1.subTuple(map1[0])
		st2 = t2.subTuple(map1[1])
		return st1 == st2

	def reorder(self, reference):
		if not Lists.sameElements(self.getVariables(), reference.getVariables()):
			raise IllegalArgumentError()

		map_of_common_variables = self.getMapOfCommonVariables(reference, self)
		reordered = []
		for pair in reference:
			r = []

			for i in range(len(map_of_common_variables[1])):
				r.append(pair.getElementAt(map_of_common_variables[1][i]))
			reordered_pair = Tuple(r)
			reordered.append(self.getValueOfTuple(reordered_pair))
		result = StdFactor(self._name, reference.getVariables(), reordered)
		return result

##################
# ConstantFactor #
##################

def ConstantFactorGetSize(variables):
	size = 1
	if not variables:
		size = 0
	for prv in variables:
		size = size * len(prv.getCodomain())
	return size

class ConstantFactor(Factor):
	'''
		Attributes
		----------
			variables : [ Prv ]
			size : int
	'''

	# Constructor

	__slots__ = ('_variables', '_size')

	def __init__(self, variables=[]):
		'''
		Constructor for the ConstantFactor class

			Parameters
			----------
				variables : [ Prv ]
		'''
		self._variables = copy(variables)
		self._size = ConstantFactorGetSize(variables)

	# staticmethods

	getSize = staticmethod(ConstantFactorGetSize)

	# Iterator
	def __iter__(self):
		# TODO: richtig?
	 	for i in range(self._size):
	 		yield(self.getTuple(i))

	# Getters

	def getIndex(self, pair):
		if pair.isEmpty():
			raise IllegalArgumentError('This tuple is empty!')
		index = 0
		r = 1
		i = pair.getSize() - 1
		while i >= 0:
			index = index + r * self.getIndexOf(i, pair)
			r = r * self.getCodomainSize(i)
			i -= 1
		return index

	def getIndexOf(self, i, pair):
		return self._variables[i].getCodomain().index(pair.getElementAt(i))

	def getCodomainSize(self, i):
		return len(self._variables[i].getCodomain())

	def getCodomainElementAt(self, range_index, prv_index):
		return self._variables[prv_index].getCodomain()[range_index]

	def getTuple(self, index):
		values = []
		j = len(self._variables) - 1
		while j > 0:
			domain_size = self.getCodomainSize(j)
			values.append(self.getCodomainElementAt(int(index % domain_size), j))
			index = int(index / domain_size)
			j -= 1
		values.append(self.getCodomainElementAt(index, 0))
		values.reverse()
		return Tuple(values)

	def getValueOfIndex(self, index):
		return D('1')

	def getValueOfTuple(self, tuple):
		return self.getValueOfIndex(0)

	def getSize(self):
		return self._size

	def getName(self):
		return '1'

	def getVariables(self):
		return copy(self._variables)

	def getValues(self):
		values = []
		for i in range(self._size):
			values.append(D('1'))
		return values

	def containsTerm(self, t):
		for prv in self._variables:
			if prv.containsTerm(t):
				return True
		return False

	def occurrences(self, t):
		count = 0
		for prv in self._variables:
			if prv.containsTerm(t):
				count += 1
		return count

	def getVariableHavingTerm(self, t):
		# TODO: As in StdFactor, this might not be ideal.
		result = Relation('')
		for prv in self._variables:
			if prv.containsTerm(t):
				result = prv
		return result

	def isSubFactorOf(self, factor):
		return set(self._variables).issubset(set(factor.getVariables()))

	def isConstant(self):
		return True

	def isEmpty(self):
		return not self._variables

	def applySubstitution(self, s):
		return ConstantFactor(Lists.applySubstitution(s, copy(self._variables)))

	def setValue(self, pair, value):
		raise NotImplementedError()

	def sumOut(self, prv):
		vars1 = self.getVariables()
		vars1.remove(prv)
		return ConstantFactor(vars1)

	def pow(self, p, q):
		return self

	def multiply(self, factor):
		return factor

	def reorder(self, reference):
		if not Lists.sameElements(self.getVariables(), reference.getVariables()):
			raise IllegalArgumentError()
		result = ConstantFactor(reference.getVariables())
		return result

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, ConstantFactor):
			return False
		return self._size == other._size and self._variables == other._variables

	def __hash__(self):
		return hash((self._size, self._variables))

#############
# Histogram #
#############

def copyHistogram(h):
	result = Histogram(list(h._distribution.keys()))
	for o in result._distribution:
		result.setCount(o, h.getCount(o))
	return result

class Histogram(RangeElement):
	'''
	Represents the elements of the range of a counting formula.
	Histograms are tuples composed by buckets, which in turn store the
	count of elements from the range of the counted PRV.

		Attributes
		----------
			distribution : {Object : int}
				dictionary that assings each object
				an integer value
	'''

	# Constructors

	__slots__ = ('_distribution')

	def __init__(self, prv_range):
		'''
		Constructor of the Histogram class

			Parameters
			----------
				prv_range : list
					list representing the codomain of some PRV
		'''
		self._distribution = {}
		for i in range(len(prv_range)):
			self._distribution[prv_range[i]] = 0

	# Getters
	def getCount(self, range_value):
	 	'''
	 	Returns the count of the specified bucket

	 		Parameters
	 		----------
	 			range_value :
	 				key to the bucket

	 		Returns
	 		-------
	 			: int
	 				the count of the specified bucket
	 	'''
	 	return self._distribution[range_value]

	def getSize(self):
	 	'''
	 	Returns the number of buckets in this histogram.

	 		Returns
	 		-------
	 			: int
	 				the number of buckets in this histogram
	 	'''
	 	return len(self._distribution)

	def containsBucket(self, bucket):
	 	'''
	 	Returns if this histogram contains the specified bucket.

	 		Paramaters
	 		----------
	 			bucket : RangeElement
	 				the bucket to search for

	 		Returns
	 		-------
	 			: bool
	 				True, iff this histogram contains the specified bucket
	 	'''
	 	# TODO: Careful!
	 	# Deviates from original
	 	for elem in self._distribution.keys():
	 		if elem == bucket:
	 			return True
	 	return False

	def containsValue(self, count):
		'''
	 	Returns true if this histogram contains a bucket with the
	 	specified count.

	 		Parameters
	 		----------
	 			count : int
	 				a count to check

	 		Returns
	 		-------
	 			: bool
	 				True, iff this histogram contains a bucket with the
	 				specified count
	 	'''
		return count in self._distribution.values()

	# Setters

	def addCount(self, range_value, amount):
		'''
		Adds the specified amount to the count of the specified range element.

			Parameters
			----------
				range_value :
					the key to the bucket
				amount : int
					the amount to sum to the bucket
		'''
		self._distribution[range_value] += amount

	def setCount(self, range_value, amount):
		'''
		Set the specified amount as the count for the specified bucket.

			Parameters
			----------
				range_value :
					the key to the bucket
				amount : int
					the amount to set into the bucket
		'''
		self._distribution[range_value] = amount

	def toMultinomial(self):
		'''
		Converts the values contained in each bucket to a Multinomial.

			Returns
			-------
				: Multinomial
					this histogram converted to a multinomial
		'''
		values = list(self._distribution.values())
		return Multinomial(values)

	def combine(self, e):
		'''
		Returns tihs histogram with the count of the specified bucket
		incremented by 1.
		'''
		result = None
		if self.containsBucket(e):
			distribution = copy(self._distribution)
			copy1 = copyHistogram(self)
			copy1.addCount(e, 1)
			result = copy1
		else:
			raise IllegalArgumentError()
		return result

	# Methods for Operators omitted. We only use CFOVE for now
	# TODO: Check later if required

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, Histogram):
			return False
		return self._distribution == other._distribution

	def __hash__(self):
		return hash(frozenset(self._distribution.items()))

###################
# CountingFormula #
###################

class CountingFormula(Prv):
	'''
	A conting formula is of the form #_A:C[F(...,A,...)],
	where:
	- A is a variable that is bound by the #-sign
	- C is a set of inequality constraints involving A
	- f(...,A,...) is a PRV
	
	The value of the counting formula, given as an assignment
	of values to random variables v, is the histogram function

	h : range(f) --> |N defined by:
	v_{A:C}[f(...,A,...)] = h^v(x) =
	|{a in D(A):C : v(f(...,a,...)) = x}|
	x in range(f)

		Attributes
		----------
		 bound : Variable
		 	the bound variable
		 constraints : { Constraint }
		 	a set of constraints
		 prv : Prv
		 codomain : [ Histogram ]
	'''

	# Constructor

	__slots__ = ('_bound', '_constraints', '_prv', '_codomain')

	def __init__(self, bound, constraints, prv):
		'''
		Constructor of the CountingFormula class

			Parameters
			----------
				bound : Variable
					the bound variable
				constraints	: { Constraint }
					set of constraints involving bound
				prv : Prv
					the Prv associated with this formula

			Raises
				IllegalArgumentError
					if bound does not appear in prv
				ValueError
					if the set of constraints is too restrictive to
					create a PRV
		'''
		self._prv = prv.copy()
		self._bound = bound
		self._constraints = copy(constraints)
		self._codomain = []

		if not prv.containsTerm(bound):
			raise IllegalArgumentError()

		if self._bound.individualsSatisfyingConstraints(self._constraints).getSize() == 0:
			raise ValueError()

		for c in constraints:
			if not c.containsTerm(bound):
				raise IllegalArgumentError()

		allowed_domain_size = self._bound.numberOfIndividualsSatisfyingConstraints(constraints)
		histogram = Histogram(prv.getCodomain())
		self.generateHistograms(self._codomain, allowed_domain_size, histogram, 0)

	def generateHistograms(self, all_histograms, max_count, histogram, current_bucket):
		'''
		Generates all possible histograms for this counting formula.
		All histograms are put in the specified list.

		The function is recursive and behaves well for histograms with
		short ranges (e.g. binary ranges.)

			Parameters
			----------
				all_histograms : [ histogram ]
					set of all histograms
				max_count : int
					maximum count a bucket can hold
				histogram : Histogram
					an empty histogram
				current_bucket : int
		'''
		if current_bucket == histogram.getSize() - 1 or max_count == 0:
			histogram.setCount(self._prv.getCodomain()[current_bucket], max_count)
			all_histograms.append(copyHistogram(histogram))
			return
		count = max_count
		while count >= 0:
			histogram.setCount(self._prv.getCodomain()[current_bucket], count)
			self.generateHistograms(all_histograms, max_count - count, histogram, current_bucket + 1)
			count -= 1

	# Getters

	def getConstraints(self):
		return copy(self._constraints)

	def getName(self):
		return self._prv.getName()

	def getParameters(self):
		param = []
		for p in self._prv.getParameters():
			if not p == self._bound:
				param.append(p)
		return param

	def getTerms(self):
		return self._prv.getTerms()

	def getBoundVariable(self):
		return copy(self._bound)

	def getGroundSetSize(self, constraints):
		size = 1
		for v in self.getParameters():
			size = size * v.individualsSatisfyingConstraints(constraints).getSize()
		return size

	def getCodomain(self):
		return copy(self._codomain)

	def getPrvCodomainSize(self):
		return len(self._prv.getCodomain())

	# Careful! Despite its name, the following method
	# omits constants and bound variables.
	# TODO: Check if this is correct (seems to be correct though).
	def containsTerm(self, t):
		return t in self.getParameters()

	def getCount(self, histogram, bucket):
		'''
		Returns the count of the bucket fo the specified
		histogram. If the speciifed histogram is not a Histogram
		or is not in the range of this counting formula, returns -1.

			Parameters
			----------
				histogram : Histogram
				bucket : int

			Returns
			-------
				count : int
		'''
		count = -1
		if histogram in self._codomain:
			h_index = self._codomain.index(histogram)
			count = self._codomain[h_index].getCount(bucket)
		return count

	def isStdPrv(self):
		'''
		Checks, if the counting formula can be converte to
		a Formula.
		'''
		return self._bound.individualsSatisfyingConstraints(self._constraints).getSize() == 1

	def getSumOutCorrection(self, e):
		return D(MathUtils.multinomial(e.toMultinomial()))

	def getCanonicalForm(self):
		return self._prv.getCanonicalForm()

	# Setters

	def addConstraint(self, constraint):
		'''
		Adds a constraint to this counting formula.
		Returns a new instance.

			Parameters
			----------
				constraints : { Constraint }

			Returns
			-------
				: CountingFormula
		'''
		constraints = copy(self._constraints)
		constraints.add(constraint)
		return CountingFormula(self._bound, constraints, self._prv)

	def removeTerm(self, t):
		'''
		Returns this counting formula with the specified Term removed.

			Parameters
			----------
				t : Term
					the term to remove

				Returns
				-------
					result : CountingFormula
						this counting formula with the specified Term removed
		'''
		constraint_on_term = InequalityConstraint(self._bound, t)
		result = self.addConstraint(constraint_on_term)

		return result

	def takeOutTerm(self, t):
		'''
		Returns the Prv associated with this counting formula
		with the bound variable replaced by the specified term.

			Parameters
			----------
				t : Term
					the replacement for the variable.

			Returns
			-------
				: Prv
					prv with the bound variable replaced by t
		'''
		b = Binding(self._bound, t)
		s = Substitution([b])
		return self._prv.applySubstitution(s)

	def simplify(self):
		'''
		Returns this counting formula converted to a Formula,
		if this conversion is possible.

			Returns
			-------
				: Prv
		'''
		if self.isStdPrv():
			return self.toStdPrv()
		return self

	def applySubstitution(self, s):
		substituted = self._prv.copy()
		constraints = copy(self._constraints)
		#bound_lv = self._bound
		#bound_lv = Variable(self._bound._name, self._bound._population)
		bound_lv = copy(self._bound)

		for to_replace in s:
			replacement = s.getReplacement(to_replace)

			if bound_lv != to_replace or replacement.isVariable():
				sub = Substitution([Binding(to_replace, replacement)])
				substituted = substituted.applySubstitution(sub)
				constraints = self.applySubstitutionToConstraints(sub, constraints)
				if bound_lv == to_replace:
					bound_lv = copy(replacement)

		return CountingFormula(bound_lv, constraints, substituted)

	def applySubstitutionToPrv(self, s):
		'''
		Returns the result of applying a substitution to prv.

			Parameters
			----------
				s : Substitution
					the substitution to be made

			Returns
			-------
				: Prv
					prv with the specified substitution applied
		'''
		# TODO: Reminder that apply changes prv!
		return self._prv.applySubstitution(s)

	def applySubstitutionToConstraints(self, s, constraints):
		'''
		Returns the set of constraints that result form applying the
		specified substitution to the specified set of constraints.

			Parameters
			----------
				s : Substitution
				constraints : { Constraint }

			Returns
			-------
				: { Constraint }
		'''
		substituted = set()
		for c in constraints:
			try:
				new_constraint = c.applySubstitution(s)
				substituted.add(new_constraint)
			except IllegalArgumentError:
				# Illegal constraint does not get added
				pass
		return substituted

	def increaseCount(self, h_index, e, n):
		'''
		Adds the specified amount to the bucket of the specified histogram.

		Does not modify this counting formula.

			Parameters
			----------
				h_index : int
					index of the histogram
				e : RangeElement
					the bucket
				n : int
					the amount to add

			Returns
			-------
				hist : Histogram
					histogram with the specified amount added
					to the specified bucket.
		'''
		hist = Histogram(self._codomain[h_index])
		hist.addCount(e, n)
		return hist

	def rename(self, name):
		raise NotImplementedError()

	def toStdPrv(self):
		'''
		Converts this counting formula to a formula
		of the type of prv.

		If conversion is not possible, returns this counting formula.

			Returns
			-------
				: Prv
		'''
		result = None
		constrained_individuals = self._bound.individualsSatisfyingConstraints(self._constraints)
		if constrained_individuals.getSize() != 1:
			result = self
		else:
			lone_individual = next(iter(constrained_individuals))
			b = Binding(self._bound, lone_individual)
			s = Substitution([b])
			result = self._prv.applySubstitution(s)
		return result

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, CountingFormula):
			return False
		return self._bound == other._bound and self._prv == other._prv and self._constraints == other._constraints and self._codomain == other._codomain

	def __hash__(self):
		return hash((self._bound, frozenset(self._constraints), *self._codomain))

#################
# NameGenerator #
#################

def NameGeneratorRenameVariable(old):
	'''
	Returns a new Variable name. Names generated have the following format:
	X{n}, where n is a number starting from 1-

	The specified variable is kept in a map so one can retrieve the
	old Variable name later.

		Parameters
		----------
			old : Variable
				the old variable to be renamed

		Returns
		-------
			: Variable
				the specified variable renamed
	'''
	if NameGenerator.map1.containsVariable(old):
		return NameGenerator.map1.getReplacement(old)
	binding_list = NameGenerator.map1.asList()
	NameGenerator.count += 1
	new_name = 'X' + str(NameGenerator.count)
	new_variable = old.rename(new_name)
	bind = Binding(new_variable, old)
	binding_list.append(bind)
	NameGenerator.map1 = Substitution(binding_list)
	return new_variable

def NameGeneratorRenameVariables(old_variables):
	'''
	Returns a substitution that replaces the specified collection of
	variables with new names.

		Parameters
		----------
			old_variables : iterable(Variable)
				iterable object of variables

		Returns
		-------
			: Substitution
				substitution that replaces the specified collection of
				variables with new names.
	'''
	to_rename = []
	to_restore = NameGenerator.map1.asList()
	for old in old_variables:
		new_name = NameGenerator.getNewName()
		new_variable = old.rename(new_name)
		to_rename.append(Binding(old, new_variable))
		to_restore.append(Binding(new_variable, old))
	NameGenerator.map1 = Substitution(to_restore)
	return Substitution(to_rename)

def NameGeneratorGetNewName():
	'''
	Returns a new variable name
	'''
	NameGenerator.count += 1
	return 'X' + str(NameGenerator.count)

def NameGeneratorReset():
	'''
	Resets the count and clears the mapping of Variables.
	'''
	NameGenerator.count = 0
	NameGenerator.map1 = Substitution()

def NameGeneratorGetOldNames():
	return NameGenerator.map1

class NameGenerator:
	'''
		Attributes
		----------
			count : int
				Class Attribute
			map1 : Substitution
				Class Attribute
	'''

	# Constructor

	def __init__(self):
		'''
		Constructor of the NameGenerator class
		'''
		pass

	# Class Attributes

	count = 0
	map1 = Substitution()

	# Static Methods

	renameVariable = staticmethod(NameGeneratorRenameVariable)
	renameVariables = staticmethod(NameGeneratorRenameVariables)
	getNewName = staticmethod(NameGeneratorGetNewName)
	reset = staticmethod(NameGeneratorReset)
	getOldNames = staticmethod(NameGeneratorGetOldNames)

#####################
# RandomVariableSet #
#####################

class RandomVariableSet(Prv):
	'''
	Represents a set of random Variables represented by a PRV and
	a set of constraint.

	For instance given the PRV f(A) with
	D(A) = {a1, a2, a3} and constraints C = {A != a1},
	the Random variable set f(A):C = {f(a2), f(a3)}

		Attributes
		----------
			prv : Prv
			constraints : { Constraint }
	'''

	# Constructor

	__slots__ = ('_prv', '_constraints')

	def __init__(self, prv, constraints):
		'''
		Constructor of the RandomVariableSet class
		'''
		self._prv = prv
		self._constraints = set()
		for c in constraints:
			if c.isUnary() and prv.containsTerm(next(iter(c.getVariables()))):
				self._constraints.add(c)
		for c in prv.getConstraints():
			if c.isUnary():
				self._constraints.add(c)

	# Getters

	def getConstraints(self):
		return copy(self._constraints)

	def getPrv(self):
		'''
		Returns the Prv bound to this set

			Parameters
			----------
				: Prv
					the prv bound to this set
		'''
		return self._prv

	def getComplement(self):
		'''
		Returns the complement of this set.

			Returns
			-------
				: RandomVariableSet
					the complement of this set
		'''
		constraints = set()
		for lv in self._prv.getParameters():
			for c in lv.individualsSatisfyingConstraints(constraints):
				constraints.add(InequalityConstraint(lv, c))
		return RandomVariableSet(self._prv, constraints)

	def intersect(self, rv_set):
		'''
		Returns the intersection of this set and the specified
		RandomVariableSet

			Parameters
			----------
				rv_set : RandomVariableSet

			Returns
			-------
				: RandomVariableSet
					intersection of this set and rv_set
		'''
		if not self._prv == rv_set._prv:
			return RandomVariableSet(Relation(''), set())
		else:
			constraints = copy(self._constraints)
		for constraint in rv_set._constraints:
			constraints.add(constraint)
		return RandomVariableSet(self._prv, constraints)

	def minus(self, rv_set):
		'''
		Returns the difference between this set and the specified set.

			Parameters
			----------
				rv_set : RandomVariableSet

			Returns
			-------
				: RandomVariableSet
					the difference between this set and the specified set
		'''
		if not self._prv == rv_set._prv:
			return self
		else:
			if self._constraints == rv_set._constraints:
				return RandomVariableSet(Relation(''), set())
			else:
				r = rv_set.getComplement()
				constraints = copy(r._constraints)
				for constraint in self._constraints:
					constraints.add(constraint)
				return RandomVariableSet(r._prv, constraints)

	def union(self, rv_set):
		'''
		Returns the union of this set and the specified set.

			Parameters
			----------
				rv_set : RandomVariableSet

			Returns
			-------
				RandomVariableSet
					union of this set and the specified set
		'''
		r = set()
		if not self._prv == rv_set._prv:
			r.add(self)
			r.add(rv_set)
		else:
			constraints = set()
			if self._constraints == rv_set._constraints:
				for constraint in self._constraints:
					constraints.add(constraint)
			else:
				# TODO: richtig?
				for constraint in self._constraints:
					if constraint in rv_set._constraints:
						constraints.add(constraint)
			return r.add(RandomVariableSet(self._prv, constraints))
		return r

	def isEmpty(self):
		return not self._prv.getParameters() and not self._constraints

	def isEquivalentTo(self, s):
		return self == s

	def getName(self):
		return self._prv.getName()

	def getParameters(self):
		return self._prv.getParameters()

	def getTerms(self):
		return self._prv.getTerms()

	def getCodomain(self):
		return self._prv.getCodomain()

	def getBoundVariable(self):
		return self._prv.getBoundVariable()

	def getGroundSetSize(self, constraints):
		return self._prv.getGroundSetSize(self._constraints.union(constraints))

	def containsTerm(self, t):
		return self._prv.containsTerm(t)

	def applySubstitution(self, s):
		return RandomVariableSet(self._prv.applySubstitution(s), Sets.applySubstitution(s, self._constraints))

	def rename(self):
		raise NotImplementedError()

	def getSumOutCorrection(self, e):
		raise NotImplementedError()

	def getCanonicalForm(self):
		return self._prv.getCanonicalForm()

	# Equality, Hash

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, RandomVariableSet):
			return False
		return self._prv == other._prv and self._constraints == other._constraints

	def __hash__(self):
		constraints = frozenset(self._constraints)
		return hash((self._prv, constraints))

########
# Prvs #
########

def PrvsMgu(prv1, prv2):
	if not Prvs.areUnifiable(prv1, prv2):
		raise IllegalArgumentError

	buffer = Prvs.pushEquations(prv1, prv2)

	mgu = []

	while not not buffer:
		equation = buffer.pop()
		if Prvs.hasIdenticalTerms(equation):
			# Do nothing
			pass
		elif equation.getFirstTerm().isVariable():
			b = equation.toBinding()
			buffer = Prvs.applyBinding(b, buffer)
			mgu.append(b)
		elif equation.getSecondTerm().isVariable():
			b = equation.toInverseBinding()
			buffer = Prvs.applyBinding(b, buffer)
			mgu.append(b)
		else:
			raise IllegalArgumentError()

	result = Substitution(mgu)
	return result

def PrvsAreUnifiable(prv1, prv2):
	same_functor = prv1.getName() == prv2.getName()
	same_number_of_param = len(prv1.getTerms()) == len(prv2.getTerms())
	return same_functor and same_number_of_param

def PrvsPushEquations(prv1, prv2):
	result = []
	for i in range(len(prv1.getTerms())):
		t1 = prv1.getTerms()[i]
		t2 = prv2.getTerms()[i]
		result.append(EqualityConstraint(t1, t2))
	return result

def PrvsHasIdenticalTerms(c):
	return c.getFirstTerm() == c.getSecondTerm()

def PrvsApplyBinding(b, buffer):
	s = Substitution([b])
	for i in range(len(buffer)):
		e = buffer[i]
		buffer[i] = e.applySubstitution(s)
	#for e in buffer:
	#	e = e.applySubstitution(s)
	return buffer

def PrvsAreDisjoint(prv1, prv2):
	'''
	Checks if the specified PRVs are disjoint.

		Parameters
		----------
			prv1 : Prv
			prv2 : Prv

		Returns
		-------
			: bool
	'''
	are_disjoint = False
	all_variables = Lists.union(prv1.getCanonicalForm().getParameters(), prv2.getCanonicalForm().getParameters())

	renamed1 = prv1.applySubstitution(NameGenerator.renameVariables(all_variables))
	renamed2 = prv2.applySubstitution(NameGenerator.renameVariables(all_variables))

	try:
		mgu = Prvs.mgu(renamed1.getCanonicalForm(), renamed2.getCanonicalForm())
		constraints = Sets.union(renamed1.getConstraints(), renamed2.getConstraints())
		if mgu.isEmpty():
			are_disjoint = not renamed1 == renamed2
		else:
			are_disjoint = not mgu.isConsistentWithConstraints(constraints)
	except IllegalArgumentError:
		are_disjoint = True

	return are_disjoint

class Prvs:

	# Constructors
	
	def __init__(self):
		'''
		Constructor of the Prvs class
		'''
		pass

	# static methods
	mgu = staticmethod(PrvsMgu)
	areUnifiable = staticmethod(PrvsAreUnifiable)
	pushEquations = staticmethod(PrvsPushEquations)
	hasIdenticalTerms = staticmethod(PrvsHasIdenticalTerms)
	applyBinding = staticmethod(PrvsApplyBinding)
	areDisjoint = staticmethod(PrvsAreDisjoint)