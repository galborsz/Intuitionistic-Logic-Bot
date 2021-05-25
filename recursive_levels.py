
class Level:
    def __init__(self, recursive_level):
        self.recursive_level = recursive_level
        self.formulas = {} # the key of the dict represents the number of variables in the formula 
                            # and the value is a list with all the formulas with that amount of variables
    
    def add_formula(self, var_num, formula):
        if self.formulas.has_key(var_num):
            self.formulas[var_num].append(formula)
        else:
            self.formulas[var_num] = []
            self.formulas[var_num].append(formula)

class FormulaStructure:
    def __init__(self, characters, formula):
        self.characters = characters # total amount of characters in the formula
        self.formula = formula # tree structure