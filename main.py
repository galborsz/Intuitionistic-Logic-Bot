class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print(self.data)
        if self.right:
            self.right.print_tree()

    def add_child_left(self, left):
        left.parent = self
        self.left = left
    
    def add_child_right(self, right):
        right.parent = self
        self.right = right

def get_subtree(stack):
    rightchild = stack.pop()
    if isinstance(rightchild, str):
        rightchild = TreeNode(rightchild)
    connective = stack.pop()
    if connective == "∼":
        negation = TreeNode("∼")
        negation.add_child_right(rightchild)
        rightchild = negation
        connective = stack.pop()
    leftchild = stack.pop()
    if isinstance(leftchild, str):
        leftchild = TreeNode(leftchild)
    tree = TreeNode(connective)
    tree.add_child_left(leftchild)
    tree.add_child_right(rightchild)
    return tree

def build_tree(formula):
    # symbols definition
    variables = ['p', 'q', 'r', 's']
    connectives = ['⊐', '∧', '∨', '∼']

    stack = [] # for storing temporal symbols
    q = 0
    for i in range(len(formula)):
        if q < len(formula):
            if formula[q] in (connectives + variables):
                element = formula[q]
                negation = TreeNode("∼")
                if formula[q] == "∼" and formula[q+1] != "(":
                    element = negation
                while formula[q] == "∼" and formula[q+1] != "(":
                    afternegation = TreeNode(formula[q+1])
                    negation.add_child_right(afternegation)
                    negation = negation.right
                    q+=1
                stack.append(element)
            elif formula[q] == ")": #pop stack and create tree
                tree = get_subtree(stack)
                stack.append(tree)
        q+=1

    tree = get_subtree(stack)
    return tree


def main():
    #formula = "∼∼∼∼p⊐(q∧s)"
    formula = "p⊐∼(q∧s)"
    #formula = "p∧q"
    tree = build_tree(formula)
    tree.print_tree()

if __name__ == '__main__':
    main()