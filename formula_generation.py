from recursive_levels import RecursiveLevel, FormulaStructure
from tree_node import TreeNode
import pickle
from decision_procedure import decision_procedure

def create_tree_formula(data, left, right):
    tree = TreeNode(data)
    if left != None:
        tree.add_child_left(TreeNode(left))
    if right != None:
        tree.add_child_right(TreeNode(right))
    return tree

def variables_substitution(formulaStructure):
    characters = formulaStructure.characters
    tree = formulaStructure.formula
    # substitute variables
    # apply tableau method to all the formulas generated
    # decision_procedure(tree)

def generate_initial_level():
    file_to_store = open("stored_object.pickle", "wb")
    list_objects = []

    # recursive level 0
    recursive_level_0 = RecursiveLevel(0)
    formula = FormulaStructure(1, TreeNode("x"))
    recursive_level_0.add_formula(1, formula)
    list_objects.append(recursive_level_0)

    # recursive level 1
    recursive_level_1 = RecursiveLevel(1)
    formula = FormulaStructure(2, create_tree_formula("∼", None, "x"))
    recursive_level_1.add_formula(1, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, create_tree_formula("⊐", "x", "x"))
    recursive_level_1.add_formula(2, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, create_tree_formula("∧", "x", "x"))
    recursive_level_1.add_formula(2, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, create_tree_formula("∨", "x", "x"))
    recursive_level_1.add_formula(2, formula)
    list_objects.append(recursive_level_1)
    #variables_substitution(formula)
    pickle.dump(list_objects, file_to_store)
    file_to_store.close()


def add_negation(tree):
    negation = TreeNode("∼")
    negation.add_child_right(tree)
    return negation

def add_conjunction(tree1, tree2):
    tree = TreeNode("∧")
    tree.add_child_left(tree1)
    tree.add_child_right(tree2)
    return tree

def add_disjunction(tree1, tree2):
    tree = TreeNode("∨")
    tree.add_child_left(tree1)
    tree.add_child_right(tree2)
    return tree

def add_implication(tree1, tree2):
    tree = TreeNode("⊐")
    tree.add_child_left(tree1)
    tree.add_child_right(tree2)
    return tree

def pattern_rules(recursive_level):
    file_to_read = open("stored_object.pickle", "rb")
    loaded_object = pickle.load(file_to_read)
    previous_recursive_level = loaded_object[recursive_level.level - 1]
    
    # ∼Rn
    for key in list(previous_recursive_level.formulas.keys()):
        list_formulas = previous_recursive_level.formulas[key]
        for formula in list_formulas:
            new_formula = add_negation(formula.formula)
            new_formula.inorder()
            new_formula = FormulaStructure(formula.characters, new_formula)
            recursive_level.add_formula(1, new_formula)
    
    # Rn * Rn
    for key1 in list(previous_recursive_level.formulas.keys()):
        list_formulas1 = previous_recursive_level.formulas[key1]
        for formula1 in list_formulas1:
            for key2 in list(previous_recursive_level.formulas.keys()):
                list_formulas2 = previous_recursive_level.formulas[key2]
                for formula2 in list_formulas2:
                    new_formula = add_implication(formula1, formula2)
                    recursive_level.add_formula(2, new_formula)
                    new_formula = add_conjunction(formula1, formula2)
                    recursive_level.add_formula(2, new_formula)
                    new_formula = add_disjunction(formula1, formula2)
                    recursive_level.add_formula(2, new_formula)
                    

    # Rn * Rn0->Rn-1 and Rn0->Rn-1 * Rn
    for level1 in loaded_object:
        for level2 in loaded_object:
             for key1 in list(level1.formulas.keys()):
                list_formulas1 = level1.formulas[key1]
                for formula1 in list_formulas1:
                    for key2 in list(level2.formulas.keys()):
                        list_formulas2 = level2.formulas[key2]
                        for formula2 in list_formulas2:
                            new_formula = add_implication(formula1, formula2)
                            recursive_level.add_formula(2, new_formula)
                            new_formula = add_conjunction(formula1, formula2)
                            recursive_level.add_formula(2, new_formula)
                            new_formula = add_disjunction(formula1, formula2)
                            recursive_level.add_formula(2, new_formula)

    file_to_read.close()
    return recursive_level

def formula_generator():
    generate_initial_level()
    
    recursive_level = RecursiveLevel(2)
    recursive_level = pattern_rules(recursive_level)
    
    #file_to_store = open("stored_object.pickle", "wb")
    #pickle.dump(recursive_level, file_to_store)
    #file_to_store.close()

"""
level = 2

while True:
    print("Generating formulas...")
    recursive_level = RecursiveLevel(level)

    # generate formula structures
    recursive_level = pattern_rules(recursive_level, file_to_store)

    # store recursive level
    pickle.dumps(recursive_level, file_to_store)

    # increase recursive level
    level += 1
"""
