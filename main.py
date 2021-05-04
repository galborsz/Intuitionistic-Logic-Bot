from tree import TreeNode, build_tree
from tableau import iterative_preorder

def main():
    #formula = "q⊐(p⊐q)"
    #formula = "p⊐∼∼p"
    #formula = "∼p⊐(p⊐q)"
    #formula = "(p∧∼p)⊐q"
    #formula = "p⊐(q∨∼q)"
    formula = "∼(p∧∼p)"
    #formula = "p⊐q"

    # convert formula to tree
    tree = build_tree(formula)
    tree.inorder()
    # apply tableau method to tree formula
    validity = iterative_preorder(tree)
    if validity:
        print(formula, " is not a tautology")
    else:
        print(formula, " is a tautology")

if __name__ == '__main__':
    main()