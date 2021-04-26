

class ExpressionTree(object):
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

    def inorder(self):
        # inorder traversal of expression tree
        # inorder traversal = > left, root, right
        if self.data == None:
            return
        self.left.inorder()
        print(self.data)
        self.right.inorder()
    
def isConnective(s):
    connectives = ['⊐', '∧', '∨', '∼']
    if s in connectives:
        return True
    else:
        return False

def isVariable(s):
    variables = ['p', 'q', 'r', 's']
    if s in variables:
        return True
    else:
        return False

def treeFactor(formula):
    if isVariable(formula):
        return ExpressionTree(formula, None, None)
    if formula[0] == "∼":
        if isVariable(formula):
            return ExpressionTree("∼", formula, None)
        else:
            tree = treeFactor(formula)
            return ExpressionTree("∼", tree, None)
    elif formula[0] == "(":
        return treeExpression(formula)

def treeTerm(formula):
    lefttree = treeFactor(formula)
    for i in range(0, len(formula)):
        if formula[i] == "∧":
            righttree = treeFactor(formula)
            return ExpressionTree("∧", lefttree, righttree)
        if formula[i] == "∨":
            righttree = treeFactor(formula)
            return ExpressionTree("∨", lefttree, righttree)
    return lefttree
    
    if formula[0] == "∧":
        righttree = treeFactor(formula)
        return ExpressionTree("∧", lefttree, righttree)
    elif formula[0] == "∨":
        righttree = treeFactor(formula)
        return ExpressionTree("∨", lefttree, righttree)
    else:
        return lefttree

def treeExpression(formula):
    lefttree = treeTerm(formula)
    for i in range(0, len(formula)):
        if formula[i] == "⊐":
            righttree = treeTerm(formula[i:])
            return ExpressionTree("⊐", lefttree, righttree)
    return lefttree

def main():
    print("Let's start!")
    # generate formula
    length = 1
    variables = ['p', 'q', 'r', 's']
    connectives = ['⊐', '∧', '∨', '∼']
    # construct expression tree to represent the formula
    # Iterate over the string
    #formula = "p⊐∼∼p"
    formula = "p"
    tree = treeExpression(formula)
    tree.inorder()
    # test validity of formula (using the expression tree)
    # post it in twitter

if __name__ == "__main__":
    main()