from modules import *
'''
	Classes
	-------
		Bool
		Lists
		MathUtils
		Multinomial
		RangeElement
		Sets
'''

def product(x):
	'''
	Returns the product of a list of numbers x

		Parameters
		----------
			x :
				a list of numbers of any type

		Returns
		-------
			the product of all numbers in x
	'''
	result = 1
	for t in x:
		result *= t
	return result

def sigmoid(x):
	'''
	Implementation of Sigmoid function
		
		Parameters
		----------
			x : float

		Returns
		-------
			sigmoid(x) : float
	'''
	return 1 / (1 + math.exp(-x))

def D_sigmoid(x):
	'''
	Computes the derivative of the sigmoid
	function.

		Parameters
		----------
			x : float

		Returns
		-------
			d/dx sigmoid(x) : float
	'''
	return sigmoid(x) * (1 - sigmoid(x))

def sigmoid_product(x):
	'''
	Product of n sigmoid functions on a list x
	of length n.
	Largely for testing purposes.

		Parameters
		----------
			x : [ float ]
				List of floats

		Returns
		-------
			result : float
				result = sigmoid(x[0]) * ... * sigmoid(x[n-1])
	'''
	result = 1.0
	for y in x:
		result *= sigmoid(y)
	return result

#########
# Lists #
#########

def ListsUnion(list1, list2):
	result = []
	# TODO: Checks by equals
	#		Leave this comment here just in case.
	for elem in list1:
		if elem not in result:
			result.append(elem)
	for elem in list2:
		if elem not in result:
			result.append(elem)
	return result

def ListsDifference(list1, list2):
	'''
	Returns the difference of two lists.
	Duplicates are eliminated and order may
	not be preserved.
	'''
	result1 = set(list1)
	result2 = set(list2)
	result = Sets.difference(result1, result2)
	return(list(result))

def ListsIntersection(list1, list2):
	'''
	Returns the intersection of two lists.
	Dublicates are eliminated.
	Order of first list is preserved.
	Order of second list may not be preserved.
	'''
	result = []
	for element in list1:
		if element in list2 and element not in result:
			result.append(element)
	return result

def ListsSameElements(list1, list2):
	if len(list1) != len(list2):
		return False
	set1 = set(list1)
	set2 = set(list2)
	return set1.issubset(set1) and set2.issubset(s1)

def ListsApplySubstitution(s, list1):
	replaced = []
	for element in list1:
		try:
			replaced.append(element.applySubstitution(s))
		except IllegalArgumentError:
			pass
		except ValueError:
			pass
	return replaced

def ListsReplace(list1, to_replace, replacement):
	replaced = copy(list1)
	index = list1.index(to_replace)
	if index != -1:
		replaced[index] = replacement
	return replaced

class Lists:

	 # Constructor

	 def __init__(self):
	 	'''
	 	Constructor of the Lists class
	 	'''
	 	pass

	 # static methods
	 union = staticmethod(ListsUnion)
	 difference = staticmethod(ListsDifference)
	 intersection = staticmethod(ListsIntersection)
	 sameElements = staticmethod(ListsSameElements)
	 applySubstitution = staticmethod(ListsApplySubstitution)
	 replace = staticmethod(ListsReplace)

########
# Sets #
########

def SetsApplySubstitution(s, set1):
	'''
	Returns the result of applying the specified substitution
	to the elements of the specified set.

	If the result of a substitution is invalid,
	it is not added to the result.

		Parameters
		----------
			s : Substitution
				the substitution to be made
			set1 : set
				set containing the elements to be substituted.

		Returns
		-------
			replaced : set
				the result of applying the specified substitution
				to the elements of the specified set
	'''
	replaced = set()
	for element in set1:
		try:
			# TODO: checks for equals
			#		Better keep this comment.
			substituted = element.applySubstitution(s)
			if substituted not in replaced:
				replaced.add(element.applySubstitution(s))
		except IllegalArgumentError:
			# not added
			pass
		except ValueError:
			# not added
			pass
	return replaced

def SetsDifference(set1, set2):
	'''
	Computes the difference of two sets, where elements
	are compared by the equals method.

		Parameters
		----------
			set1 : set
			set2 : set

		Returns
		-------
			: set
				set1 - set2
	'''
	result = set()
	for obj in set1:
		if obj not in set2:
			result.add(obj)
	return result

def SetsUnion(set1, set2):
	# TODO: Checks by equals
	#		Leave this comment here just in case.
	result = set()
	for elem in set1:
		if elem not in result:
			result.add(elem)
	for elem in set2:
		if elem not in result:
			result.add(elem)
	return result

class Sets:

	# Constructor

	def __init__(self):
		'''
		Constructor of the Sets class
		'''
		pass

	# static methods

	applySubstitution = staticmethod(SetsApplySubstitution)
	difference = staticmethod(SetsDifference)
	union = staticmethod(SetsUnion)

###############
# Multinomial #
###############

class Multinomial:
	'''
		Attributes
		----------
			mult : [ int ]
	'''

	# Constructors

	__slots__ = ('_multi')

	def __init__(self, m):
		'''
		Constructor of the Multinomial class

			Parameters
			----------
				m : [ int ]
		'''
		self._multi = m

	def getSize(self):
		return len(self._multi)

	def get(self, index):
		return self._multi[index]

	def decrement(self, index):
		'''
		Subtracts 1 from the number at the specified position.

			Parameters
			----------
				index : int
					index to decrement

			Returns
			-------
				: Multinomial
					this multinomial with the specified
					position decremented
		'''
		decremented = copy(self._multi)
		decremented[index] = decremented[index] - 1
		return Multinomial(decremented)

	def isValid(self):
		'''
		Checks if this Multinomial has only positive values.

			Returns
			-------
				: bool
					True, iff this Multinomial has only positive values
		'''
		for i in self._multi:
			if i < 0:
				return False
		return True

	def isZeroed(self):
		'''
		Checks if this Multinomial only has zero values.

			Returns
			-------
				: bool
					True, iff this Multinomial only has zero values
		'''
		for i in self._multi:
			if i != 0:
				return False
		return True

	def sumTerms(self, from_index, to_index):
		'''
		Sums all terms in the specified interval.
		That includes both parameters.

			Parameters
			----------
				from_index : int
				to_index : int

			Return
			------
				result : int
					sum of all terms in the
					specified intervall
		'''
		result = 0
		for i in range(from_index, to_index + 1):
			result += self._multi[i]
		return result

	# Equality

	def __eq__(self, other):
		if not isinstance(other, Multinomial):
			return False
		if self._multi != other._multi:
			return False
		return True

#############
# MathUtils #
#############

def MathUtilsCombination(n, k):
	'''
	Calculates the binomial coefficient C(n,k).

		Parameters
		----------
			n : int
				nonnegative integer
			k : int
				nonnegative integer

		Returns
		-------
			r : int
				C(n,k)

		Raises
		------
			IllegalArgumentError
				if arguments are negative
	'''
	if n < 0 or k < 0:
		raise IllegalArgumentError('Cannot calculate combination for negative numbers.')
	if n == 0:
		return 0
	r = 1
	m_minus_k = n - k
	for i in range(1, k+1):
		r = int((r * (m_minus_k + i)) / i)
	return r

def MathUtilsMultinomial(m):
	'''
	Calculates the Multinomial coefficients.

		Parameters
		----------
			m : Multinomial

		Returns
		-------
			result : int
				value of the specified multinomial
	'''
	result = 1
	if m.getSize() < 2 or m.isZeroed():
		result = 1
	else:
		for i in range(1, m.getSize()):
			n = m.sumTerms(0, i)
			k = m.get(i)
			c = MathUtils.combination(n, k)
			result = result * c
	return result

def MathUtilsPow(b, p, q):
	'''
	Returns the result of b^(p/q) as
	Decimal.
	Not defined for negative numbers.

		Parameters
		----------
			b : Decimal
				base
			p : int
				numerator of the exponent
			q : int
				denominator of the exponent

		Returns
		-------
			result : Decimal
				b^(p/q)

		Raises
		------
			IllegalArgumentError
				if b = 0 and n < 0
				if (b < 0 or p*q < 0) and p % q != 0
	'''
	sign = p * q
	if b == 0:
		if sign > 0:
			result = D('0')
		elif sign == 0:
			result = D('1')
		else:
			raise IllegalArgumentError('0^n, n < 0 is undefined!')
	elif b < 0 or sign < 0:
		if p % q == 0:
			exp = int(p / q)
			result = b ** exp
		else:
			raise IllegalArgumentError('Operation not defined for negative numbers')
	else:
		int_part = int(p / q)
		dec_part = p / q - int_part
		int_pow = b ** D(int_part)
		dec_pow = b ** D(dec_part)

		result = int_pow * dec_pow
	MathUtils.calls += 1
	return result

class MathUtils:
	'''
		Attributes
		----------
			calls : int
				Class attribute
			cache : { Multinomial : int }
				Class Attribute
				Cache for Multinomial calculation
				All calculated multinomials are cached in order
				to improve efficiency.
	'''

	# Constructors

	def __init__(self):
		'''
		Constructor of the MathUtils class
		'''
		pass

	# Class Attributes
	
	calls = 0
	cache = {} 

	# Static Methods

	combination = staticmethod(MathUtilsCombination)
	multinomial = staticmethod(MathUtilsMultinomial)
	mathUtilsPow = staticmethod(MathUtilsPow) # Has to be this clunky name because pow is reserved in Python.

################
# RangeElement #
################

class RangeElement:
    '''
    Represents elements from Formula ranges.
    This is an abstract class.
    No Instance of RangeElement should be created.
    '''

    # Constructors

    def __init__(self):
        pass

########
# Bool #
########

class Bool(RangeElement):
    '''
    Represents boolean values, wrapping the bool type.
    Inherits from RangeElement

        Attributes
        ----------
            value : bool
    '''

    # Constructors

    __slots__ = ('_value')

    def __init__(self, value):
        '''
        Constructor of the Bool class

            Parameters
            ----------
                value : bool
        '''
        self._value = value

    # Getters

    def getValue(self):
        '''
        Returns the value

            Returns
            -------
                value : bool
        '''
        return self._value

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, Bool):
            return False
        return self._value == other.getValue()

    def __hash__(self):
    	return hash(self._value)

FALSE = Bool(False)
TRUE = Bool(True)