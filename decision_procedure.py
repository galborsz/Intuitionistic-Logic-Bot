from tree_node import TreeNode
import string

# global variables
alphabet = list(string.ascii_lowercase)
connectives = ['⊐', '∧', '∨', '∼']

class Formula:
    def __init__(self, tree, world, assignation):
        self.tree = tree
        self.world = world
        self.assignation = assignation

class Interpretation:
    def __init__(self):
        self.removable_formulas = []
        self.permanent_formulas = []
        self.worlds = 0
        self.relations = set()
        self.valuations = {}
        self.used_relations = set()
        self.tautology_world_generator_present = False
        self.world_generator_present = False

    def add_removable_formula(self, formula):
        if formula not in self.removable_formulas:
            self.removable_formulas.append(formula)
    
    def add_permanent_formula(self, formula):
        if formula not in self.permanent_formulas:
            self.permanent_formulas.append(formula)
    
    def add_world(self):
        self.worlds += 1
        # reflexive rule applied every time a new world is introduced
        for i in range(self.worlds+1):
            self.add_relation(i, i)
    
    def add_relation(self, first_world, second_world):
        self.relations.add(tuple([first_world, second_world]))
    
    # for keeping track of the relations already used by the permanent formulas
    def add_used_relation(self, first_world, second_world):
        self.used_relations.add(tuple([first_world, second_world]))
        
    def add_valuation(self, variable, world, value):
        if (variable, world) in self.valuations:
            if self.valuations[(variable, world)] != value: # contradiction
                return False
        else:
            self.valuations[(variable, world)] = value
            return True

# create initial list of the tableau
def create_initial_tableau_node(formula):
    tableau_node = Interpretation()
    tableau_node.add_removable_formula(Formula(formula, 0, False))
    return tableau_node

def copy_interpretation(old_interpretation):
    new_interpretation = Interpretation()
    new_interpretation.removable_formulas = old_interpretation.removable_formulas.copy()
    new_interpretation.permanent_formulas = old_interpretation.permanent_formulas.copy()
    new_interpretation.relations = old_interpretation.relations.copy()
    new_interpretation.used_relations = old_interpretation.used_relations.copy()
    new_interpretation.worlds = old_interpretation.worlds
    new_interpretation.tautology_world_generator_present = old_interpretation.tautology_world_generator_present
    new_interpretation.world_generator_present = old_interpretation.world_generator_present
    new_interpretation.valuations = old_interpretation.valuations.copy()
    return new_interpretation

# application of the tableau rules
def rules(old_interpretation, formula, connective, interpretations):
    if connective == '⊐' and formula.assignation == False:
        if old_interpretation.permanent_formulas and decision_procedure(formula.tree) == True: # if world generator is a tautology, there won't be an infinite branch
            old_interpretation.tautology_world_generator_present = True
        elif old_interpretation.permanent_formulas and decision_procedure(formula.tree) == False:
            old_interpretation.world_generator_present = True
        old_interpretation.add_removable_formula(Formula(formula.tree.left, old_interpretation.worlds + 1, True))
        old_interpretation.add_removable_formula(Formula(formula.tree.right, old_interpretation.worlds + 1, False))
        old_interpretation.add_relation(formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_world()
        interpretations.append(old_interpretation)
        return interpretations
         
    elif connective == '⊐' and formula.assignation == True:
        old_interpretation.add_permanent_formula(formula)
        new_interpretation = copy_interpretation(old_interpretation)

        # determine possible accessible worlds not used before
        possible_relations = set()
        for relation in old_interpretation.relations:
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    possible_relations.add(relation)
        
        # not possible to extend permanent formulas so it is not a tautology
        if not possible_relations:
            return False

        for relation in possible_relations:
            old_interpretation.add_used_relation(relation[0], relation[1])
            new_interpretation.add_used_relation(relation[0], relation[1])
            old_interpretation.add_removable_formula(Formula(formula.tree.left, relation[1], False))
            new_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], True))
        interpretations.append(old_interpretation)
        interpretations.append(new_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == True: 
        old_interpretation.add_permanent_formula(formula)
        
        # determine possible accessible worlds not used before
        possible_relations = set()
        for relation in old_interpretation.relations:
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    possible_relations.add(relation)
        
        # not possible to extend permanent formulas so it is not a tautology
        if not possible_relations:
            return False

        for relation in possible_relations:
            old_interpretation.add_used_relation(relation[0],  relation[1])
            old_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], False))
        interpretations.append(old_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == False:
        if old_interpretation.permanent_formulas and decision_procedure(formula.tree) == True: # if world generator is a tautology, there won't be an infinite branch
            old_interpretation.tautology_world_generator_present = True
        elif old_interpretation.permanent_formulas and decision_procedure(formula.tree) == False:
            old_interpretation.world_generator_present = True
        old_interpretation.add_removable_formula(Formula(formula.tree.right, old_interpretation.worlds + 1, True))
        old_interpretation.add_relation(formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_world()
        interpretations.append(old_interpretation)
        return interpretations
    
    elif connective == '∧' and formula.assignation == True:
        old_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        old_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, True))
        interpretations.append(old_interpretation)
        return interpretations

    elif connective == '∧' and formula.assignation == False:
        new_interpretation = copy_interpretation(old_interpretation)
        old_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, False))
        interpretations.append(old_interpretation)
        interpretations.append(new_interpretation)
        return interpretations

    elif connective == '∨' and formula.assignation == True:
        new_interpretation = copy_interpretation(old_interpretation)
        old_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, True))
        interpretations.append(old_interpretation)
        interpretations.append(new_interpretation)
        return interpretations

    elif connective == '∨' and formula.assignation == False:
        old_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        old_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, False))
        interpretations.append(old_interpretation)
        return interpretations

# application of the transitivity and heredity rules, as well as extension of the permanent formulas if necessary
def no_more_formulas(old_interpretation, interpretations):
    new_transitivity_relations = []
    # transitivity rule
    for first_relation in old_interpretation.relations:
        if first_relation[0] != first_relation[1]:
            first = first_relation[1]
            for second_relation in old_interpretation.relations:
                if second_relation[0] != second_relation[1]:
                    if first == second_relation[0]:
                        new_transitivity_relations.append(tuple([first_relation[0], second_relation[1]]))
                        first = second_relation[1]
    
    for relation in new_transitivity_relations:
        old_interpretation.add_relation(relation[0], relation[1])

    # heredity rule
    variables = []
    worlds = []
    for valuation in old_interpretation.valuations:
        for relation in old_interpretation.relations:
            if valuation[1] == relation[0] and relation[0] != relation[1] and old_interpretation.valuations[valuation] == True:
                variables.append(valuation[0])
                worlds.append(relation[1])
    
    # try to find contradiction
    for variable, world in zip(variables, worlds):
        added = old_interpretation.add_valuation(variable, world, True)
        if added == False:
            return interpretations # the branch is closed, so we can get rid of it
    

    # apply rule again to permanent formulas (only if there are relations that have not been applied yet)
    for formula in old_interpretation.permanent_formulas:
        possible_relations = set()
        for relation in old_interpretation.relations:
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    possible_relations.add(relation)
        
        if possible_relations:
            if old_interpretation.tautology_world_generator_present:
                return interpretations # branch closed bc world generator is a tautology

            # if there is no tautological world generator, check whether there are still removable formulas to work with
            # if it was not infinite, it would have closed already
            elif not old_interpretation.removable_formulas and old_interpretation.world_generator_present:
                return False # infinite branch, not a tautology
            return rules(old_interpretation, formula, formula.tree.data, interpretations)
    
    return False # no contradiction found, so it is not a tautology

def apply_procedure(interpretations):
    old_interpretation = interpretations.pop()
    if old_interpretation.removable_formulas:
        formula = old_interpretation.removable_formulas.pop(0)
        connective = formula.tree.data
        if connective in connectives: # apply rule assigned to connective
            return rules(old_interpretation, formula, connective, interpretations)
    
        elif connective in alphabet: # no connective left, add valuations
            added = old_interpretation.add_valuation(connective, formula.world, formula.assignation)
            if added == False:
                return interpretations # the branch is closed, so we can get rid of it
            interpretations.append(old_interpretation)
            return interpretations
        else:
            print("wrong notation")
            return False

    else: # no more formulas, apply transitivity rule, then heredity rule and finally permanent formulas
        return no_more_formulas(old_interpretation, interpretations)
        
def decision_procedure(tree):
    interpretations = [] #stack
    initial_node = create_initial_tableau_node(tree)
    interpretations.append(initial_node)
    while interpretations:
        interpretations = apply_procedure(interpretations)
        if interpretations == False: # process should stop because the branch is open
            return False # it is not a tautology
        elif not interpretations:
            return True # it is a tautology
        # process should continue, but this interpretation should not be in the list anymore

    return True # it is a tautology