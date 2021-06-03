
import string
#import tweepy
import time
from decision_procedure import decision_procedure
from tree_node import treeToString
from keys_format import *

# global variables
alphabet = list(string.ascii_lowercase)
#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = tweepy.API(auth)

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

def variables_substitution(var_num, formula, maxim, level, characters):
    if level == var_num + 1:
        print("formula: ")
        formula.inorder()
        print("\n")
        if characters <= 240 and decision_procedure(formula):
            # post in Twitter
            line = []
            treeToString(formula, line)
            print("tautology: ", ''.join(line))
            #api.update_status(''.join(line))
            #time.sleep(60)
        return
    
    for i in range(maxim):
        if i == maxim - 1:
            maxim = maxim + 1
            new_formula = formula
        else:
            new_formula = formula.copy()
        traversal_replace(alphabet[i], new_formula)
        variables_substitution(var_num, new_formula, maxim, level+1, characters)    
