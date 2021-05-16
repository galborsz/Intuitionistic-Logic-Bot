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
        self.worlds = 0 # use it as a counter instead of as a list ?
        self.relations = []
        self.valuations = {}

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
                self.open = False
                print("contradiction found")
        else:
            self.valuations[(variable, world)] = value

def create_initial_tableau_node(formula):
    tableau_node = TreeNode(Interpretation())
    tableau_node.data.add_removable_formula(Formula(formula, 0, False))
    return tableau_node

def copy_node(original_node):
    new_node = TreeNode(Interpretation())
    new_node.data.relations = original_node.data.relations
    new_node.data.removable_formulas = original_node.data.removable_formulas
    new_node.data.permanent_formulas = original_node.data.permanent_formulas
    new_node.data.valuations = original_node.data.valuations
    new_node.data.worlds = original_node.data.worlds
    new_node.data.open = original_node.data.open
    return new_node

def apply_rule(tableau_node):
    print("remaining formulas: ")
    tableau_node.data.removable_formulas[0].tree.inorder()
    if not tableau_node.data.removable_formulas:
        print("end")
        new_right_node = None
        new_left_node = None
        return new_right_node, new_left_node

    formula = tableau_node.data.removable_formulas.pop(0)

    new_right_node = copy_node(tableau_node)
    new_right_node.data.number += 1
    new_left_node = None
    connective = formula.tree.data

    if connective == '⊐' and formula.assignation == False:
        print("rule ⊐ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, new_right_node.data.worlds + 1, True))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, new_right_node.data.worlds + 1, False))
        new_right_node.data.add_relation(formula.world, new_right_node.data.worlds + 1)
        new_right_node.data.add_world()
         
    elif connective == '⊐' and formula.assignation == True:
        print("rule ⊐ +")
        #new_left_node = previous_node
        for relation in new_right_node.data.relations:
            if relation[0] == formula.world:
                print("uiui")

    elif connective == '∼' and formula.assignation == True:
        print("rule ∼ +")
        for relation in new_right_node.data.relations:
            if relation[0] == formula.world:
                new_right_node.data.add_removable_formula(Formula(formula.tree.right, relation[1], False))
        print("old formula: ")
        formula.tree.inorder()
        new_right_node.data.add_removable_formula(formula) # should be kept always
            

    elif connective == '∼' and formula.assignation == False:
        print("rule ∼ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, new_right_node.data.worlds + 1, True))
        new_right_node.data.add_relation(formula.world, new_right_node.data.worlds + 1)
        new_right_node.data.add_world()
    
    elif connective == '∧' and formula.assignation == True:
        print("rule ∧ +")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, True))

    elif connective == '∧' and formula.assignation == False:
        print("rule ∧ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        new_left_node = copy_node(tableau_node)
        new_left_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, False))
    
    elif connective == '∨' and formula.assignation == True:
        print("rule ∨ +")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        new_left_node = copy_node(tableau_node)
        new_left_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, True))

    elif connective == '∨' and formula.assignation == False:
        print("rule ∨ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, False))

    #elif isinstance(connective, str):
    elif connective in ['p', 'q', 'r', 's']:
        new_right_node.data.add_valuation(connective, formula.world, formula.assignation)    
    else:
        print("cannot do anything")
        new_right_node = None
        
    return new_right_node, new_left_node

def auxiliary(tableau):
    
    # apply rule
    new_right_node, new_left_node = apply_rule(tableau)

    if new_right_node != None and new_right_node.data.contradiction == False:
        tableau.add_child_right(new_right_node)
        auxiliary(tableau.right)
    if new_left_node != None and new_left_node.data.contradiction == False:
        tableau.add_child_left(new_left_node)
        auxiliary(tableau.left)

    return tableau

    

def create_tableau(tree):
    # create initial list
    root = create_initial_tableau_node(tree)
    
    # extend tableau
    tableau = auxiliary(root)

    return tableau