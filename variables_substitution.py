
import string
#import tweepy
from decision_procedure import decision_procedure
from tree_node import treeToString
from keys_format import *
#import main
import time
import globals 


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

def variables_substitution(var_num, formula, maximum, level, characters, total_tautologies, total_formulas, rec_level):
    if rec_level not in total_tautologies.keys():
        total_tautologies[rec_level] = 0 # initialize counter
    if rec_level not in total_formulas.keys():
        total_formulas[rec_level] = 0 # initialize counter
        if rec_level > 1:
            print("RECURSIVE LEVEL: ", rec_level-1)
            print("TOTAL FORMULAS: ", total_formulas[rec_level-1])
            print("TOTAL TAUTOLOGIES: ", total_tautologies[rec_level-1])
    if level == var_num + 1:
        #print("rec level: ", rec_level)
        #print("formula: ")
        #formula.inorder()
        #print("\n")
        total_formulas[rec_level] += 1
        
        if characters <= 240 and decision_procedure(formula):
            print("--- %s seconds ---" % (time.time() - globals.start_time))
            total_tautologies[rec_level] += 1
                
            # post in Twitter
            line = []
            treeToString(formula, line)
            print("tautology: ", ''.join(line))
            #api.update_status(''.join(line))
            #time.sleep(60)
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
        variables_substitution(var_num, new_formula, maximum, level+1, characters, total_tautologies, total_formulas, rec_level)    
