from modules import * 
'''
This modules provides classes and methods
for the training of an FLBN.

	Classes
	-------
		ParametrizedFlbnNode
'''

def rbn_distribution(structure, nodes, parameters):
	'''
	Returns the RBN distribution of a given data set
	accodring to Jaeger's paper and simultaneously updates
	the parameters of the nodes to the given parameters.

	The parameter list must be of the correct formfor the nodes.
	If the nodes are [n1, ..., nm] and the parameters are
	[w1, ..., wk], then if the first node has i formulas,
	the the first i+1 parameters belong to n1, the next
	parameter w(i+2), ..., w(i+2+j+1) belong to n2, if 
	n2 has j formulas and so on.
	The correct parameters for the nodes are infered
	using the counter below.

		Parameters
		----------
			structure : str
				An interpretation of a FO-language
				in form of the name of an XSB module
				Keep in mind that the entries of 
				'structure.P' must have the correct form!
			nodes : [ ParametrizedFlbnNode ]
				a list of FlbnNodes
			parameters : np.array, torch.tensor
				Parameters on which to
				compute the likelihood

		Returns
		-------
			: float
	'''
	result = 1.0

	counter = 0
	for i in range(len(nodes)):
		# We need to find the correct parameters
		# for the i-th node. That's what the counter is for.
		size = nodes[i].getLength() + 1
		for grounding in Groundings(nodes[i].getR()):
			s = Substitution(grounding)

			#probability = nodes[i].probability(s, structure, parameters[counter : counter + size])

			# Remark: The following two commands yield the same result, as the commented
			# out command above, which invokes the overwriting probability method
			# in ParametrizedFlbnNode (which is atm also commented out).
			# This suggests, that updating the parameters at a node does not
			# seem to "mess up" the automically computed gradient in pytorch.
			nodes[i].updateParameters(parameters[counter : counter + size])
			probability = nodes[i].probability(s, structure)
			if nodes[i].getR().evaluate(s, structure):
				result = result * probability
			else:
				result = result * (1 - probability)
		counter = counter + size

	return result

def likelihood(data, nodes, parameters):
	'''
	Computes the likelihood of a RBN
	according to Jaeger's paper and updates
	the parameters of the nodes.

		Parameters
		----------
			data : [ str ]
				list of structures
				represented as names
				of XSB modules
			nodes : [ FlbnNode ]
				list of FLBN nodes
			parameters : np.array, torch.tensor
				Parameters on which to
				compute the likelihood

		Returns
		-------
			: float
	'''
	result = 1.0
	_count = 0

	for structure in data:
		# If we have only one module, we will assume
		# that it has already been consulted by a calling function.
		# Otherwise, we need to consult it now.
		if len(data) > 1:
			consult(structure)
		result = result * rbn_distribution(structure, nodes, parameters)

	return result

def initialize_weights(size):
	'''
	Initializes the weights of a
	parametrized FLBN node.

	This will also set the data type of the weights.
	Currently it is set to be torch.float64
	
	For now, they will all be initialized
	with 0.5

		Parameters
		----------
			size : size of weight vector

		Returns
		-------
			result : torch.tensor
				tensor with initialized weights
	'''
	result = torch.tensor([0.5 for i in range(size)], dtype=torch.float64, requires_grad=True)
	return result

def update_multiple_parameters(nodes, parameters):
	'''
	Updates the weights of the given nodes
	with the give parameters according to the same
	order as in likelihood, gradient.

	The method directliy modifies the nodes and as
	such does not return anything

		Parameters
		----------
			nodes : [ ParametrizedFlbnNode ]
			parameters : [ float ], torch.Tensor, np.array
	'''

	counter = 0
	for i in range(len(nodes)):
		# We need to find the correct parameters
		# for the i-th node. That's what the counter is for.
		size = nodes[i].getLength() + 1
		nodes[i].updateParameters(parameters[counter : counter + size])
		counter = counter + size

def gradient_descent(data, nodes, lr=0.1, threshold=0.0000000001, loss=nn.MSELoss(), n_iters=0):
	'''
	The complete gradient descent learning algorithm
	for FLBNs

		Paramteres
		----------
			data : [ str ]
				list of XSB modules from
				which to learn
			nodes : [ ParametrizedFlbnNode ]
				list of FlbnNodes on which
				to learn
			lr : float
                learning rate
            threshold : float
            	the maximum squared difference between
            	consequtive weights, at which the learning
            	stops.
            	Note: With mean squared error as metric,
            	threshold right now needs to be very small.
            loss : function
            	metric to determine, when to consecutive
            	parameter vectors are close
            n_iters : int
            	Maximum number of iterations.
            	If learning does not converge, it will break
            	after this amount of iterations.
            	If n_iters <= 0, the loop wil potentially run forever
	'''
	# Get the correct length for the weights
	length = 0
	for node in nodes:
		length += (node.getLength() + 1)

	# Initialize weights
	w = initialize_weights(length)

	# If we have only one module,
	# We only need to consult it once, so we do it here
	if len(data) == 1:
		consult(next(iter(data)))

	epoch = 0
	print('\n')
	while(True):
		# We optimize the log likelikhood, as likelihood values
		# were so small that weights never update.
		L = -torch.log(likelihood(data, nodes, w))
		L.backward()

		with torch.no_grad():
			w_star = deepcopy(w)
			w -= lr * w.grad

			# Determine the distance between to consecutive
			# Parameter vectors.
			dist = loss(w, w_star).item()

		# TODO: Rewrite or comment out below command
		#		when testing with multiple value tensors!
		print(f'epoch {epoch+1}, w = {w.tolist()}, loss = {dist}')
		w.grad.zero_()

		# If distance between consecutive parameter vectors is
		# smaller than set threshold, we stop.
		if dist < threshold:
			break

		epoch += 1
		if n_iters > 0 and epoch >= n_iters:
			print('\nWARNING! Gradient descend did not converge!\n')
			break

	# TODO: The below command to update the parameters may not be necessary,
	#		as the weights now get automatically updated by the rbn_distribution
	#		method. However it does not hurt, so I'll leave it here for now.
	update_multiple_parameters(nodes, w)

########################
# ParametrizedFlbnNode #
########################

class ParametrizedFlbnNode(FlbnNode):
	'''
	A special case of an FLBN-node,
	where the probability function f
	is of the form
	sigmoid(w0 + x1*w1 + ... + xn*wn)
	for parameters w0, w1, ..., wn
	and inputs x1, ..., xn.

		Attributes
		----------
			r : Relation
			formulas : [ Formula ]
			f : function
				f(x1,...,xn) = sigmoid(w0 + w1*x1 + ... + wn*xn)
			parameters : torch.tensor( [ float ] )
	'''

	# Constructor

	__slots__ = ('_r', '_formulas', '_parameters', '_f')

	def __init__(self, r, formulas, parameters):
		'''
		Constructor of the ParametrizedFlbnNode class

			Parameters
			----------
				r : Relation
				formulas : [ Formula ]
				parameters : torch.tensor( [ float ] )
		'''
		super().__init__(r, formulas, self.f)
		self.updateParameters(parameters)

	def fWithParameters(self, arguments, parameters):
		'''
		The parametrized probability function belonging
		to this node.

			Parameters
			----------
				arguments : [ float ], np.array, torch.Tensor

			Returns
			-------
				: float
		'''
		result = parameters[0]
		for i in range(len(arguments)):
			result = result + parameters[i+1] * arguments[i]
			
		# If parameters are a torch tensor, then we want
		# to use the pytorch implementation of sigmoid, so 
		# we can do a backward propagation later on.
		# Otherwise, we use our own implementation.
		if isinstance(parameters, torch.Tensor):
			return torch.sigmoid(result)
		return sigmoid(result)

	def f(self, arguments):
		'''
		The parametrized probability function belonging
		to this node.

			Parameters
			----------
				arguments : [ float ], np.array, torch.Tensor

			Returns
			-------
				: float
		'''	
		#result = self._parameters[0]
		#for i in range(len(arguments)):
		#	result = result + self._parameters[i+1] * arguments[i]
		#return sigmoid(result)
		return self.fWithParameters(arguments, self._parameters)

	# Getters

	def getParameters(self):
		'''
		Returns a copy of the parameters
		of this node.

			Returns
			-------
				paramters : float
		'''

		# Not copying is important here, since we want
		# the parameters to retain the gradient!
		return self._parameters

	def getParameterAt(self, i):
		'''
		Returns the parameter of this node
		at the specified index i.

			Parameters
			----------
				i : int

			Returns
			-------
				parameters[i] : float
		'''

		# Not copying is important here, since we want
		# the parameters to retain the gradient!
		return self._parameters[i]

	# Remark: Currently, we do not want to overwrite the probability method
	# to remain compatibile with C-FOVE.
	# This might change later, so for now this method is just commented out.

	#def probability(self, s, module, parameters):
	#	param = self._r.getParameters()
	#	keys = s.getVariables()
	#	if not iterables_contain_same_elements(param, keys):
	#		raise IllegalArgumentError('Substitution must contain exactly the variables in r and none other')
	#
	#	grounding = copy(self._r).applySubstitution(s)
	#	argument = []
	#	for p in self._formulas:
	#		argument.append(p.getRelativeTrueGroundings(s, module))
	#	if not argument:
	#		return 1.0
	#	return self.fWithParameters(argument, parameters)

	# Setters

	def updateParameters(self, parameters):
		'''
		Sets the list of parameters of this node
		to the list of parameters specified in the
		argument. Is alo used ofr initialization of
		this node.

			Parameters
			----------
				paramters : [ float ]
		'''
		if not len(parameters) == len(self._formulas) + 1:
			raise IllegalArgumentError('parameters must be of the size of formulas + 1')
		#self._parameters = copy(parameters)

		# Not copying is important here, since we want
		# the parameters to retain the gradient!
		self._parameters = parameters

	def setParameterAt(self, i, w):
		'''
		Replaces a single parameter at the specified
		index with the specified parameter w.

			Parameters
			----------
				i : int
					the specified index
				w : float
					the specified parameter
		'''

		# Not copying is important here, since we want
		# the parameters to retain the gradient!		
		self._parameters[i] = w

	# Equality, hash, String

	def __eq__(self, other):
		if self is other:
			return True
		if not isinstance(other, ParametrizedFlbnNode):
			return False
		return self._length == other._length and self._formulas == other._formulas and self._parameters == other._parameters

	def __hash__(self):
		return hash(self._r)

	def __str__(self):
		return self._name