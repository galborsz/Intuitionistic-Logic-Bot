from tree_node import TreeNode

def get_subtree(stack):
    rightchild = stack.pop()
    if isinstance(rightchild, str):
        rightchild = TreeNode(rightchild)
    
    connective = stack.pop()
    negation = TreeNode("∼")
    while connective == '∼':
        negation.add_child_right(rightchild)
        rightchild = negation
        if stack:
            connective = stack.pop()
            negation = TreeNode("∼")
        else:
            break
    if stack:
        leftchild = stack.pop()
        if isinstance(leftchild, str):
            leftchild = TreeNode(leftchild)
        tree = TreeNode(connective)
        tree.add_child_left(leftchild)
        tree.add_child_right(rightchild)
    else: 
        tree = rightchild
    return tree

def build_tree(formula):
    # symbols definition
    variables = ['p', 'q', 'r', 's', '*']
    connectives = ['⊐', '∧', '∨', '∼']

    stack = [] # for storing temporal symbols
    q = 0
    for i in range(len(formula)):
        if q < len(formula):
            element = formula[q]
            if element in (connectives + variables):
                if element == '∼':
                    count = 1
                    while element == '∼':
                        if formula[q+1] == "(":
                            for i in range(count):
                                stack.append('∼')
                        elif formula[q+1] in variables:
                            negation = TreeNode("∼")
                            original = negation
                            for i in range(count - 1): # do not count the root
                                negation.add_child_right(TreeNode("∼"))
                                negation = negation.right
                            negation.add_child_right(TreeNode(formula[q+1]))
                            stack.append(original)
                        elif formula[q+1] == "∼":
                            count+=1  
                        q+=1   
                        element = formula[q]   
                else: 
                    stack.append(element)
            elif formula[q] == ")": # pop stack and create tree
                tree = get_subtree(stack)
                stack.append(tree)
            q+=1

    tree = get_subtree(stack)
    return tree