import string
import tweepy
from decision_procedure import decision_procedure
from tree_node import treeToString
from keys_format import *
import time
import globals 


# global variables
alphabet = list(string.ascii_lowercase)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# replaces the first free space in the skeleton (represented by the character *)
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

def variables_substitution(var_num, formula, maximum, level, characters, rec_level):
    
    if level == var_num + 1:        
        if characters <= 280 and decision_procedure(formula):  
            # post on Twitter only if formula is a tautology and has less than 280 characters
            line = []
            treeToString(formula, line)
            api.update_status(''.join(line))
            time.sleep(86400)
        return
    
    for i in range(maximum): 
        if i == maximum - 1:
            maximum = maximum + 1
            new_formula = formula
        else:
            new_formula = formula.copy()
        if i == len(alphabet): # there are no more available characters for representing propositional variables
            return
        traversal_replace(alphabet[i], new_formula)
        variables_substitution(var_num, new_formula, maximum, level+1, characters, rec_level) 