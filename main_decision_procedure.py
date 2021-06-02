from tree_node import TreeNode
from formula_tree import build_tree
from decision_procedure import decision_procedure
from formula_generation import formula_generator

def main():
    #formula = "q⊐(p⊐q)" # tautology - correct
    #formula = "p⊐∼∼p" # tautology - correct
    #formula = "∼p⊐(p⊐q)" # tautology - correct
    #formula = "(p∧∼p)⊐q" # tautology - correct
    #formula = "p⊐(q∨∼q)" # not a tautology - correct
    #formula = "∼(p∧∼p)" # tautology - correct
    #formula = "∼∼(p∨∼p)" # tautology - correct
    #formula = "p∧∼p" # not a tautology - correct
    #formula = "p⊐q" # not a tautology - correct
    #formula = "(p⊐q)⊐(∼q⊐∼p)" # tautology - correct
    #formula = "∼p⊐∼p" # tautology - correct
    #formula = "p⊐p" # tautology - correct
    #formula = "∼p∨p" # not a tautology - correct
    #formula = "∼p∨∼p" # not a tautology - correct
    #formula = "∼p⊐q" # not a tautology - correct
    #formula = "(q∧p)⊐p" # tautology - correct
    formula = "∼∼∼*"
    print("Given formula: ", formula)
    
    # convert formula to tree
    #tree = build_tree(formula)
    tree = TreeNode("∼")
    rightfirst = TreeNode("∼")
    leaf = TreeNode("*")
    rightfirst.add_child_right(leaf)
    rightsecond = TreeNode("∼")
    rightsecond.add_child_right(rightfirst)
    tree.add_child_right(rightsecond)

    # apply tableau method to tree formula
    if decision_procedure(tree):
        print(formula, " is a tautology")
    else:
        print(formula, " is not a tautology")

    #formula_generator()
    

if __name__ == '__main__':
    main()