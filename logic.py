from modules import *
'''
This module handles Classes and methods
to represent those Objects in first order logic
that are needed for FLBNs

    Classes
    -------
        AbstractConstraint
        And
        Binding
        Constant
        Constraint
        EqualityConstraint
        Formula
        Implies
        IneqaulityConstraint
        Not
        Or
        Population
        Prv
        Relation
        Substitution
        Term
        Variable
'''

########
# Term #
########

class Term:
    '''
    Represents a Term in First order logic.
    Can be a Constant or a term.
    This class is supposed to be abstract.
    Any instances of term should be of one of its subclasses.

        Attributes
        ----------
            name : str
                name of the term
    '''

    # Constructor

    __slots__ = ('_name')

    def __init__(self, name):
        '''
        Constructor of the Term class

            Parameters
            ----------
                name : str
                    Name of the term
        '''
        self._name = name

    # Getters

    def getName(self):
        '''
        Returns the name of the Term.

            Returns
            -------
                name : str
                    Name of the constant
        '''
        return self._name

    def getValue(self):
        '''
        This method does the same as getName.
        It exists to prevent sloppy errors during implementation.
        '''
        return self._name

    def isConstant(self):
        '''
        Checks if this Term is a Constant
        '''
        pass

    def isVariable(self):
        '''
        Checks if this Term is a Variable
        '''
        pass

    # Equality, String

    def __eq__(self, other):
        '''
        Checks if two Terms are equal.
        Two terms are equal, if they have the same name.
        Different Terms with the same name are not distinguished.

            Parameters
            ----------
                other : Object
                    The object to compare this Term to

            Returns
            -------
                : bool
                    True, iff this Constant is equal to other.
        '''
        if not isinstance(other, Term):
            return False
        return self._name == other._name

    def __str__(self):
        return self._name

############
# Constant #
############

class Constant(Term):
    '''
    Represents a constant symbol
    in first order logic.

        Attributes
        ----------
            name : str
                Name of the constant.
                Has to be lower case.
    '''

    # Constructor

    __slots__ = ('_name')

    def __init__(self, name):
        '''
        Constructor of the Constant class

            Paramterers
            -----------
                name : str
                    The name of the constant
                    Has to be lower case.

            Raises
            ------
                IllegalArgumentError
                    If name does not start with lower case letter
        '''
        if not name[0].islower():
            raise IllegalArgumentError('name must start with lower case letter')
        super().__init__(name)

    def isConstant(self):
        '''
        Checks if this Term is a Constant

            Returns
            -------
                True : bool
        '''
        return True

    def isVariable(self):
        '''
        Checks if this Term is a Variable

            Returns
            -------
                False : bool
        '''
        return False

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return self._name

##############
# Population #
##############

class Population:
    '''
    A population is a set of individuals.
    Individuals are Constants.

        Attributes
        ----------
            individuals : [ Constant ]  
    '''

    # Constructor

    __slots__ = ('_individuals')

    def __init__(self, individuals=[]):
        '''
        Constructor of the Population class

            Parameters
            ----------
                individuals : [ Constant ]
                    A list of Constants
        '''
        self._individuals = []
        for c in individuals:
            if not c in self._individuals:
                self._individuals.append(c)

    # Iterator

    def __iter__(self):
        '''
        Iterates over population
        '''
        for c in self._individuals:
            yield(c)

    # Getters

    def getIndividualAt(self, index):
        '''
        Returns a copy of an individual from the population

            Parameters
            ----------
                index : int
                    the index of the individual in the population

            Returns
            -------
                : Constant
                    A copy of an individual from the population
        '''
        return copy(self._individuals[index])

    def getSize(self):
        '''
        Returns the number of individuals in the population.

            Returns
            -------
                : int
                    the number of individuals in the population
        '''
        return len(self._individuals)

    def containsIndividual(self, individual):
        '''
        Returns true if the population contains the specified individual.

            Parameters
            ----------
                individual : Constant
                    the individual whose presence in the population is to be tested

            Returns
            -------
                : bool
                    True, iff the population contains the specified individual
        '''
        return (individual in self._individuals)

    def toSet(self):
        '''
        Returns the individuals of the population as a set.

            Returns
            -------
                : { Constant }
                    Set containing the individuals of the population
        '''
        return { individual for individual in self._individuals }

    # Setters

    def remove(self, individual):
        '''
        Removes the individual specified from the population.

            Parameters
            ----------
                individual : Constant
                    the individual to be removed
        '''
        self._individuals.remove(individual)

    # Equality, Hash
    
    def __eq__(self, other):
        if not isinstance(other, Population):
            return False
        if self.getSize() != other.getSize():
            return False
        for i in range(self.getSize()):
            if not self._individuals[i] == other._individuals[i]:
                return False
        return True

    def __hash__(self):
        return hash(self._individuals)

############
# Variable #
############

class Variable(Term):
    '''
    Represents a variable from first order logic.
    Inherits from Term.

        Attributes
        ----------
            name : str
                The name of the variable
            population : Population
                The domain of the Variable
                Represented as a non-empty set of Constants
    '''

    # Constructor

    __slots__ = ('_name', '_population')

    def __init__(self, name, population):
        '''
        Constructor of the variable class

            Parameters
            ----------
                name : str
                    Name of the Variable
                    Must start with upper case
                population : Population
                    Domain of the variable
                    Represented as an instance of population

            Raises
            ------
                IllegalArgumentError
                    If name does not start with upper case letter
                    If domain is empty
        '''
        if not(not name or name[0].isupper()):
            raise IllegalArgumentError('name must start with upper case letter')
        super().__init__(name)
        self._population = population

    # Iterator

    def __iter__(self):
        '''
        Iterates over all constants in domain
        '''
        for C in self._domain:
            yield(C)

    # Getters

    def getPopulation(self):
        '''
        Returns the domain of the Variable.

            Returns
            -------
                domain : { Constant }
                    The domain of the variable
        '''
        return copy(self._population)

    def populationContains(self, C):
        '''
        Checks if a constant C is included in the domain.

            Parameters
            ----------
                C : Constant

            Returns
            -------
                : bool
                    True, iff C is in domain
        '''
        for t in self._population:
            if C == t:
                return True
        return False

    def isConstant(self):
        '''
        Checks if this Term is a Constant

            Returns
            -------
                False : bool
        '''
        return False

    def isVariable(self):
        '''
        Checks if this Term is a Variable

            Returns
            -------
                True : bool
        '''
        return True

    def isEmpty(self):
        return not self._name and self._population.getSize() == 0

    def individualsSatisfyingConstraints(self, constraints):
        '''
        Returns all individuals of the population that
        satisfy the specified set of constraints of the form X != t,
        t constant.

            Parameters
            ----------
                constraints : { Constraint }
                    a set of constraints that restricts the individuals
                    of the population

            Returns
            -------
                : Population
                    set of all individuals satisfying the specified constraint
        '''
        if not constraints:
            return self._population

        pop = Population(copy(self._population._individuals))
        for individual in self._population:
            bind = Binding(self, individual)
            inverse_bind = Binding(individual, self)
            for constraint in constraints:
                if constraint.isUnary() and not constraint.isConsistentWithBinding(bind):
                    pop.remove(individual)
                    break
        return pop

    def rename(self, new_name):
        '''
        Renames this variable.
        A new variable will be created.

            Paramters
            ---------
                new_name : str

            Returns
                : Variable 
        '''
        return Variable(new_name, self._population)

    def excludedSet(self, constraints):
        '''
        Returns the excluded set for this Variable, that is,
        the set of terms t such that (X != t) for all specified constraints.

            Parameters
            ----------
                constraints : { Constraint }
                    a set of InequalityConstraints
            Returns
            -------
                : { Term }
                    excluded set for this variable
        '''
        excluded_set = set()
        for constraint in constraints:
            if constraint.containsTerm(self):
                if self == constraint.getFirstTerm():
                    #if not iterable_contains(excluded_set, constraint.getSecondTerm()): # deprecated
                    if constraint.getSecondTerm() not in excluded_set:
                        excluded_set.add(constraint.getSecondTerm())
                else:
                    #if not iterable_contains(excluded_set, constraint.getFirstTerm()): # deprecated
                    if constraint.getFirstTerm() not in excluded_set:
                        excluded_set.add(constraint.getFirstTerm())
        return excluded_set

    def numberOfIndividualsSatisfyingConstraints(self, constraints):
        '''
            Parameters
            ----------
                constraints : { Constraint }

            Returns
            -------
                : int
        '''
        domain_size = self._population.getSize()
        excluded_set_size = len(self.excludedSet(constraints))
        return domain_size - excluded_set_size

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return self._name

#######
# Prv #
#######

class Prv:
    '''
    Prv stands for parametrized random variable.
    A structure that represents sets of random variables.

    This is an abstract class.
    '''
    def __init__(self):
        pass

    # Getters

    def getConstraints(self):
        '''
        Returns the set of constraints
        associated with this Prv.

            Returns
            -------
                : { Constraint }
        '''
        pass

    def getName(self):
        '''
        Returns the name of the Prv

            Returns
            -------
                : str
        '''
        pass

    def getParameters(self):
        '''
        Returns a list of variables that appear in this Prv

            Returns
            -------
                : [ Variable ] 
        '''
        pass

    def getTerms(self):
        '''
        Returns a list containing the Terms
        that appear in this Prv.

            Returns
            -------
                : [ Term ]
        '''
        pass

    def getCodomain(self):
        '''
        Returns the codomain of the Prv.

            Returns
            -------
                codomain : [ RangeElement ]
        '''
        return copy(self._codomain)

    def getBoundVariable(self):
        '''
        Returns the bound variable of this Prv.

            Returns
            -------
                : Variable
                    Bound Variable of this Prv
        '''
        pass

    def getGroundSetSize(self, constraints):
        '''
        Returns the number of instances satisfying
        the specifed set of constraints.

            Parameters
            ----------
                constraints : { Constraint }
                    a set of constraints

            Returns
            -------
                : int
                    number of instances satisfying the specified set of constraints
        '''
        pass

    def containsTerm(self, t):
        '''
        Returns True, iff the Term specified is present in
        this Prv.

            Parameters
            ----------
                t : Term
                    the term to search for

            Returns
            -------
                True, iff the Prv contains the specified term
        '''
        pass

    def applySubstitution(self, s):
        '''
        Returns an instance of this Prv by applying a substitution.
        The application of a substitution is a Prv that is the original
        Prv with every occurrence Xj replaced by the corresponding tij.

            Parameters
            ----------
                s : Substitution
                    a substitution that will be applied to this Prv

            Returns
            -------
                : Prv
                    the substituted Prv
        '''
        pass

    def rename(self, name):
        '''
        Returns a new Prv with the same codomain and parameters,
        but with the specified name.

            Parameters
            ----------
                name : str
                    the new name

            Returns
            -------
                : Prv
                    this prv renamed
        '''
        pass

    def getSumOutCorrection(self, e):
        '''
        Returns the correction factor used in lifted elimination.

            Parameters
            ----------
                e : The range element in this PRV to be processed

            Returns
            -------
                : Prv
                    The corrected factor used in lifted elimination
        '''
        pass

    def isEquivalentTo(self, s):
        '''
        Returns True if this PRV represents the ssame set of random
        variables in the specified set.

            Parameters
            ----------
                s : RandomVariableSet
                    a set of random variables

            Returns
            -------
                : bool
                    True, iff this PRV represents the same random
                    variables as the specified set
        '''
        pass

    def getCanonicalForm(self):
        '''
        Returns the Std. PRV associated with this PRV.
        If it is a counting formula #.A:C [f], returns f, if it is a random variable set f:C,
        returns f, else it returns itself.

            Returns
            -------
                : Prv
        '''
        pass

###########
# Formula #
###########

class Formula(Prv):
    '''
    Represents a Formula in First order logic.
    Can be a Relation (atomary) or a composed Formula.
    This class is supposed to be abstract.
    Any instances of Formula should be of one of its subclasses.

        Attributes
        ----------
            name : str
                name of the formula
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
    '''

    # Constructor

    __slots__ = ('_name', '_codomain')

    def __init__(self, name):
        '''
        Constructor óf the Formula class

            Parameters
            ----------
                name : str
                    name of the formula
        '''
        self._name = name
        self._codomain = [FALSE, TRUE]

    # Getters

    def getName(self):
        '''
        Returns the name of the Formula

            Returns
            -------
                name : str
                    name of the formula
        '''
        return self._name

    def getBoundVariable(self):
        # Returns an empty variable
        return Variable('', Population())

    def getGroundSetSize(self, constraints):
        size = 1
        for v in self.getParameters():
            size = size * v.individualsSatisfyingConstraints(constraints).getSize()
        return size

    def getSumOutCorrection(self, e):
        return D('1')

    def getCanonicalForm(self):
        return self

    def evaluate(self, s, module):
        '''
        Evaluates the truth value of this Formula
        given a grounding s and an XSB module.

            Parameters
            ----------
                s : Substitution
                    the grounding
                module : str
                    name of an XSB module

            Returns
            -------
                : bool
                    the evaluation of this formula
        '''
        pass

    def evaluateByList(self, variables, truth_values):
        '''
        Evaluates the truth value of this Formula
        given a list of formulas in which this formula
        is assumed to appear and an assignment of truth values
        to this formula, represented by a list phi.

            Parameters
            ----------
                variables : [ Relation ]
                    A list of Relations
                phi : [ bool ]
                    A list of truth values

            Returns
            -------
                : bool
                    the truth value of this
                    formula
        '''
        pass

    def copy(self):
        '''
        Returns a copy of this formula.

            Returns
            -------
                : Formula
                    a copy of this formula
        '''
        pass

    # Setters

    def replaceTerm(self, to_replace, replacement):
        '''
        Replaces all occurrences of the term to_replace
        by replacement in the list of terms.

        If the term does not exist, nothhing is done.

            Parameters
            ----------
                to_replace : Term
                    term to replace
                
                replacement : Term
                    the term that will replace the term
        '''
        pass

    def getConstraints(self):
        return set()

    def getRelativeTrueGroundings(self, s, module):
        '''
        Returns the quotient of the amount of true groundings
        of this Formula and the amount of total possible groundings.

            Parameters
            ----------
                s : Substitution
                    a partial grounding
                module : str
                    the XSB module to consult

            Returns
            -------
                : float
        '''
        grounding = copy(self).applySubstitution(s)
        
        # Compute denominator i.e.
        # number of total possible groundings
        total_groundings = 1.0
        # List difference with empty list to get rid of dublicates
        parameters = Lists.difference(grounding.getParameters(), [])
        for param in parameters:
            total_groundings *= param.getPopulation().getSize()

        # Compute numerator i.e.
        # number of true groundings
        true_groundings = 0
        l = []
        for param in parameters:
            m = []
            for c in param.getPopulation():
                m.append([param, c])
            l.append(m)
        product = list(itertools.product(*l))

        bind_list = []
        for pair in product:
            bindings = []
            for m in pair:
                bindings.append(Binding(m[0], m[1]))
            bind_list.append(bindings)

        for bindings in bind_list:
            #for b in bindings:
            #    print(b.getFirstTerm().getName(), b.getSecondTerm().getName())
            sub = Substitution(bindings)
            if grounding.evaluate(sub, module):
                true_groundings += 1

        return true_groundings / total_groundings

############
# Relation #
############

class Relation(Formula):
    '''
        Represents a Relational symbol in first order logic.

        Attributes
        ----------
            name : str
                name of the Relation
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
            terms : [ Term ]
                list of terms
                representing the terms of the Relation
            arity : int
                length of terms,
                representing the arity of the relation
    '''

    # Constructor

    __slots__ = ('_name', '_codomain', '_terms', '_arity')

    def __init__(self, name, terms=[]):
        '''
        Constructor of the Relation class

            Parameters
            ----------
                name : str
                    name of the relation

                terms : [ Term ]
                    terms of the relation
        '''
        #if not name[0].islower():
        #    raise IllegalArgumentError('name should start with a lower case letter')
        super().__init__(name)
        self._terms = terms
        self._arity = len(terms)

    # Iterator

    def __iter__(self):
        '''
        Iterates over all terms
        '''
        for t in self._terms:
            yield(t)

    # Getters

    def getTerms(self):
        '''
        Returns the terms of the Relation

            Returns
            -------
                terms : [ Term ]
                    terms of the relation
        '''
        return copy(self._terms)

    def getParameters(self):
        '''
        Returns a list of all free variables of the formula

            Returns
            -------
                param : [ Variable ]
        '''
        param = []
        for t in self._terms:
            if t.isVariable():
                param.append(t)
        return param

    def containsTerm(self, t):
        # TODO: Careful! Deviates slightly from original
        for term in self._terms:
            if t == term:
                return True
        return False

    def getArity(self):
        '''
        Returns the arity of the Relation

            Returns
            -------
                arity : int
                    arity of the Relation
        '''
        return self._arity

    def getTermAt(self, i):
        '''
        Returns the i-th Term of the Relation

            Parameters
            ----------
                i : int
                    The postion of the term to get
                    Must not be less then 0 or larger than arity-1
            
            Returns
            -------
                terms[i] : Term

            Raises
            ------
                IllegalArgumentError
                    if i < 0 or i > arity - 1
        '''
        if i < 0 or i > self._arity - 1:
            raise IllegalArgumentError('argument out of bounds')
        return self._terms[i]

    def evaluate(self, s, module):
        grounding = copy(self).applySubstitution(s)

        names = []
        for t in grounding.getTerms():
            names.append(t.getName())

        # If xsb does not know this Relation,
        # then it will raise a SystemError.
        # We catch it and set this evaluation
        # up to be False.

        # TODO: The above only works once!
        # If the same module is consulted in the same setting
        # (which will happen in the loop in getRelativeTrueGroundings)
        # then the program will crash BADLY.
        # Figure out why this is and fix it!
        try:
            result = px_cmd(module, self._name, *names)
        except SystemError:
            result = 0
        return result == 1

    def evaluateByList(self, variables, truth_values):
        #index = get_index_of_iterable(variables, self) # deprecated
        index = variables.index(self)
        if index == -1:
            raise IllegalArgumentError('A relation does not appear in the specified variables')
        return truth_values[index]

    def copy(self):
        return Relation(self._name, copy(self._terms))

    # Setters

    def applySubstitution(self, s):
        substituted = Relation(self._name, copy(self._terms))
        #substituted = copy(self)
        for to_replace in s:
            replacement = s.getReplacement(to_replace)
            substituted.replaceTerm(to_replace, replacement)
        return substituted

    def replaceTerm(self, to_replace, replacement):
        while self.containsTerm(to_replace):
            substituted_index = self._terms.index(to_replace)
            #substituted_index = get_index_of_iterable(self._terms, to_replace) # deprecated
            self._terms[substituted_index] = replacement

    def rename(self, name):
        return Relation(name, copy(self._terms))

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        if self._arity != other._arity:
            return False
        if not self._terms == other._terms:
            return False
        return self._name == other._name

    def __hash__(self):
        return hash((self._arity, *self._terms, self._name))

    def __str__(self):
        result = self._name + '('
        for term in self._terms:
            result = result + term.getName() + ', '
        result = result.rstrip(', ')
        result += ')'
        return result

#######
# Not #
#######

class Not(Formula):
    '''
    Represents a Negation in first order logic
    Inherits from Formula

        Attributes
        ----------
            A : Formula
                the negated formula
            name : str
                name of the negation
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
    '''

    # Constructor

    __slots__ = ('_A', '_name')

    def __init__(self, A):
        '''
        Constructor of the Not class

            Parameters
            ----------
                A : Formula
                    the negated Formula
        '''
        name = '!' + A.getName()
        super().__init__(name)
        self._A = A       

    # Getters

    def getA(self):
        '''
        Returns the negated formula

            Returns
            -------
                A : Formula
                    the negated formula
        '''
        return self._A

    def getTerms(self):
        return self._A.getTerms()

    def getParameters(self):
        '''
        Returns a list of all free variables of the formula

            Returns
            -------
                : [ Variable ]
                    Paramters of A
        '''
        return self._A.getParameters()

    def containsTerm(self, t):
        return self._A.contains(t)

    def copy(self):
        return Not(self._A.copy())

    # Setters

    def applySubstitution(self, s):
        return Not(self._A.applySubstitution(s))

    def replaceTerm(self, to_replace, replacement):
        self._A.replaceTerm(to_replace, replacement)

    def rename(self, name):
        return Not(name, self._A)

    def evaluate(self, s, module):
        return not self._A.evaluate(s, module)

    def evaluateByList(self, variables, truth_values):
        return not self._A.evaluateByList(variables, truth_values)

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self._name == other._name and self._A == other._A

    def __hash__(self, other):
        return hash((self._name, self._A))

    def __str__(self):
        return self._name

######
# Or #
######

class Or(Formula):
    '''
    Represents a Disjunction of Formulas in first order logic
    Inherits from Formula

        Attributes
        ----------
            A : Formula
                first (left) argument of the disjunction 
            B : Formula
                second (right) argument of the disjunction
            name : str
                name of the disjunction
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
    '''

    # Constructor

    __slots__ = ('_A', '_B', '_name')

    def __init__(self, A, B):
        '''
        Constructor of the Or class

            Parameters
            ---------
                A : Formula
                    first (left) argument of the disjunction 
                B : Formula
                    second (right) argument of the disjunction
        '''
        name = '(' + A.getName() + ' || ' + B.getName() + ')'
        super().__init__(name)
        self._A = A
        self._B = B   

    # Getters

    def getA(self):
        '''
        Returns the first argument of the disjunciton

            Returns
            -------
                A : formula
                    first (left) argument of the disjunction 
        '''
        return self._A

    def getB(self):
        '''
        Returns the second argument of the disjunciton

            Returns
            -------
                B : formula
                    second (right) argument of the disjunction 
        '''
        return self._B

    def getTerms(self):
        return self._A.getTerms() + self._B.getTerms()

    def getParameters(self):
        '''
        Returns a list of all free variables of the formula

            Returns
            -------
                : [ Variable ]
                    Paramters of A + B
        '''
        return self._A.getParameters() + self._B.getParameters()

    def containsTerm(self, t):
        return self._A.contains(t) or self._B.contains(t)

    def evaluate(self, s, module):
        return self._A.evaluate(s, module) or self._B.evaluate(s, module)

    def evaluateByList(self, variables, truth_values):
        return self._A.evaluateByList(variables, truth_values) or self._B.evaluateByList(variables, truth_values)

    def copy(self):
        return Or(self._A.copy(), self._B.copy())

    # Setters

    def applySubstitution(self, s):
        return Or(self._A.applySubstitution(s), self._B.applySubstitution(s))

    def replaceTerm(self, to_replace, replacement):
        self._A.replaceTerm(to_replace, replacement)
        self._B.replaceTerm(to_replace, replacement)

    def rename(self, name):
        return Or(name, self._A, self._B)

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        return self._name == other._name and self._A == other._A and self._B == other._B

    def __hash__(self):
        return hash((self._name, self._A, self._B))

    def __str__(self):
        return self._name

#######
# And #
#######

class And(Formula):
    '''
    Represents a Conjunction of Formulas in first order logic
    Inherits from Formula

        Attributes
        ----------
            A : Formula
                first (left) argument of the conjunction 
            B : Formula
                second (right) argument of the conjunction
            name : str
                name of the conjunction
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
    '''

    # Constructor

    __slots__ = ('_A', '_B', '_name')

    def __init__(self, A, B):
        '''
        Constructor of the And class

            Parameters
            ----------
                A : Formula
                    first (left) argument of the conjunction 
                B : Formula
                    second (right) argument of the conjunction
        '''
        name = '(' + A.getName() + ' && ' + B.getName() + ')'
        super().__init__(name)
        self._A = A
        self._B = B

    # Getters

    def getA(self):
        '''
        Returns the first argument of the conjunciton

            Returns
            -------
                A : formula
                    first (left) argument of the conjunction 
        '''
        return self._A

    def getB(self):
        '''
        Returns the second argument of the conjunciton

            Returns
            -------
                B : formula
                    second (right) argument of the conjunction 
        '''
        return self._B

    def getTerms(self):
        return self._A.getTerms() + self._B.getTerms()

    def getParameters(self):
        '''
        Returns a list of all free variables of the formula

            Returns
            -------
                : [ Variable ]
                    Paramters of A + B
        '''
        return self._A.getParameters() + self._B.getParameters()

    def containsTerm(self, t):
        return self._A.contains(t) or self._B.contains(t)

    def evaluate(self, s, module):
        return self._A.evaluate(s, module) and self._B.evaluate(s, module)

    def evaluateByList(self, variables, truth_values):
        return self._A.evaluateByList(variables, truth_values) and self._B.evaluateByList(variables, truth_values)

    def copy(self):
        return And(self._A.copy(), self._B.copy())

    # Setters

    def applySubstitution(self, s):
        return And(self._A.applySubstitution(s), self._B.applySubstitution(s))

    def replaceTerm(self, to_replace, replacement):
        self._A.replaceTerm(to_replace, replacement)
        self._B.replaceTerm(to_replace, replacement)

    def rename(self, name):
        return And(name, self._A, self._B)

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        return self._name == other._name and self._A == other._A and self._B == other._B

    def __hash__(self):
        return hash((self._name, self._A, self._B))

    def __str__(self):
        return self._name

###########
# Implies #
###########

class Implies(Formula):
    '''
    Represents an Implication of Formulas in first order logic
    Inherits from Formula

        Attributes
        ----------
            A : Formula
                Premise (left argument) of the implication
            B : Formula
                Conclusion (right argument) of the implication
            name : str
                name of the implication
            codomain : [ RangeElement ]
                Range of values that this formula can take
                (Always Bool for us)
    '''

    # Constructor

    __slots__ = ('_A', '_B', '_name')

    def __init__(self, A, B):
        '''
        Constructor of the Implies class

            Parameters
            ----------
                A : Formula
                    Premise (left argument) of the implication 
                B : Formula
                    Conclusion (right argument) of the implication 
        '''
        name = '(' + A.getName() + ' => ' + B.getName() + ')'
        super().__init__(name)
        self._A = A
        self._B = B

    # Getters

    def getA(self):
        '''
        Returns the premise of the implication

            Returns
            -------
                A : formula
                    premise of the implication
        '''
        return self._A

    def getB(self):
        '''
        Returns the conclusion of the implication

            Returns
            -------
                B : formula
                    conclusion of the implication 
        '''
        return self._B

    def getTerms(self):
        return self._A.getTerms() + self._B.getTerms()

    def getParameters(self):
        '''
        Returns a list of all free variables of the formula

            Returns
            -------
                : [ Variable ]
                    Paramters of A + B
        '''
        return self._A.getParameters() + self._B.getParameters()

    def containsTerm(self, t):
        return self._A.contains(t) or self._B.contains(t)

    # Setters

    def applySubstitution(self, s):
        return Implies(self._A.applySubstitution(s), self._B.applySubstitution(s))

    def replaceTerm(self, to_replace, replacement):
        self._A.replaceTerm(to_replace, replacement)
        self._B.replaceTerm(to_replace, replacement)

    def rename(self, name):
        return Implies(name, self._A, self._B)

    def evaluate(self, s, module):
        return (not self._A.evaluate(s, module)) or self._B.evaluate(s, module)

    def evaluateByList(self, variables, truth_values):
        return (not self._A.evaluateByList(variables, truth_values)) or self._B.evaluateByList(variables, truth_values)

    def copy(self):
        return Implies(self._A.copy(), self._B.copy())

    # Equality, Hash, Str

    def __eq__(self, other):
        if not isinstance(other, Implies):
            return False
        return self._name == other._name and self._A == other._A and self._B == other._B

    def __hash__(self):
        return hash((self._name, self._A, self._B))

    def __str__(self):
        return self._name

###########
# Binding #
###########

class Binding:
    '''
    A binding is an ordered pair of terms (t1, t2). The first term (t1)
    must be a Variable and the second term (t2) may be a Constant or a Variable.

        Attributes
        ----------
            firstTerm : Variable
            secondTerm : Term
    '''

    # Constructor

    __slots__ = ('_firstTerm', '_secondTerm')

    def __init__(self, t1, t2):
        '''
        Constructor of the Binding class

            Parameters
            ----------
                t1 : Variable
                t2 : Term
        '''
        self._firstTerm = t1
        self._secondTerm = t2

    # Getters

    def getFirstTerm(self):
        '''
        Returns the first Term of this Binding.

            Returns
            -------
                firstTerm : Variable
        '''
        return self._firstTerm

    def getSecondTerm(self):
        '''
        Returns the second Term of this Binding.

            Returns
            -------
                secondTerm : Term
        '''
        return self._secondTerm

    def containsTerm(self, t):
        '''
        Returns True, if this binding contains the specified term.

            Parameters
            ----------
                t : Term

            Returns
            -------
                : bool
                    True, iff this binding contains the specified term.
        '''
        return (t == self._firstTerm) or (t == self._secondTerm)

    def isValid(self):
        '''
        Returns True, if
        The second Term is a Constant and it belongs to first term's population.
        The second Term is a Variable and both terms have the same population.

            Returns
            -------
                : bool
                    True iff the second term is in first term's population
                    or if second term and first term have the same population.
        '''
        isValid = False
        if self._secondTerm.isConstant():
            isValid = self._firstTerm.getPopulation().containsIndividual(self._secondTerm)
        else:
            isValid = (self._firstTerm.getPopulation() == self._secondTerm.getPopulation())
        return isValid

    def toInequalityConstraint(self):
        '''
        Returns this binding converted to InequalityConstraint
            Returns
            -------
                : InequalityConstraint
                    this binding converted to InequalityConstraint
        '''
        return InequalityConstraint(self._firstTerm, self._secondTerm)

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, Binding):
            return False
        return self._firstTerm == other._firstTerm and self._secondTerm == other._secondTerm

    def __hash__(self):
        return hash((self._firstTerm, self._secondTerm))

################
# Substitution #
################

class Substitution:
    '''
    Represents a substitution in first order logic.

        Attributes
        ----------
            bindings : { Variable : Term }
                dictionary representing a mapping from a variable
                to a term
    '''

    # Constructors

    __slots__ = ('_bindings')
    
    def __init__(self, bindings=[]):
        '''
        Constructor of the Substitution class

            Parameters
            ----------
                bindings : [ Binding ]
                    A list of Bindings
        '''
        self._bindings = {}
        for binding in bindings:
            self.addBinding(binding)

    def addBinding(self, b):
        '''
        Adds a new binding to this substitution

            Parameters
            ----------
                b : Binding

            Raises
            ------
                IllegalArgumentError
                --------------------
                    If the first term in this substitution is already replaced
        '''
        if b.getFirstTerm() in self._bindings.keys():
            raise IllegalArgumentError(b.getFirstTerm() + ' is already being replaced')
        self._bindings[b.getFirstTerm()] = b.getSecondTerm()

    # Iterator

    def __iter__(self):
        '''
        Iterates over the keys in the bindings
        of this Substitution
        '''
        for key in self._bindings.keys():
            yield(key)

    # Getters

    def getVariables(self):
        '''
        Returns a set containing all the variables that are in the first
        element of each binding in this substitution.

            Returns
            -------
                : { Variable }
        '''
        return set(self._bindings.keys())

    def getReplacement(self, substituted):
        '''
        Returns the replacement of a given logical variable in this substitution.
        i.e. if the substituion is given by [X/Y, Z/r], then calling this method with 'X'
        will return 'Y'.

            Parameters
            ----------
                substituted : Variable
                    the variable being substituted

            Returns
            -------
                : Term
                    the replacement of a given variable in this substitution
        '''
        for key in self._bindings.keys():
            if key == substituted:
                return self._bindings[key]

    # renamed from contains()
    def containsBinding(self, binding):
        '''
        Checks, if this substitution contains the specified binding.

            Parameters
            ----------
                binding : Binding
                    the binding to search for

            Returns
            -------
                : bool
                    True, iff this substitution contains the specified binding
        '''
        key = binding.getFirstTerm()
        if key in self._bindings.keys():
            return (self._bindings[key] == binding.getSecondTerm())
        return False

    # renamed from contains()
    def containsVariable(self, replaced):
        '''
        Checks if there is any binding in this substitution
        that replaces the specified variable.

            Parameters
            ----------
                replaced : Variable
                    the variable being replaced to search for

            Returns
            -------
                : bool
                    True iff any binding in this substitution replaces
                    the specified variable

        '''
        # TODO: Warning, deviates from original
        for v in self._bindings.keys():
            if v == replaced:
                return True
        return False
        #return replaced in self._bindings.keys()

    def hasTerm(self, t):
        '''
        Checks if any binding in this substitution
        contains the specified term.

            Parameters
            ----------
                t : Term
                    the term to search for

            Returns
            -------
                : bool
                    True iff 
        '''
        return t in self._bindings.keys() or t in self._bindings.values()

    def hasCommonReplacement(self, first_variable, second_variable):
        '''
        Checks if the specified variables have the same replacement.

            Parameters
            ----------
                first_variable : Variable
                second_variable : Variable

            Returns
            -------
                : bool
                    True iff the specified variables
                    have a common replacement
        '''
        if first_variable in self._bindings.keys() and second_variable in self._bindings.keys():
            return (self._bindings[first_variable] == self._bindings[second_variable])
        else:
            return False

    def isEmpty(self):
        '''
        Checks if there are no elements in this substitution.
            
            Returns
            -------
                True iff bindings is empty
        '''
        return not self._bindings

    def isUnifier(self, prv1, prv2):
        '''
        Checks if this substitution unifies the specified Prv.

        A substitution is a unifier of two Prvs
        r(ti1,...,tik), r(tj1,...,tjk) if
        r(ti1,...,tik)[&theta] = r(tj1,...,tjk)[&theta]
        We then say that thw two Prvs unify.

            Parameters
            ----------
                prv1 : Prv
                prv2 : Prv

            Returns
            -------
                : bool
                    True iff this substitution
                    unifies the specified Prvs
        '''
        # TODO: Input will be substituted (side-effect), is this correct?
        #       It is how it is done in Java implementation
        return (prv1.applySubstitution(self) == prv2.applySubstitution(self))

    def getSize(self):
        '''
        Returns the number of bindings in this substitution.

            Returns
            -------
                : int
                    the number of bindings in this substitution
        '''
        return len(self._bindings)

    def asList(self):
        '''
        Converts this substitution to a list if Bindings

            Returns
            -------
                binds : [ Binding ]
                    this substitution as a list of bindings
        '''
        binds = []
        for t1 in self._bindings.keys():
            b = Binding(t1, self._bindings[t1])
            binds.append(b)
        return binds

    def getFirstBinding(self):
        '''
        Retrives, but does not remove, the first Binding
        in this substitution, throwing an exception if this is empty.

            Returns
            -------
                : Binding
                    first binding in this substitution

            Raises
            ------
                ValueError
                    If this substitution is empty     
        '''
        if not self._bindings:
            raise ValueError()
        else:
            return self.asList()[0]

    def isConsistentWithConstraints(self, constraints):
        '''
        Checks if this substitution is consistent with the specified set
        of constraints.

        A substitution is consistent with a set of constraints when applying
        the former to the latter generates only valid expressions.

            Parameters
            ----------
                constraints : { Constraint }
                    the set of constraints to test this substitution against

            Returns
            -------
                : bool
                    True iff this substitution is consisten with the
                    specified set of constraints
        '''
        size = 0
        for constraint in constraints:
            try:
                constraint.applySubstitution(self)
                size += 1
            except IllegalArgumentError:
                # ignore invalid constraints
                pass
            except ValueError:
                # takes into account valid Constant-only constraints
                size += 1
        return len(constraints) == size

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, Substitution):
            return False
        if self.getSize() != other.getSize():
            return False
        if self._bindings != other._bindings:
            return False
        #for t in self._bindings.keys():
        #    if not other.containsVariable(t):
        #        return False
        #for t in self._bindings.keys():
        #    for u in other._bindings.keys():
        #        if t.equals(u) and not self._bindings[t].equals(other.getReplacement(u)):
        #            return False
        return True

    def __hash__(self):
        return hash(self._bindings)

##############
# Constraint #
##############

class Constraint:
    '''
    Represents a constraint for the C-FOVE algorithm-
    Abstract class, can be either InequalityConstraint
    or EqualityConstraint.

    Constraints are of the form X = Y or X != Y
    '''

    # Constructor

    def __init__(self):
        '''
        Constructor of the Constraint class
        '''
        pass

    def getFirstTerm(self):
        '''
        Returns the left term in this constraint.

            Returns
            -------
                : Term
                    the left term in this constraint
        '''
        pass

    def getSecondTerm(self):
        '''
        Returns the right term in this constraint.

            Returns
            -------
                : Term
                    the right term in this constraint
        '''
        pass

    def applySubstitution(self, s):
        '''
        Applies the substitution in this constraint.

        Parameters
        ----------
            s : Substitution
                the substitution to apply to this constraint

        Returns
        -------
            The constraint that results from applying the
            specified substitution to this constraint

        Raises
        ------
            IllegalArgumentError
                if the resulting constraint is always false
            ValueError
                if the resulting constraint involves only constants
        '''
        pass

    def containsTerm(self, t):
        '''
        Checks if the specified Term is in this constraint

            Parameters
            ----------
                t : Term
                    the specified term

            Returns
            -------
                : bool
                    True iff the specified term equals one of
                    the terms in this constraint
        '''
        pass

    def hasCommonTerm(self, c):
        '''
        Checks if this constraint and the specified constraint
        have a common term.

            Parameters
            ----------
                c : Constraint
                    the constraint to compare to

            Returns
            -------
                : bool
                    True iff this constraint and the specified constraint
                    have a common term
        '''
        pass

    def isConsistentWithBinding(self, b):
        '''
        Checks if the specified Binding satisfies this
        constraint, i.e. returns True if applying
        the specified binding to this constraint results in a valid sentece.

        Also returns False when it is not possible to
        evaluate whether the resulting constraint is valid or not.

        For instance, let  X, Y, W, Z be variables with common population
        {a, b, ..., z}, then:
        X != a is consistent with X/B (because b != a is true)
        X != Y is consistent with W/Z (because X != Y is still true)
        X != a is not consistent with X/a (because a != a is not true)
        X != a is not consistent with W/W (because W != a is not necessarily true)
        X != Y is not consistent with X/W (because W != Y is not necassarily true)

        Parameters
        ----------
            b : Binding
                the binding to test

        Returns
        -------
            : bool
                True iff this constraint is consistent
                with the specified binding
        '''
        pass

    def toBinding(self):
        '''
        Returns the Binding corresponding to this constraint,
        i.e. if this constraint is t1 != t2 then this method
        returns Binding(t1, t2)

            Returns
            -------
                : Binding
                    the binding corresponding to this constraint

            Raises
            ------
                IllegalArgumentError
                    If the first term is not a variable
        '''
        pass

    def toInverseBinding(self):
        '''
        Returns the Binding obtained by inverting the terms if this
        constraint.

            Returns
            -------
                : Binding
                    the inverse binding corresponding
                    to this constraint

            Raises
            ------
                IllegalArgumentError
                    if the second term is not a variable
        '''
        pass

    def isUnary(self):
        '''
        checks if this constraint is unary, that is, if
        it is composed by a variable and a constant.

            Returns
            -------
                : bool
                    True iff this constraint is unary
        '''
        pass

    def getVariables(self):
        '''
        Returns a set containing all variables in this constraint.
        '''
        pass

######################
# AbstractConstraint #
######################

class AbstractConstraint(Constraint):
    '''
    This class represents constraints of the form X ? Y, where
    X and Y are Terms and ? is either = or !=

    Constraints with two constants are invalid.
    If a method detects an invalid constraint, it returns None.

        Attributes
        ----------
            firstTerm : Term
            secondTerm : Term
    '''

    # Getters

    def getFirstTerm(self):
        return self._firstTerm

    def getSecondTerm(self):
        return self._secondTerm

    def containsTerm(self, term):
        return (self._firstTerm == term) or (self._secondTerm == term)

    def hasCommonTerm(self, constraint):
        return (self._firstTerm == constraint.getFirstTerm()) or (self._firstTerm == constraint.getSecondTerm()) or (self._secondTerm == constraint.getFirstTerm()) or (self._secondTerm == constraint.getSecondTerm())    

    def toBinding(self):
        return Binding(self._firstTerm, self._secondTerm)

    def toInverseBinding(self):
        return Binding(self._secondTerm, self._firstTerm)

    def getBinding(self, t1, t2):
        '''
        Creats a Binding with the specified Terms.

            Parameters
            ----------
                t1 : Term
                t2 : Term

            Returns
            -------
                : Binding
                    the binding t1/t2

            Raises
            ------
                ValueError
                    if t1 is not a variable
        '''
        if t1.isVariable():
            return Binding(t1, t2)
        else:
            raise ValueError()

    def isUnary(self):
        return (self._firstTerm.isVariable() and self._secondTerm.isConstant()) or (self._firstTerm.isConstant() and self._secondTerm.isVariable())

    def getVariables(self):
        logical_variables = set()
        if self._firstTerm.isVariable():
            logical_variables.add(self._firstTerm)
        if self._secondTerm.isVariable():
            logical_variables.add(self._secondTerm)
        return logical_variables

########################
# InequalityConstraint #
########################

class InequalityConstraint(AbstractConstraint):
    '''
    This class represents inequality constraints of the form X != Y
    where X and Y are terms.

    Inequalities with two constants are invalid.
    '''
    
    # Constructor

    __slots__ = ('_firstTerm', '_secondTerm')

    def __init__(self, t1, t2):
        '''
        Constructor of the InequalityConstraint class

            Parameters
            ----------
                t1 : Term
                    left side of the constraint
                t2 : Term
                    right side of the constraint

            Raises
            ------
                IllegalArgumentError
                    if t1 and t2 are equal
                ValueError
        '''
        if t1 == t2:
            raise IllegalArgumentError()
        if t1.isVariable() or t2.isVariable():
            self._firstTerm = t1
            self._secondTerm = t2
        else:
            raise ValueError()

    def applySubstitution(self, s):
        t1 = self._firstTerm
        t2 = self._secondTerm
        for replaced in s:
            if replaced == t1:
                t1 = s.getReplacement(replaced)
            if replaced == t2:
                t2 = s.getReplacement(replaced)
        return InequalityConstraint(t1, t2)

    def isConsistentWithBinding(self, b):
        is_consistent = False
        if self._firstTerm.isVariable() and self._secondTerm.isVariable():
            is_consistent = False
        else:
            if self.isApplicable(b):
                if b.getSecondTerm().isVariable():
                    is_consistent = False
                else:
                    c = InequalityConstraint(self._firstTerm, self._secondTerm)
                    c._firstTerm = b.getSecondTerm()
                    is_consistent = not (c._firstTerm == c._secondTerm)
            else:
                is_consistent = True
        return is_consistent

    def isApplicable(self, b):
        '''
        Checks if the specified binding can be applied in this
        constraint.

            Parameters
            ----------
                b : Binding
                    the binding to test applicability

            Returns
            -------
                : bool
                    True iff the specified binding can be applied
                    in this constraint.
        '''
        return self.containsTerm(b.getFirstTerm())

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, InequalityConstraint):
            return False
        direct = (self._firstTerm == other._firstTerm) and (self._secondTerm == other._secondTerm)
        inverse = (self._firstTerm == other._secondTerm) and (self._secondTerm == other._firstTerm)
        return direct or inverse

    def __hash__(self):
        return hash((self._firstTerm, self._secondTerm))

######################
# EqualityConstraint #
######################

class EqualityConstraint(AbstractConstraint):
    '''
    This class represents equations of the form ti = tj, where
    ti and tj are parameters of a PRV.

    This class is used in the algorithmto find the MGU between two
    PRVS.

        Attributes
        ----------
            firstTerm : Term
            secondTerm : Term
    '''

    # Constructor

    __slots__ = ('_firstTerm', '_secondTerm')

    def __init__(self, t1, t2):
        '''
        Constructor of the EqualityConstraint class

            Parameters
            ----------
                t1 : Term
                    the left side of the constraint
                t2 : Term
                    the right side of the constraint
        '''
        self._firstTerm = t1
        self._secondTerm = t2

    def applySubstitution(self, s):
        t1 = self._firstTerm
        t2 = self._secondTerm
        for replaced in s:
            if replaced == t1:
                t1 = s.getReplacement(replaced)
            if replaced == t2:
                t2 = s.getReplacement(replaced)
        return EqualityConstraint(t1, t2)

    def isConsistentWithBinding(self, b):
        raise NotImplementedError()

    # Equality, Hash

    def __eq__(self, other):
        if not isinstance(other, InequalityConstraint):
            return False
        direct = (self._firstTerm == other._firstTerm) and (self._secondTerm == other._secondTerm)
        inverse = (self._firstTerm == other._secondTerm) and (self._secondTerm == other._firstTerm)
        return direct or inverse

    def __hash__(self):
        return hash((self._firstTerm, self._secondTerm))