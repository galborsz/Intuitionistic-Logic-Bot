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
        self.worlds = 0 # use it as a counter instead of as a list
        self.relations = set()
        self.valuations = {}
        self.used_relations = set()
        self.world_generator_present = False

    def add_removable_formula(self, formula):
        if formula not in self.removable_formulas:
            self.removable_formulas.append(formula)
    
    def add_permanent_formula(self, formula):
        if formula not in self.permanent_formulas:
            #print("adding: ")
            #formula.tree.inorder()
            #print(" ", formula.world, " \n")
            self.permanent_formulas.append(formula)
        #else:
            #print("not added: ")
            #formula.tree.inorder()
            #print(" ", formula.world, " \n")
    
    def add_world(self):
        self.worlds += 1
        # reflexive rule applied every time a new world is introduced
        for i in range(self.worlds+1):
            self.add_relation(i, i)
    
    def add_relation(self, first_world, second_world):
        self.relations.add(tuple([first_world, second_world]))
        #if tuple([first_world, second_world]) not in self.relations:
            #self.relations.append(tuple([first_world, second_world]))
    
    def add_used_relation(self, first_world, second_world):
        self.used_relations.add(tuple([first_world, second_world]))
        #if tuple([first_world, second_world]) not in self.used_relations:
            #self.used_relations.append(tuple([first_world, second_world]))
        
    def add_valuation(self, variable, world, value):
        if (variable, world) in self.valuations:
            if self.valuations[(variable, world)] != value: # contradiction
                return False
        else:
            self.valuations[(variable, world)] = value
            return True

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
    new_interpretation.world_generator_present = old_interpretation.world_generator_present
    new_interpretation.valuations = old_interpretation.valuations.copy()
    return new_interpretation

def rules(old_interpretation, formula, connective, interpretations):
    if connective == '⊐' and formula.assignation == False:
        old_interpretation.world_generator_present = True
        old_interpretation.add_removable_formula(Formula(formula.tree.left, old_interpretation.worlds + 1, True))
        old_interpretation.add_removable_formula(Formula(formula.tree.right, old_interpretation.worlds + 1, False))
        #print("new relation: ", formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_relation(formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_world()
        interpretations.append(old_interpretation)
        return interpretations
         
    elif connective == '⊐' and formula.assignation == True:
        old_interpretation.add_permanent_formula(formula)
        new_interpretation = copy_interpretation(old_interpretation)

        possible_relations = set()
        for relation in old_interpretation.relations:
            #print("relation here: ", relation[0], relation[1])
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    #print("relation added: ", relation[0], relation[1])
                    possible_relations.add(relation)
        
        if not possible_relations:
            #print("end2")
            return False

        count = 0
        for relation in possible_relations:
            #print("count: ", count)
            #count += 1
            #print("relation ⊐: ", relation[0], relation[1])
            old_interpretation.add_used_relation(relation[0], relation[1])
            new_interpretation.add_used_relation(relation[0], relation[1])
            old_interpretation.add_removable_formula(Formula(formula.tree.left, relation[1], False))
            new_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], True))
        interpretations.append(old_interpretation)
        interpretations.append(new_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == True: 
        old_interpretation.add_permanent_formula(formula)
        possible_relations = set()
        for relation in old_interpretation.relations:
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    #print("here relation added: ", relation[0], relation[1])
                    possible_relations.add(relation)
        
        if not possible_relations:
            #print("end1")
            return False

        for relation in possible_relations:
            #print("relation ∼: ", relation[0], relation[1])
            old_interpretation.add_used_relation(relation[0],  relation[1])
            old_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], False))
        interpretations.append(old_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == False:
        old_interpretation.world_generator_present = True
        old_interpretation.add_removable_formula(Formula(formula.tree.right, old_interpretation.worlds + 1, True))
        old_interpretation.add_relation(formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_world() # make sure this is correct
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
            #print("closed2")
            return interpretations # the branch is closed, so we can get rid of it
    
    #print("worlds: ", old_interpretation.worlds) 
    #if old_interpretation.worlds > 30:
        #print("infinite")
        #return False 

    # apply rule again to permanent formulas (only if there are relations that have not been applied yet)
    for formula in old_interpretation.permanent_formulas:
        #formula.tree.inorder()
        if old_interpretation.world_generator_present:
            print("infinite")
            return False # infinite branch, not a tautology
        """
        if formula.tree.right and (formula.tree.right.data  == "∼" or formula.tree.right.data  == "⊐"):
            if decision_procedure(formula.tree.right) == False: # to check that the implication is not a tautology
                #print("infinite")
                return False # infinite branch, not a tautology
        elif formula.tree.left and (formula.tree.left.data == "⊐" or formula.tree.left.data  == "∼"):
            if decision_procedure(formula.tree.left) == False: # to check that the implication is not a tautology
                #print("infinite")
                return False # infinite branch, not a tautology
        """
            
        #print("permanent")
        possible_relations = set()
        for relation in old_interpretation.relations:
            if relation not in old_interpretation.used_relations:
                if relation[0] == formula.world:
                    #print("relation added: ", relation[0], relation[1])
                    possible_relations.add(relation)
                    #old_interpretation.add_used_relation(relation[0], relation[1])
        
        if possible_relations:
            #old_interpretation.relations = possible_relations
            #print(interpretations)
            #print("possible")
            return rules(old_interpretation, formula, formula.tree.data, interpretations)
        #else:
            #print("not possible")
        #if not operator.eq(set(possible_relations),set(old_interpretation.used_relations)):
            #return rules(old_interpretation, formula, formula.tree.data, interpretations)
    
    return False # no contradiction found, so it is not a tautology

def apply_rule(interpretations):
    old_interpretation = interpretations.pop(0)
    if old_interpretation.removable_formulas:
        formula = old_interpretation.removable_formulas.pop(0)
        connective = formula.tree.data
        if connective in connectives:
            return rules(old_interpretation, formula, connective, interpretations)
    
        elif connective in alphabet: # no connective left, add valuations
            added = old_interpretation.add_valuation(connective, formula.world, formula.assignation)
            if added == False:
                #print("closed")
                return interpretations # the branch is closed, so we can get rid of it
            interpretations.append(old_interpretation)
            return interpretations
        else:
            print("wrong notation")
            return False

    else: # no more formulas, apply transitivity rule, then heredity rule and finally permanent formulas
        return no_more_formulas(old_interpretation, interpretations)
        
def decision_procedure(tree):
    interpretations = []
    initial_node = create_initial_tableau_node(tree)
    interpretations.append(initial_node)
    while interpretations:
        interpretations = apply_rule(interpretations)
        if interpretations == False: # process should stop because the branch is open
            #print("end")
            return False # it is not a tautology
        elif not interpretations:
            return True # it is a tautology
        # process should continue, but this interpretation should not be in the list anymore

    return True # it is a tautology