
import string
from decision_procedure import decision_procedure
from tree_node import treeToString
from keys_format import *

import tweepy
import time
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.


# global variables
alphabet = list(string.ascii_lowercase)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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

def variables_substitution(var_num, formula, maxim, level):
    if level == var_num + 1:
        if decision_procedure(formula):
            # post in Twitter
            line = []
            treeToString(formula, line)
            api.update_status(''.join(line))
            time.sleep(60)
        return
    
    for i in range(maxim):
        if i == maxim - 1:
            maxim = maxim + 1
            new_formula = formula
        else:
            new_formula = formula.copy()
        traversal_replace(alphabet[i], new_formula)
        variables_substitution(var_num, new_formula, maxim, level+1)    
