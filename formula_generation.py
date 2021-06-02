from recursive_levels import RecursiveLevel, FormulaStructure
from tree_node import TreeNode, tree_formula
import pickle
from decision_procedure import decision_procedure

def generate_initial_level():
    file_to_store = open("stored_object.pickle", "wb")
    list_objects = []

    # recursive level 0
    recursive_level_0 = RecursiveLevel(0)
    formula = FormulaStructure(1, TreeNode("*"))
    recursive_level_0.add_formula(1, formula)
    list_objects.append(recursive_level_0)

    # recursive level 1
    recursive_level_1 = RecursiveLevel(1)
    formula = FormulaStructure(2, tree_formula("∼", None, "*"))
    recursive_level_1.add_formula(1, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, tree_formula("⊐", "*", "*"))
    recursive_level_1.add_formula(2, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, tree_formula("∧", "*", "*"))
    recursive_level_1.add_formula(2, formula)
    #variables_substitution(formula)

    formula = FormulaStructure(3, tree_formula("∨", "*", "*"))
    recursive_level_1.add_formula(2, formula)
    #variables_substitution(formula)
    
    list_objects.append(recursive_level_1)
    pickle.dump(list_objects, file_to_store)
    file_to_store.close()

def pattern_rules(level):
    file_to_read = open("stored_object.pickle", "rb")
    loaded_object = pickle.load(file_to_read)
    previous_recursive_level = loaded_object[level - 1]
    list_objects = []
    current_recursive_level = RecursiveLevel(level)
    
    # ∼Rn
    for key in list(previous_recursive_level.formulas.keys()):
        list_formulas = previous_recursive_level.formulas[key]
        for formula in list_formulas:
            new_formula = tree_formula("∼", None, formula.formula)
            new_formula_structure = FormulaStructure(formula.characters + 1, new_formula)
            current_recursive_level.add_formula(key, new_formula_structure)
    
    # Rn * Rn
    for key1 in list(previous_recursive_level.formulas.keys()):
        list_formulas1 = previous_recursive_level.formulas[key1]
        for formula1 in list_formulas1:
            for key2 in list(previous_recursive_level.formulas.keys()):
                list_formulas2 = previous_recursive_level.formulas[key2]
                for formula2 in list_formulas2:
                    new_formula = tree_formula("⊐", formula1.formula, formula2.formula)
                    new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    
                    new_formula = tree_formula("∧", formula1.formula, formula2.formula)
                    new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    
                    new_formula = tree_formula("∨", formula1.formula, formula2.formula)
                    new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    

    # Rn * Rn0->Rn-1 and Rn0->Rn-1 * Rn
    for level in loaded_object[:-1]:
        list_objects.append(level)
        for key1 in list(previous_recursive_level.formulas.keys()):
            list_formulas1 = previous_recursive_level.formulas[key1]
            for formula1 in list_formulas1:
                for key2 in list(level.formulas.keys()):
                    list_formulas2 = level.formulas[key2]
                    for formula2 in list_formulas2:
                        new_formula = tree_formula("⊐", formula1.formula, formula2.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("⊐", formula2.formula, formula1.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∧", formula1.formula, formula2.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∧", formula2.formula, formula1.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∨", formula1.formula, formula2.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∨", formula2.formula, formula1.formula)
                        new_formula_structure = FormulaStructure(formula1.characters + formula2.characters + 1, new_formula)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)
    
    list_objects.append(previous_recursive_level)
    file_to_read.close()

    list_objects.append(current_recursive_level)
    file_to_store = open("stored_object.pickle", "wb")
    pickle.dump(list_objects, file_to_store)
    file_to_store.close()

def formula_generator():
    generate_initial_level()
    level = 2

    while level < 4:
        pattern_rules(level)
        level += 1

    file_to_read = open("stored_object.pickle", "rb")
    loaded_object = pickle.load(file_to_read)
    for level in loaded_object:
        print("Level: ", level.level)
        for key in list(level.formulas.keys()):
            print("Variables: ", key)
            list_formulas = level.formulas[key]
            for formula in list_formulas:
                formula.formula.inorder()
                print("\n")
    
    file_to_read.close()
