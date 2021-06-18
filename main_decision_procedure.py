from tree_node import TreeNode
from formula_tree import build_tree
from decision_procedure import decision_procedure
from tree_node import treeToString

import time
start_time = time.time()

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
    #formula = "∼∼∼p" # not a tautology - correct
    #formula = "∼∼∼(a⊐b)" # not a tautology - correct
    #formula = "∼((a⊐b)⊐a)" # not a tautology - correct
    #formula = "(∼((∼a)⊐(∼b)))"
    #formula = "(∼(a⊐(a∨a)))" # not a tautology - correct
    #formula = "((∼(∼a))⊐(∼(∼a)))" # not a tautology - correct - infinite
    #formula = "(a⊐(a∨a))" # tautology - correct
    #formula = "((∼(a∧b))⊐(∼(a∧a)))" # not a tautology
    #formula = "((∼(∼a))∧((a∨a)⊐(b⊐b)))" # not a tautology
    #formula = "(((a∨b)∨(∼a))⊐((a⊐a)⊐(c⊐c)))" # tautology - correct
    #formula = "(((a∨b)∨(∼a))⊐((a⊐b)⊐(c⊐d)))"
    #formula = "(∼(∼((∼a)∧(∼a))))" # not a tautology - correct
    #formula = "(∼(∼((∼a)∧(∼a))))" # not working
    #formula = "(∼(∼a))" # not a tautology - correct
    #formula = "(∼(∼(a⊐b)))"
    #formula = "(∼((a⊐a)⊐a))" 
    #formula = "(((∼a)⊐a)⊐(∼(∼a)))"
    #formula = "((∼a)⊐a)"
    #formula = "(a∧b)⊐(a∧b)"
    #formula = "a∧(a⊐a)"
    #formula = "(((p∨q)⊐(p∨r))⊐(p∨(q⊐r)))" # not a tautology - correct
    #formula = "(p∨(~(~(~p))))"
    formula = "(~(p⊐q)⊐(q⊐p))"
    print("Given formula: ", formula)
    
    # convert formula to tree

    tree = build_tree(formula)
    tree.inorder()
    line = []
    treeToString(tree, line)
    print("tautology: ", ''.join(line))

    # apply tableau method to tree formula
    if decision_procedure(tree):
        print("--- %s seconds ---" % (time.time() - start_time))
        print(formula, " is a tautology")
    else:
        print("--- %s seconds ---" % (time.time() - start_time))
        print(formula, " is not a tautology")

    #formula_generator()
    

if __name__ == '__main__':
    main()