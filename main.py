

class ExpressionTree(object):
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

    def newExpTreeNode(self, data, left, right):
        return ExpressionTree(data, left, right)
    
    def isVariable(self, s):
        connectives = ['⊐', '∧', '∨', '∼']
        if s in connectives:
            return True
        else:
            return False
    
    def treeFactor(lp, tp):
        if isVariable(lp):
            tp = newExpTreeNode(lp, NULL, NULL)
            return 1
        if acceptCharacter(lp, "∼"):
            if isVariable(lp):
                return 1
            else:
                return 0
        if not acceptCharacter(lp, "("):
            return 0
        if not treeExpression(lp):
            return 0
        return acceptCharacter(lp, ")")

    def treeTerm(lp, tp):
        if treeFactor(lp, tp):
            return 0
        tr = tp
        while lp not NULL:
            if acceptCharacter(lp, "∧"):
                if treeFactor(lp, tp):
                    tr = newExpTreeNode(tr, tp)
                else:
                    return 0
            elif acceptCharacter(lp, "∨"):
                if treeFactor(lp, tp):
                    tr = newExpTreeNode(tr, tp)
                else:
                    return 0
            else:
                tp = tr
                return 1
        tp = tr
        return 1

def treeTerm(formula, tree):
    formula, tree = treeFactor(formula, tree)

def treeExpression(formula):
    tree = None
    formula, tree = treeTerm(formula, tree)
    for element in formula:
        print(element, end='\n')
        if element == "⊐":
            formula, tree = treeTerm(formula, tree)
    return tree


def convertIntoTree(formula):
    return treeExpression(formula)
    

def main():
    print("Let's start!")
    # generate formula
    length = 1
    variables = ['p', 'q', 'r', 's']
    connectives = ['⊐', '∧', '∨', '∼']
    # construct expression tree to represent the formula
    # Iterate over the string
    formula = "p⊐∼∼p"
    convertIntoTree(formula)
    # test validity of formula (using the expression tree)
    # post it in twitter

if __name__ == "__main__":
    main()