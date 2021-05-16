from tree_node import TreeNode

class Formula:
    def __init__(self, tree, world, assignation):
        self.tree = tree
        self.world = world
        self.assignation = assignation

# node = TreeNode(Data())
class Interpretation:
    def __init__(self):
        self.removable_formulas = []
        self.permanent_formulas = []
        self.worlds = 0 # use it as a counter instead of as a list ?
        self.relations = []
        self.valuations = {}

    def add_removable_formula(self, formula):
        # what if the key already exists?
        self.removable_formulas.append(formula)
    
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
            #if self.valuations[(variable, world)] == False and value == True:
            if self.valuations[(variable, world)] != value:
                return False
        self.valuations[(variable, world)] = value
        return True

def create_initial_tableau_node(formula):
    tableau_node = TreeNode(Interpretation())
    tableau_node.data.add_removable_formula(Formula(formula, 0, False))
    return tableau_node

def apply_rule(previous_node, formula):
    symbol = formula.tree.data
    new_right_node = previous_node
    #new_left_node = None

    if symbol == '⊐' and formula.assignation == False:
        print("rule ⊐ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world+1, True))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world+1, False))
        new_right_node.data.add_relation(new_right_node.data.worlds, new_right_node.data.worlds + 1)
        new_right_node.data.add_world()
        
    
    elif symbol == '⊐' and formula.assignation == True:
        print("rule ⊐ +")
        #new_left_node = previous_node
        for relation in new_right_node.data.relations:
            if relation[0] == formula.world:
                print("uiui")

    elif symbol == '∼' and formula.assignation == True:
        print("rule ∼ +")
        for relation in new_right_node.data.relations:
            if relation[0] == formula.world:
                new_right_node.data.add_removable_formula(Formula(formula.tree.right, relation[1], False))
        print("old formula: ")
        formula.tree.inorder()
        new_right_node.data.add_formula(formula) # should be kept alwaaays
            

    elif symbol == '∼' and formula.assignation == False:
        print("rule ∼ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world+1, True))
        new_right_node.data.add_removable_relation(formula.world, formula.world+1)
        new_right_node.data.add_world()
    
    elif symbol == '∧' and formula.assignation == True:
        print("rule ∧ +")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, True))

    elif symbol == '∧' and formula.assignation == False:
        print("rule ∧ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        #new_left_node = previous_node
        #new_left_node.data.add_formula(Formula(formula.tree.right, formula.world, False))
    
    elif symbol == '∨' and formula.assignation == True:
        print("rule ∨ +")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
        #new_left_node = previous_node
        #new_left_node.data.add_formula(Formula(formula.tree.right, formula.world, True))

    elif symbol == '∨' and formula.assignation == False:
        print("rule ∨ -")
        new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
        new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, False))

    else:
        added = new_right_node.data.add_valuation(symbol, formula.world, formula.assignation)
        if not added:
            return False

    #return new_right_node, new_left_node
    return new_right_node
 
# An iterative process to print preorder traveral of BT
# https://www.geeksforgeeks.org/iterative-preorder-traversal/
def iterative_preorder(root):
     
    # Base CAse
    if root is None:
        return
 
    # create an empty stack and push root to it
    nodeStack = []
    nodeStack.append(root)

    # create initial list
    previous_node = create_initial_tableau_node(root)
 
    # Pop all items one by one. Do following for every popped item
    # a) print it
    # b) push its right child
    # c) push its left child
    # Note that right child is pushed first so that left
    # is processed first */
    while(len(nodeStack) > 0):
         
        # Pop the top item from stack and print it
        symbol = nodeStack.pop()
        print("symbol: ", symbol.data)
        formula = previous_node.data.formulas.pop(0)

        # create node
        new_right_node, new_left_node = apply_rule(previous_node, symbol.data, formula)
        print("new_left_node: ", new_left_node)
        if not new_left_node:
            previous_node.add_child_right(new_right_node)
        else:
            previous_node.add_child_right(new_right_node)
            previous_node.add_child_left(new_left_node)
        """
        new_right_node = apply_rule(previous_node, symbol.data, formula)
        if not new_right_node:
            return False
        previous_node.add_child_right(new_right_node)
        """
        # Push right and left children of the popped node
        # to stack
        if symbol.right is not None:
            nodeStack.append(symbol.right)
        if symbol.left is not None:
            nodeStack.append(symbol.left)

        # apply heredity rule
        variables = []
        worlds = []
        for element in new_right_node.data.valuations:
            print("element: ", element, new_right_node.data.valuations[element])
            for relation in new_right_node.data.relations:
                print("relation: ", relation)
                if element[1] == relation[0] and relation[0] != relation[1]:
                    print("found: ", element, relation[1])
                    variables.append(element[0])
                    worlds.append(relation[1])
        
        # try to find contradiction
        for variable, world in zip(variables, worlds):
            print("adding: ", variable, world)
            added = new_right_node.data.add_valuation(variable, world, True)
            if not added:
                return False
        
        previous_node = new_right_node

    return True

def rule(tableau_node):

    new_right_node = tableau_node
    new_left_node = None
    for formula in tableau_node.data.removable_formulas:
        connective = formula.tree.data
        if connective == '⊐' and formula.assignation == False:
            print("rule ⊐ -")
            new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world+1, True))
            new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world+1, False))
            new_right_node.data.add_relation(new_right_node.data.worlds, new_right_node.data.worlds + 1)
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
            new_right_node.data.add_removable_formula(formula) # should be kept alwaaays
                

        elif connective == '∼' and formula.assignation == False:
            print("rule ∼ -")
            new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world+1, True))
            new_right_node.data.add_relation(formula.world, formula.world+1)
            new_right_node.data.add_world()
        
        elif connective == '∧' and formula.assignation == True:
            print("rule ∧ +")
            new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
            new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, True))

        elif connective == '∧' and formula.assignation == False:
            print("rule ∧ -")
            new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
            new_left_node = previous_node
            new_left_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, False))
        
        elif connective == '∨' and formula.assignation == True:
            print("rule ∨ +")
            new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, True))
            new_left_node = previous_node
            new_left_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, True))

        elif connective == '∨' and formula.assignation == False:
            print("rule ∨ -")
            new_right_node.data.add_removable_formula(Formula(formula.tree.left, formula.world, False))
            new_right_node.data.add_removable_formula(Formula(formula.tree.right, formula.world, False))

        else:
            added = new_right_node.data.add_valuation(connective, formula.world, formula.assignation)
            if not added:
                return False

        return new_right_node, new_left_node


def create_tableau(tableau):
    formula = tableau.data.removable_formulas.pop(0)
    # apply rule
    new_right_node, new_left_node = apply_rule(tableau, formula)
    print("new right: ", new_right_node)
    print("new left: ", new_left_node)

    if new_right_node != None:
        tableau.add_child_right(new_right_node)
        create_tableau(tableau.right)
    if new_left_node != None:
        tableau.add_child_left(new_left_node)
        create_tableau(tableau.left)

    if tableau.right == None and tableau.left == None:
        return tableau

def auxiliary(tree):
    # create initial list
    root = create_initial_tableau_node(tree)

    tableau = create_tableau(root)

    return tableau