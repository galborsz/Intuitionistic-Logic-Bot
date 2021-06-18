import os
import string
from tree_node import TreeNode
from decision_procedure import decision_procedure
import time

# global variables
alphabet = list(string.ascii_lowercase)
folders = os.listdir(os.getcwd()) 

def extenddoubleimplication(tree):
    if tree.data == "*":
        conjunction = TreeNode("∧")
        leftimplication = TreeNode("⊐")
        rightimplication = TreeNode("⊐")
        leftimplication.add_child_left(tree.left)
        leftimplication.add_child_right(tree.right)
        rightimplication.add_child_left(tree.right)
        rightimplication.add_child_right(tree.left)
        conjunction.add_child_left(leftimplication)
        conjunction.add_child_right(rightimplication)
        tree = conjunction
    if tree.left:
        tree.left = extenddoubleimplication(tree.left)
    if tree.right:
        tree.right = extenddoubleimplication(tree.right)
    return tree

def get_subtree(stack):
    rightchild = stack.pop()
    if isinstance(rightchild, str):
        rightchild = TreeNode(rightchild)
    
    if stack:
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
    else:
        tree = rightchild
    return tree

def build_tree(formula):
    # symbols definition
    connectives = ['⊐', '∧', '∨', '∼', '*']

    stack = [] # for storing temporal symbols
    q = 0
    varbool = False
    countopen = 0
    countclose = 0
    for i in range(len(formula)):
        if q < len(formula):
            element = formula[q]
            if element == "(":
                countopen += 1
            if element == ")":
                countclose += 1
            if element in alphabet:
                varbool = True
                q += 1
                var = element
                if formula[q] == "_":
                    q += 1
                while formula[q].isnumeric():
                    var = var + formula[q]
                    q += 1
                element = var
                q -= 1
            if element in connectives or varbool:
                varbool = False
                #print("element: ", element)
                if element == '∼':
                    count = 1
                    while element == '∼':
                        if formula[q+1] == "(":
                            for i in range(count):
                                stack.append('∼')
                        elif formula[q+1] in alphabet:
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
    #print("open (: ", countopen)
    #print("close ): ", countclose)
    return tree

def main():
    for f in folders:
        if os.path.isdir(f):
            for filename in os.listdir(f):
                if filename.endswith('.txt'):
                    print(filename)
                    current_path = "".join((os.getcwd(), "/", f, "/", filename))
                    with open(current_path) as topo_file:
                        formbool = False
                        formula = []
                        for line in topo_file.readlines():
                            words = line.split()
							#print(words)
                            for w in words:
                                if "fof" in w:
                                    formbool = True
                            if not words:
                                formbool = False
                            if formbool:
                                if "fof" not in w:
                                    formula.append(words)

                    formulaitems = []
                    for item in formula:
                        formulaitems.append(''.join(item))
					
                    formulastring = ''.join(formulaitems)
                    formulastring = formulastring.rstrip('.')
                    formulastring = formulastring.replace("~", "∼")
                    formulastring = formulastring.replace("&", '∧')
                    formulastring = formulastring.replace("|", '∨')
                    formulastring = formulastring.replace("<=>", "*")
                    formulastring = formulastring.replace("=>", '⊐')
                    formulastring = formulastring.split(".")
					
                    parts = []
                    for item in formulastring:
                        item = item[:-1]
                        parts.append(item)

                    for formula in parts:
                        if "false" not in formula and "true" not in formula:
                            if "∨" in formula or "∧" in formula or "⊐" in formula or "~" in formula or "*" in formula:
                                #print("formula: ", formula)
                                tree = build_tree(formula)
                                tree = extenddoubleimplication(tree)
                                #print("after:")
                                #tree.inorder()
                                #print("\n")
                                start_time = time.time()
                                # apply tableau method to tree formula
                                if decision_procedure(tree):
                                    print("--- %s seconds ---" % (time.time() - start_time))
                                    print(formula, " is a tautology")
                                else:
                                    print("--- %s seconds ---" % (time.time() - start_time))
                                    print(formula, " is not a tautology")
					
if __name__ == '__main__':
    main()							
