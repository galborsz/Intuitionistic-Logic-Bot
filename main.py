class BinaryTree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
    
# A function to do inorder tree traversal
def printInorder(tree):
    if tree:
        if tree.data == None:
            return
        else:
            # First recur on left child
            printInorder(tree.left)
    
            # then print the data of node
            print(tree.data)
    
            # now recur on right child
            printInorder(tree.right)

def convertIntoTree(formula):
    # symbols definition
    variables = ['p', 'q', 'r', 's']
    connectives = ['⊐', '∧', '∨', '∼']

    stack = [] #for storing temporal symbols
    for i in range(len(formula)):
        if formula[i] in (connectives + variables):
            element = formula[i]
            print("element: ", element)
            if element == "∼" and formula[i+1] != "(":
                element = BinaryTree("∼", formula[i+1])
                print("tree: ")
                printInorder(element)
                print("end tree")
                i+=1
            stack.append(element)
        elif formula[i] == ")": #pop stack and create tree
            rightchild = BinaryTree(stack.pop())
            connective = stack.pop()
            if connective == "∼":
                rightchild = BinaryTree("∼", rightchild)
                connective = stack.pop()
            leftchild = BinaryTree(stack.pop())
            tree = BinaryTree(connective, leftchild, rightchild)
            stack.append(tree)
    rightchild = BinaryTree(stack.pop())
    connective = stack.pop()
    leftchild = BinaryTree(stack.pop())
    tree = BinaryTree(connective, leftchild, rightchild)
    return tree

def main():
    print("Let's start!")
    # generate formula
    variables = ['p', 'q', 'r', 's']
    connectives = ['⊐', '∧', '∨', '∼']

    # construct expression tree to represent the formula
    # Iterate over the string
    #formula = "p⊐∼p"
    formula = "p⊐(q∧s)"
    #formula = "p∧q"
    tree = convertIntoTree(formula)
    printInorder(tree)
    # test validity of formula (using the expression tree)
    # post it in twitter

if __name__ == "__main__":
    main()