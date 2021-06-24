from recursive_levels import ComplexityLevel, LogicalStructure
from tree_node import TreeNode, tree_formula
from variables_substitution import variables_substitution
import pickle
from time import process_time
import globals

def generate_initial_level():
    file_to_store = open("stored_object.pickle", "wb")
    list_objects = []

    # initialize recursive level 0
    recursive_level_0 = ComplexityLevel(0)
    formula = LogicalStructure(1, TreeNode("*"))
    recursive_level_0.add_formula(1, formula)
    list_objects.append(recursive_level_0)

    # initialize recursive level 1
    recursive_level_1 = ComplexityLevel(1)
    globals.start_time_generation = process_time()
    formula = LogicalStructure(4, tree_formula("∼", None, "*"))
    variables_substitution(1, formula.formula.copy(), 1, 1, 4, 1)
    recursive_level_1.add_formula(1, formula)
    
    formula = LogicalStructure(5, tree_formula("⊐", "*", "*"))
    variables_substitution(2, formula.formula.copy(), 1, 1, 5, 1)
    recursive_level_1.add_formula(2, formula)

    formula = LogicalStructure(5, tree_formula("∧", "*", "*"))
    variables_substitution(2, formula.formula.copy(), 1, 1, 5, 1)
    recursive_level_1.add_formula(2, formula)

    formula = LogicalStructure(5, tree_formula("∨", "*", "*"))
    variables_substitution(2, formula.formula.copy(), 1, 1, 5, 1)
    recursive_level_1.add_formula(2, formula)
    
    list_objects.append(recursive_level_1)
    pickle.dump(list_objects, file_to_store)
    file_to_store.close()

def pattern_rules(level, total_tautologies, total_formulas):
    file_to_read = open("stored_object.pickle", "rb")
    loaded_object = pickle.load(file_to_read)
    previous_recursive_level = loaded_object[level - 1]
    list_objects = []
    current_recursive_level = ComplexityLevel(level)

    # ∼Rn
    for key in list(previous_recursive_level.formulas.keys()):
        list_formulas = previous_recursive_level.formulas[key]
        for formula in list_formulas:
            new_formula = tree_formula("∼", None, formula.formula)
            new_formula_structure = LogicalStructure(formula.characters + 3, new_formula)
            variables_substitution(key, new_formula_structure.formula.copy(), 1, 1, formula.characters + 3, level)
            current_recursive_level.add_formula(key, new_formula_structure)
    
    # Rn * Rn
    for key1 in list(previous_recursive_level.formulas.keys()):
        list_formulas1 = previous_recursive_level.formulas[key1]
        for formula1 in list_formulas1:
            for key2 in list(previous_recursive_level.formulas.keys()):
                list_formulas2 = previous_recursive_level.formulas[key2]
                for formula2 in list_formulas2:
                    new_formula = tree_formula("⊐", formula1.formula, formula2.formula)
                    new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                    variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    
                    new_formula = tree_formula("∧", formula1.formula, formula2.formula)
                    new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                    variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    
                    new_formula = tree_formula("∨", formula1.formula, formula2.formula)
                    new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                    variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                    current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                    

    # Rn * Rn0->Rn-1 and Rn0->Rn-1 * Rn
    for level1 in loaded_object[:-1]:
        list_objects.append(level1)
        for key1 in list(previous_recursive_level.formulas.keys()):
            list_formulas1 = previous_recursive_level.formulas[key1]
            for formula1 in list_formulas1:
                for key2 in list(level1.formulas.keys()):
                    list_formulas2 = level1.formulas[key2]
                    for formula2 in list_formulas2:
                        new_formula = tree_formula("⊐", formula1.formula, formula2.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("⊐", formula2.formula, formula1.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)
                        
                        new_formula = tree_formula("∧", formula1.formula, formula2.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∧", formula2.formula, formula1.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∨", formula1.formula, formula2.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)

                        new_formula = tree_formula("∨", formula2.formula, formula1.formula)
                        new_formula_structure = LogicalStructure(formula1.characters + formula2.characters + 3, new_formula)
                        variables_substitution(key1 + key2, new_formula_structure.formula.copy(), 1, 1, formula1.characters + formula2.characters + 3, level)
                        current_recursive_level.add_formula(key1 + key2, new_formula_structure)
    
    list_objects.append(previous_recursive_level)
    file_to_read.close()

    list_objects.append(current_recursive_level)
    file_to_store = open("stored_object.pickle", "wb")
    pickle.dump(list_objects, file_to_store)
    file_to_store.close()

def formula_generator():

    # generate recusrive levels 0 and 1
    generate_initial_level()
    level = 2

    
    while True:
        # generate all recursive levels in increasing order
        pattern_rules(level)
        level += 1
    
    
