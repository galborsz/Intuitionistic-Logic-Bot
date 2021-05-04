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
        for i in range(self.worlds+1):
            print("reflexive relation: ", i, i)
            self.add_relation(i, i)
    
    def add_relation(self, first_world, second_world):
        if tuple([first_world, second_world]) not in self.relations:
            self.relations.append(tuple([first_world, second_world]))
        
    def add_valuation(self, variable, world, value):
        if (variable, world) in self.valuations:
            if self.valuations[(variable, world)] == False and value == True:
                print("FALSE NOT ADDEEEED")
                return False
        self.valuations[(variable, world)] = value
        return True

def create_initial_tableau_node(formula):
    tableau_node = TreeNode(Data())
    tableau_node.data.add_formula(Formula(formula, 0, False))
    return tableau_node

# ['⊐', '∧', '∨', '∼'] new_node = create_tableau_node(previous_node.data.formulas[0])
def apply_rule(previous_node, symbol, formula):
    new_node = TreeNode(Data())
    new_node.data.formulas = previous_node.data.formulas
    new_node.data.worlds = previous_node.data.worlds
    new_node.data.relations = previous_node.data.relations
    new_node.data.valuations = previous_node.data.valuations

    #formula = new_node.data.formulas.pop(0)
    if symbol == '⊐' and formula.assignation == False:
        print("rule ⊐ -")
        new_node.data.add_formula(Formula(formula.tree.left, formula.world+1, True))
        new_node.data.add_formula(Formula(formula.tree.right, formula.world+1, False))
        print("WORLDS ⊐ -: ", new_node.data.worlds)
        new_node.data.add_relation(new_node.data.worlds, new_node.data.worlds + 1)
        new_node.data.add_world()
        
    
    elif symbol == '⊐' and formula.assignation == True:
        print("rule ⊐ +")

    elif symbol == '∼' and formula.assignation == True:
        print("rule ∼ +")
        for relation in new_node.data.relations:
            if relation[0] == formula.world:
                new_node.data.add_formula(Formula(formula.tree.right, relation[1], False))
            

    elif symbol == '∼' and formula.assignation == False:
        print("rule ∼ -")
        print("WORLDS ∼ -: ", new_node.data.worlds)
        new_node.data.add_formula(Formula(formula.tree.right, formula.world+1, True))
        new_node.data.add_relation(new_node.data.worlds, new_node.data.worlds+1)
        new_node.data.add_world()
    
    elif symbol == '∧' and formula.assignation == True:
        print("rule ∧ +")
        new_node.data.add_formula(Formula(formula.tree.left, formula.world, True))
        new_node.data.add_formula(Formula(formula.tree.right, formula.world, True))

    elif symbol == '∧' and formula.assignation == False:
    
    elif symbol == '∨' and formula.assignation == True:

    elif symbol == '∨' and formula.assignation == False:
        print("rule ∧ -")
        new_node.data.add_formula(Formula(formula.tree.left, formula.world, False))
        new_node.data.add_formula(Formula(formula.tree.right, formula.world, False))

    else:
        #print("uy uy symbol: ", symbol)
        #print("adding valuation ", formula.world, " to formula: ")
        #formula.tree.inorder()
        print("adding valuation: ", symbol, formula.world, formula.assignation)
        added = new_node.data.add_valuation(symbol, formula.world, formula.assignation)
        if not added:
            return False

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
        print("symbol: ", symbol.data)
        if not previous_node.data.formulas:
            print("no more formulas")
            break
        formula = previous_node.data.formulas.pop(0)
        #print("popped formula: ", formula.world, formula.assignation)
        #formula.tree.inorder()

        # create node
        new_node = apply_rule(previous_node, symbol.data, formula)
        if not new_node:
            return False
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
            print("element: ", element, " value: ", new_node.data.valuations[element])
            for relation in new_node.data.relations:
                print("relation: ", relation)
                if element[1] == relation[0] and relation[0] != relation[1]:
                    print("HELLO VARIABLE: ", element[0], " WORLD: ", relation[1])
                    variables.append(element[0])
                    worlds.append(relation[1])
        
        # try to find contradiction
        for variable, world in zip(variables, worlds):
            print("adding valuation ", world, " to formula: ", variable)
            print("found: ", variable, world)
            added = new_node.data.add_valuation(variable, world, True)
            if not added:
                return False
        
        previous_node = new_node
    
    return True