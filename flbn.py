from modules import *
'''
This module handles Functional Lifted Bayesian Networks (short FLBNs).

	Classes
	-------
		Groundings
		FlbnNode	
'''

def create_FLBN(V):
	'''
	Creates the first layer of a Functional Lifted Bayesian Network
	(i.e. the 'root'-nodes) from a collection of FlbnNodes V.

		Paramters
		---------
			V :
				an iterable collection of FlbnNodes

		Returns
		-------
			G : nx.DiGraph
				A graph containing the given nodes
				and no edges
	'''
	G = nx.DiGraph()
	for v in V:
		G.add_node(v)
	return G

def add_to_FLBN(G, w, V):
	'''
	Adds a node and edges to a given FLBN G.
	The way this is set up makes sure that G is acyclical and undirected.

		Parameters
		----------
			G : nx.DiGraph
				The graph to which w is to be added
			w : FlbnNode
				the node which we wish to add to G
			V :
				an iterable collection of FlbnNodes
				from which edges are to be added to w
				(pointing from a v in V to w)
	'''
	G.add_node(w)
	for v in V:
		G.add_edge(v, w)

def generate_truth_table(n):
	'''
	This method creates a table in form of a n x 2**n matrix,
	representing all possible assignments of truth values
	to n propositional variables.

	This will be used as a reference for the potential
	when converting an FLBN node to a parfactor.

	REMARK: This function was written with the help
	of ChatGPT.

		Paramters
		---------
			n : int
				the amount of propositional
				variables

			Returns
			-------
				table : [ [ bool ] ]
					a matrix of boolean values
	'''
	if n <= 0:
		return [[]]

	table = []
	for i in range(2**n):
		binary_repr = bin(i)[2:].zfill(n)
		row = [bool(int(bit)) for bit in binary_repr]
		table.append(row)

	return table

def get_values(node, variables):
	'''
	This method returns the correct values
	for a Parfactor in a FLBN.

		Parameters
		----------
			node : FlbnNode
				the node which we wish to transform
				into a parfactor
			variables : [ Prv ]

		Returns
		-------
			: [ Decimal ]
	'''
	prv = node.getR()
	parents = variables[1:]
	size = len(parents)
	truth_table = generate_truth_table(size)
	false_results = []
	true_results = []
	for truth_values in truth_table:
		arguments = []
		for formula in node.getFormulas():
			# We do the same trick as in node_to_parfactor
			# to get a list of all possible groundings that do
			# not involve free variables in the node.
			params_to_substitute = Lists.intersection(prv.getParameters(), formula.getParameters())
			bind_list = []
			for t in params_to_substitute:
				bind_list.append(Binding(t, next(iter(t.getPopulation()))))
			s = Substitution(bind_list)
			substituted = formula.applySubstitution(s)
			groundings = Groundings(substituted)
			numerator = 0
			denominator = len(list(groundings))
			if denominator != 0:
				for grounding in groundings:
					t = Substitution(grounding)
					to_test = formula.applySubstitution(t)
					if to_test.evaluateByList(parents, truth_values):
						numerator += 1
				arguments.append(D(numerator/denominator))
			else:
				arguments.append(int(formula.evaluateByList(parents, truth_values)))
		probability = node._f(arguments)
		false_results.append(D('1') - D(probability))
		true_results.append(D(probability))

	return false_results + true_results
		
def node_to_parfactor(G, node):
	'''
	Returns the parfactor corresponding to a node
	for the C-FOVE algorithm.

		Parameters
		----------
			G : nx.DiGraph
				A graph containing node
			node : FlbnNode
				the node which we wish to transform
				into a parfactor

		Returns
		-------
			: StdParfactor
				the parfactor corresponding to the node
	'''
	prv = node.getR()
	# We create the list of variables (i.e. prvs) for
	# our parfactor
	variables = [prv]
	for parent in G.predecessors(node):
		to_add = parent.getR()
		# We get a list of all parameters of prv
		# that also appear in to_add.
		params_to_substitute = Lists.intersection(prv.getParameters(), to_add.getParameters())
		# We get a list of bindings from all common variables in bind_list
		# to its first possible substitution.
		# This is a trick, so we can later create a substitution that does not
		# involve these variables.
		bind_list = []
		for t in params_to_substitute:
			bind_list.append(Binding(t, next(iter(t.getPopulation()))))
		s = Substitution(bind_list)
		substituted = to_add.applySubstitution(s)
		groundings = Groundings(substituted)
		for grounding in groundings:
			t = Substitution(grounding)
			variables.append(to_add.applySubstitution(t))

	values = get_values(node, variables)

	result = StdParfactorBuilder().addVariables(variables).addValues(values)
	return result.build()

def get_parfactors(G, node):
	'''
	Iteratively transforms a graph G into a set of
	parfactors.
	More precicely: Starting with the given node,
	it recursively creates a set of parfactors for the
	smallest subgraph H of the given graph G ending in
	the given node.

		Parameters
		----------
			G : nx.DiGraph
				the graph containing the node
				for context
			node : FlbnNode
				The child node defining the subgraph
				of G that we wish to trasnform into parfactors

		Returns
		-------
			parfactors : { StdParfactor }
				A set of parfactors representing H
	'''
	parfactors = set()
	parfactors.add(node_to_parfactor(G, node))
	parents = list(G.predecessors(node))
	if parents:
		for parent in G.predecessors(node):
			parfactors = Sets.union(get_parfactors(G, parent), parfactors)
	return parfactors

def query(G, node):
	'''
	Queries the probability of the given node
	in the given graph G using the CFOVE algorithm.

		Parameters
		----------
			G : nx.DiGraph
				The graph containing the node
				we wish to query
			node : FlbnNode
				The node we wish to query

		Returns
		-------
			probability : Decimal
				the probability that the
				given node is true
	'''
	parfactors = get_parfactors(G, node)
	query_predicate = node.getR()
	rvs = RandomVariableSet(query_predicate, set())
	input1 = StdMarginalBuilder().setParfactors(parfactors).setPreservable(rvs).build()
	cfove = CFOVE(input1)
	result = cfove.run()
	#probability = result.getFactor().getValues()[1]
	return result

##############
# Groundings #
##############

class Groundings:
	'''
	The main purpose of this class is
	to provide an iterator that yields
	all possible groundings of a Formula p.

	Technically, p is assumed to contain only
	free variables, but the iterator should work
	for partially grounded Formulas as well.

	Remark: This class has been relocated from learning.py,
	as it is already needed in flbn.py.

		Attributes
		----------
			p : Formula
				the formula we wish to iterate over
			bindList : [ [ Binding ] ]
				list of all possible groundings of p
				in the form of lists of bindings.
	'''

	# Constructor

	__slots__ = ('_p', '_bindList')

	def __init__(self, p):
		'''
		Constructor of the groundings class

			Parameters
			----------
				p : Formula
					the formula we wish to iterate over
		'''
		self._p = p
		self._bindList = []

		# list difference with empty list
		# to get rid of dublicates.
		parameters = Lists.difference(p.getParameters(), [])

		l = []
		for param in parameters:
			m = []
			for c in param.getPopulation():
				m.append([param, c])
			l.append(m)
		product = list(itertools.product(*l))

		for pair in product:
			bindings = []
			for m in pair:
				bindings.append(Binding(m[0], m[1]))
			self._bindList.append(bindings)

	# Iterator

	def __iter__(self):
		'''
		Iterates over all allowed groundings of p.
		Groundings are returned in the form of
		lists of bindings.
		'''
		for bindings in self._bindList:
			yield(bindings)

############
# FlbnNode #
############

class FlbnNode:
	'''
	Represents a node in a Functional Lifted Bayesian Network

		Attributes
		----------
			r : Relation
				A relation of first order logic
			formulas : [ Formulas ]
				A list of formulas
			length : int
				The length of formulas
			f :
				A function from [0,1]^length to [0,1]
			name : str
				name of the node
	'''
	
	# Constructor

	__slots__ = ('_r', '_formulas', '_length', '_f', '_name')

	def __init__(self, r, formulas=[], f=lambda x : 0):
		'''
		Constructor of the FlbnNode Class

			Paramters
			---------
				r : Relation
					A relation of first order logic
				formulas : [ Formula ]
					A list of formulas
				n : int
					The length of formulas
				f :
					A function from [0,1]^{n} to [0,1]
		'''
		# TODO: Make sure that all atoms in formulas are parents of r
		# TODO: Make sure f has the correct domain and codomain
		self._r = r
		self._formulas = copy(formulas)
		self._length = len(formulas)
		self._f = f
		self._name = r.getName()

	# Iterator

	def __iter__(self):
		'''
		Iterates over the list of formulas
		'''
		for p in self._formulas:
			yield(p)

	# Getters

	def getR(self):
		'''
		Returns the Relation belonging to the node

			Returns
			-------
				r : Relation
					the relation belonging to the node
		'''
		return self._r

	def getFormulas(self):
		'''
		Returns the list of formulas
			
			Returns
			-------
				formulas : [ Formula ]
		'''
		return self._formulas

	def getLength(self):
		'''
		Returns the length of the list of formulas

			Returns
			-------
				length : int
		'''
		return self._length

	def getName(self):
		'''
		Returns the name of the node

			Returns
			-------
				name : str
					name of the node
		'''
		return self._name

	def getFormulaAt(self, i):
		'''
		Returns the formula at index i

			Returns
			-------
				formulas[i] : Formula
					The i-th entry of the list of formulas

			Raises
			------
				IllegalArgumentError
					If i < 0 or i > length-1
		'''
		if i < 0 or i > self._length - 1:
			raise IllegalArgumentError('argument out of bound')
		return self._formulas[i]

	def evalF(self, *arg):
		'''
		Evaluates the function f belonging to this node
		on the argument arg

			Parameters
			----------
				arg : [ float ]
					List of floats
					Must be of length 'length'

			Returns
			-------
				f(*arg) : float

			Raises
			------
				IllegalArgumentError
					If len(arg) != length
		'''
		if len(arg) != self._length:
			raise IllegalArgumentError('argument has wrong length')
		return self._f(arg)

	def probability(self, s, module, assignment=[]):
		'''
		Computes the probability of this node,
		given a grounding s. s must contain Bindings
		for all variables, appearing in r and none else.

			Parameters
			----------
				s : Substitution
					grounding of all variables in r
				module : str
					the XSB module that will be consulted
				assignment : [ bool ]
					a list of boolean values, used to
					reference an assignment of truth values
					to the parents of this node.
					This is used for setting up the potential
					for the C-FOVE algorithm.

			Returns
			-------
				: float
					probability of r[s]

			Raises 
			------
				IllegalArgumentError
					If s does not contain Bindings for
					all variables in r or if s contains
					bindings of variables that are not in r.
		'''
		param = self._r.getParameters()
		keys = s.getVariables()
		if set(param) != set(keys):
			raise IllegalArgumentError('Substitution must contain exactly the variables in r and none other')

		grounding = copy(self._r).applySubstitution(s)
		argument = []

		# If our assignment is empty or None,
		# we just compute the probability regularily.
		# Otherwise, we compute adapted probabilities for every
		# entry of the list, to represent the potential in the
		# parfactors of the C-FOVE algorithm.
		if not assignment:
			for p in self._formulas:
				argument.append(p.getRelativeTrueGroundings(s, module))
		else:
			size = len(self._formulas)
			for i in range(size):
				quotient = self._formulas[i].getRelativeTrueGroundings(s, module)
				if assignment[i+1]:
					argument.append(quotient)
				else:
					argument.append(1-quotient)

			# If the first entry of assignments
			# is False, we return 1 - f(argument) to
			# reflect the opposite probability
			# Otherwise, the rest of the method will do
			# the correct job.
			if not assignment[0]:
				return 1.0 - self._f(argument)

		#if not argument:
		#	return 1.0

		return self._f(argument)

	# Equality, hash, String

	def __eq__(self, other):
		# TODO: Prevent same relation with different other parameters
		# TODO: Check equality for funciton
		if self is other:
			return True
		if not isinstance(other, FlbnNode):
			return False
		return self._length == other._length and self._formulas == other._formulas and self._r == other._r

	def __hash__(self):
		return hash(self._r)

	def __str__(self):
		return self._name