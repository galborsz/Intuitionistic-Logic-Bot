from recursive_levels import Level, FormulaStructure
from tree_node import TreeNode
import pickle

def create_tree_formula(data, left, right):
    tree = TreeNode(data)
    tree.add_child_left(left)
    tree.add_child_right(right)
    return tree

def generate_initial_levels(file_to_store):
    # recursive level 0
    recursive_level_0 = Level(0)
    formula = FormulaStructure(1, TreeNode("x"))
    recursive_level_0.add_formula(1, formula)
    pickle.dumps(recursive_level_0, file_to_store)

    # recursive level 1
    recursive_level_1 = Level(1)
    formula = FormulaStructure(2, create_tree_formula("∼", None, "x"))
    recursive_level_1.add_formula(1, formula)

    formula = FormulaStructure(3, create_tree_formula("⊐", "x", "x"))
    recursive_level_1.add_formula(2, formula)

    formula = FormulaStructure(3, create_tree_formula("∧", "x", "x"))
    recursive_level_1.add_formula(2, formula)

    formula = FormulaStructure(3, create_tree_formula("∨", "x", "x"))
    recursive_level_1.add_formula(2, formula)
    pickle.dumps(recursive_level_1, file_to_store)

def formula_generator():
    file_to_store = open("stored_object.pickle", "wb")
    generate_initial_levels(file_to_store)
    while True:
        print("Generating formulas...")
        recursive_level = Level(recursive_level)
        pickle.dumps(recursive_level, file_to_store)


"""
import pickle
import tweepy

class example_class:
    a_number = 35
    a_string = "hey"
    a_list = [1, 2, 3]
    a_dict = {"first": "a", "second": 2, "third": [1,2,3]}
    a_tuple = (22, 23)

my_object = example_class()
my_pickled_object = pickle.dumps(my_object)
print(f"This is my pickled object:\n{my_pickled_object}\n")

my_unpickled_object = pickle.loads(my_pickled_object)
print(f"a_dict of of unpickled object:\n{my_unpickled_object.a_dict}\n")
"""
