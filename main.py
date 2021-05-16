from formula_tree import build_tree
from decision_procedure import decision_procedure

def main():
    #formula = "q⊐(p⊐q)"
    #formula = "p⊐∼∼p"
    #formula = "∼p⊐(p⊐q)"
    #formula = "(p∧∼p)⊐q"
    #formula = "p⊐(q∨∼q)"
    #formula = "∼(p∧∼p)" # tautology - correct
    formula = "∼∼(p∨∼p)"
    #formula = "p∧∼p" # not a tautology - correct
    #formula = "p⊐q" # not a tautology - correct
    print("Given formula: ", formula)
    
    # convert formula to tree
    tree = build_tree(formula)
    #tree.inorder()


    # apply tableau method to tree formula
    if decision_procedure(tree):
        print(formula, " is a tautology")
    else:
        print(formula, " is not a tautology")

if __name__ == '__main__':
    main()