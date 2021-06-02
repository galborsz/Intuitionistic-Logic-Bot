
import string
from tree_node import TreeNode
from formula_tree import build_tree
from decision_procedure import decision_procedure



def traversal_replace(var, formula):
    if formula.data == "*":
        formula.data = var
        return True
    
    if formula.left:
        assigned = traversal_replace(var, formula.left)
        if assigned:
            return True

    if formula.right:
        assigned = traversal_replace(var, formula.right)
        if assigned:
            return True
    
    return False

    

def variables_substitution(var_num, formula, maxim, level):
    if level == var_num + 1:
        if decision_procedure(formula):
            formula.inorder()
            print(" is a tautology")
        else:
            formula.inorder()
            print(" is not a tautology")
        return

    alphabet = list(string.ascii_lowercase)
    
    for i in range(maxim):
        if i == maxim - 1:
            maxim = maxim + 1
            new_formula = formula
        else:
            new_formula = formula.copy()
        traversal_replace(alphabet[i], new_formula)
        variables_substitution(var_num, new_formula, maxim, level+1)    

def main():
    root = TreeNode("⊐")
    left = TreeNode("⊐")
    left.add_child_left(TreeNode("*"))
    left.add_child_right(TreeNode("*"))

    right = TreeNode("⊐")
    right.add_child_left(TreeNode("*"))
    right.add_child_right(TreeNode("*"))

    root.add_child_left(left)
    root.add_child_right(right)
    root.inorder()
    print("\n")
    variables_substitution(4, root, 1, 1)

if __name__ == '__main__':
    main()
