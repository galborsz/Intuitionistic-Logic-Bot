
import string
from decision_procedure import decision_procedure

# global variable
alphabet = list(string.ascii_lowercase)

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
    #print("\nformula: \n")
    #formula.inorder()
    #print("\n")
    if level == var_num + 1:
        if decision_procedure(formula):
            formula.inorder()
            print(" is a tautology")
        return
    
    for i in range(maxim):
        if i == maxim - 1:
            maxim = maxim + 1
            new_formula = formula
        else:
            new_formula = formula.copy()
        traversal_replace(alphabet[i], new_formula)
        variables_substitution(var_num, new_formula, maxim, level+1)    
