from tree_node import TreeNode

class Formula:
    def __init__(self, tree, world, assignation):
        self.tree = tree
        self.world = world
        self.assignation = assignation

class Interpretation:
    def __init__(self):
        self.open = True
        self.removable_formulas = []
        self.permanent_formulas = []
        self.worlds = 0 # use it as a counter instead of as a list
        self.relations = []
        self.valuations = {}
        self.used_relations = []

    def add_removable_formula(self, formula):
        # what if the key already exists?
        self.removable_formulas.append(formula)
    
    def add_permanent_formula(self, formula):
        # what if the key already exists?
        self.permanent_formulas.append(formula)
    
    def add_world(self):
        self.worlds += 1
        # reflexive rule applied every time a new world is introduced
        for i in range(self.worlds+1):
            self.add_relation(i, i)
    
    def add_relation(self, first_world, second_world):
        if tuple([first_world, second_world]) not in self.relations:
            self.relations.append(tuple([first_world, second_world]))
        
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
    new_interpretation.open = old_interpretation.open
    new_interpretation.removable_formulas = old_interpretation.removable_formulas
    new_interpretation.permanent_formulas = old_interpretation.permanent_formulas
    new_interpretation.relations = old_interpretation.relations
    new_interpretation.worlds = old_interpretation.worlds
    new_interpretation.valuations = old_interpretation.valuations
    return new_interpretation

def rules(old_interpretation, formula, connective, interpretations):
    if connective == '⊐' and formula.assignation == False:
        print("rule ⊐ -")
        #new_interpretation = copy_interpretation(old_interpretation)
        old_interpretation.add_removable_formula(Formula(formula.tree.left, old_interpretation.worlds + 1, True))
        old_interpretation.add_removable_formula(Formula(formula.tree.right, old_interpretation.worlds + 1, False))
        old_interpretation.add_relation(formula.world, old_interpretation.worlds + 1)
        old_interpretation.add_world()
        interpretations.append(old_interpretation)
        return interpretations
         
    elif connective == '⊐' and formula.assignation == True:
        first_new_interpretation = copy_interpretation(old_interpretation)
        first_new_interpretation.add_permanent_formula(formula)
        second_new_interpretation = copy_interpretation(old_interpretation)
        second_new_interpretation.add_permanent_formula(formula)
        for relation in old_interpretation.relations:
            if relation[0] == formula.world:
                first_new_interpretation.used_relations.append(relation)
                second_new_interpretation.used_relations.append(relation)
                first_new_interpretation.add_removable_formula(Formula(formula.tree.left, relation[1], False))
                second_new_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], True))
        interpretations.append(first_new_interpretation)
        interpretations.append(second_new_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == True: 
        #new_interpretation = copy_interpretation(old_interpretation)
        old_interpretation.add_permanent_formula(formula)
        for relation in old_interpretation.relations:
            if relation[0] == formula.world:
                old_interpretation.used_relations.append(relation)
                old_interpretation.add_removable_formula(Formula(formula.tree.right, relation[1], False))
        interpretations.append(old_interpretation)
        return interpretations

    elif connective == '∼' and formula.assignation == False:
        new_interpretation = copy_interpretation(old_interpretation)
        new_interpretation.add_removable_formula(Formula(formula.tree.right, new_interpretation.worlds + 1, True))
        new_interpretation.add_relation(formula.world, new_interpretation.worlds + 1)
        new_interpretation.add_world() # make sure this is correct
        interpretations.append(new_interpretation)
        return interpretations
    
    elif connective == '∧' and formula.assignation == True:
        new_interpretation = copy_interpretation(old_interpretation)
        new_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, True))
        interpretations.append(new_interpretation)
        return interpretations

    elif connective == '∧' and formula.assignation == False:
        first_new_interpretation = copy_interpretation(old_interpretation)
        second_new_interpretation = copy_interpretation(old_interpretation)
        first_new_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        second_new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, False))
        interpretations.append(first_new_interpretation)
        interpretations.append(second_new_interpretation)
        return interpretations

    elif connective == '∨' and formula.assignation == True:
        first_new_interpretation = copy_interpretation(old_interpretation)
        second_new_interpretation = copy_interpretation(old_interpretation)
        first_new_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        second_new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, True))
        interpretations.append(first_new_interpretation)
        interpretations.append(second_new_interpretation)
        return interpretations

    elif connective == '∨' and formula.assignation == False:
        new_interpretation = copy_interpretation(old_interpretation)
        new_interpretation.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        new_interpretation.add_removable_formula(Formula(formula.tree.right, formula.world, False))
        interpretations.append(new_interpretation)
        return interpretations

def apply_rule(interpretations):
    old_interpretation = interpretations.pop(0)
    print("old: ", old_interpretation)
    if old_interpretation.removable_formulas:
        formula = old_interpretation.removable_formulas.pop(0)
        print("formula apply rule to:")
        formula.tree.inorder()
        connective = formula.tree.data

        if connective in ['⊐', '∧', '∨', '∼']:
            return rules(old_interpretation, formula, connective, interpretations)
    
        elif connective in ['p', 'q', 'r', 's']: # no connective left, add valuations
            #new_interpretation = copy_interpretation(old_interpretation)
            added = old_interpretation.add_valuation(connective, formula.world, formula.assignation)
            if added == False:
                print("contradiction")
                #old_interpretation.data.open = False
                return interpretations 
            interpretations.append(old_interpretation)
            if interpretations:
                print("not empty", interpretations[0])
                #interpretations[0].removable_formulas[0].tree.inorder()
            return interpretations

    else: # no more formulas, apply transitivity rule, then heredity rule and finally permanent formulas
        print("transitivity")
        # transitivity rule
        for first_relation in old_interpretation.relations:
            first = first_relation[1]
            for second_relation in old_interpretation.relations:
                if first == second_relation[0]:
                    old_interpretation.add_relation(first_relation[0], second_relation[1])
                    first = second_relation[1]

        # heredity rule
        variables = []
        worlds = []
        for valuation in old_interpretation.valuations:
            for relation in old_interpretation.relations:
                if valuation[1] == relation[0] and relation[0] != relation[1]:
                    variables.append(valuation[0])
                    worlds.append(relation[1])
        
        # try to find contradiction
        for variable, world in zip(variables, worlds):
            added = old_interpretation.add_valuation(variable, world, True)
            if added == False:
                print("contradiction 2")
                #old_interpretation.open = False
                return interpretations
        
        # apply rule again to permanent formulas
        for formula in old_interpretation.permanent_formulas:
            return rules(old_interpretation, formula, formula.tree.data, interpretations)
        
        return False # no contradiction found, so it is not a tautology
        


def decision_procedure(tree):
    interpretations = []
    initial_node = create_initial_tableau_node(tree)
    interpretations.append(initial_node)
    while interpretations:
        interpretations = apply_rule(interpretations)
        print("interpretations: ", interpretations)
        if interpretations == False: # process should stop because the branch is open
            return False # it is not a tautology
        elif not interpretations:
            return True
        # process should continue, but this interpretation should not be in the list anymore

    return True # it is a tautology