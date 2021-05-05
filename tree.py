# https://github.com/codebasics/data-structures-algorithms-python/blob/master/data_structures/7_Tree/7_tree.py
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

    def inorder(self):
        if self.left:
            self.left.inorder()
        print(self.data)
        if self.right:
            self.right.inorder()
    
    def preorder(self):
        print(self.data)
        if self.left:
            self.left.preorder()
        if self.right:
            self.right.preorder()
    
    def tree_to_string(self):
        node = self.inorder()
        while node:
            node = node + self.inorder()
        return node

    def add_child_left(self, left):
        left.parent = self
        self.left = left
    
    def add_child_right(self, right):
        right.parent = self
        self.right = right

def get_subtree(stack):
    tree = None
    rightchild = stack.pop()
    if isinstance(rightchild, str):
        rightchild = TreeNode(rightchild)
    connective = stack.pop()
    if connective == "∼":
        negation = TreeNode("∼")
        negation.add_child_right(rightchild)
        rightchild = negation
        if stack:
            connective = stack.pop()
            tree = TreeNode(connective)
            tree.add_child_right(rightchild)
        else:
            tree = rightchild
    else:
        tree = TreeNode(connective)
        tree.add_child_right(rightchild)
    if stack:
        leftchild = stack.pop()
        if isinstance(leftchild, str):
            leftchild = TreeNode(leftchild)
        tree.add_child_left(leftchild)
    
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
                if formula[q+1] == "(":
                    negation = element
                    while negation:
                        stack.append(negation.data)
                        negation = negation.right
                else:
                    stack.append(element)
            elif formula[q] == ")": #pop stack and create tree
                tree = get_subtree(stack)
                stack.append(tree)
        q+=1

    tree = get_subtree(stack)
    return tree