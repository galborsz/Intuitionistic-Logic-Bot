from tree import TreeNode

class Formula:
    def __init__(self, tree, world, assignation):
        self.tree = tree
        self.world = world
        self.assignation = assignation

# node = TreeNode(Data())
class Data:
    def __init__(self):
        self.formulas = []
        self.worlds = 0 # use it as a counter instead of as a list ?
        self.relations = []
        self.valuations = {}

    def add_formula(self, formula):
        # what if the key already exists?
        self.formulas.append(formula)
    
    def add_world(self):
        self.worlds += 1
        # reflexive rule applied every time a new world is introduced
        for i in range(self.worlds):
            self.add_relation(i, i)
    
    def add_relation(self, first_world, second_world):
        if tuple([first_world, second_world]) not in self.relations:
            self.relations.append(tuple([first_world, second_world]))
        
    def add_valuation(self, variable, world, value):
        if (variable, world) in self.valuations:
            if self.valuations[(variable, world)] == False and value == True:
                return False
        self.valuations[(variable, world)] = value
        return True

def create_initial_tableau_node(formula):
    tableau_node = TreeNode(Data())
    tableau_node.data.add_formula(Formula(formula, 0, False))
    tableau_node.data.add_world()
    return tableau_node

# ['⊐', '∧', '∨', '∼'] new_node = create_tableau_node(previous_node.data.formulas[0])
def apply_rule(previous_node, symbol, assignation):
    new_node = TreeNode(Data())
    new_node.data.formulas = previous_node.data.formulas
    new_node.data.worlds = previous_node.data.worlds
    new_node.data.relations = previous_node.data.relations
    new_node.data.valuations = previous_node.data.valuations

    formula = new_node.data.formulas.pop(0)
    if symbol == '⊐' and assignation == False:
        new_node.data.add_formula(Formula(formula.tree.left, formula.world+1, True))
        new_node.data.add_formula(Formula(formula.tree.right, formula.world+1, False))
        new_node.data.add_world()
        new_node.data.add_relation(new_node.data.worlds - 1, new_node.data.worlds)
    else:
        new_node.data.add_valuation(symbol, formula.world, formula.assignation)

    return new_node
 
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

        # create node
        new_node = apply_rule(previous_node, symbol.data, False)
        previous_node.add_child_right(new_node)
         
        # Push right and left children of the popped node
        # to stack
        if symbol.right is not None:
            nodeStack.append(symbol.right)
        if symbol.left is not None:
            nodeStack.append(symbol.left)
    
        # apply heredity rule
        variables = []
        worlds = []
        for element in new_node.data.valuations:
            for relation in new_node.data.relations:
                if element[1] == relation[0] and relation[0] != relation[1]:
                    variables.append(element[0])
                    worlds.append(relation[1])
          
        for variable, world in zip(variables, worlds):
            added = new_node.data.add_valuation(variable, world, True)
            if not added:
                return False
    
    return True