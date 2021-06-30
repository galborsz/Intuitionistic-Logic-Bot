# Intuitionistic-Logic-Bot
## Abstract
The present program is an implementation of an intuitionistic propositional logic bot that publishes a tautology every day on Twitter. In general, our implementation consists  of  two  main  different procedures: a formula generator and the theorem prover itself, which is based on a tableau-based method with a possible worlds semantics. Those formulas that are concluded to be tautologies by our decision procedure are eventually posted on Twitter. 

The approach that is suggested in this study aims for high efficiency. Such efficiency is understood in terms of the time the system takes to check whether a generated formula is a tautology, with respect to its length. In order to achieve our goal, we propose some techniques to narrow the search space, which results in a lower memory cost and less time needed for reaching a final decision. Moreover, we also present a new method to guarantee the intended exhaustivity and efficiency of our formula generator.

The results we obtained after testing our program, evidence the satisfactory performance of our implementation, which allows us to conclude the expected feasibility of the implementation of an efficient theorem prover in intuitionistic propositional logic.

## How to run the program
1) Make sure that you have the following libraries installed:
* Tweepy
* Pickle

2) Navigate to the folder with all the code
3) Run the code by using the following command:
```python3 main.py```
