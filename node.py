# Definition for a binary tree node.
class Node(object):
    def __init__(self, val=" ", left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):
    def __init__(self, postfix_exp):
        self.exp = postfix_exp
        self.root = None
        self.createTree(self.exp)

    def createTree(self, s):
        """
        :type s: str
        :rtype: Node
        """
        def compute(operands, operators):
            right, left = operands.pop(), operands.pop()
            operands.append(Node(val=operators.pop(), left=left, right=right))

        precedence = {'+':0, '-':0, '*':1, '/':1}
        operands, operators, operand = [], [], 0
        for i in xrange(len(s)):
            if s[i].isdigit():
                operand = operand*10 + int(s[i])
                if i == len(s)-1 or not s[i+1].isdigit():
                    operands.append(Node(val=str(operand)))
                    operand = 0
            elif s[i] == '(':
                operators.append(s[i])
            elif s[i] == ')':
                while operators[-1] != '(':
                    compute(operands, operators)
                operators.pop()
            elif s[i] in precedence:
                while operators and operators[-1] in precedence and \
                      precedence[operators[-1]] >= precedence[s[i]]:
                    compute(operands, operators)
                operators.append(s[i])
        while operators:
            compute(operands, operators)
        return operands[-1]

    def inorder(self, head):
        # inorder traversal of expression tree
        # inorder traversal = > left, root, right
        if head.left:
            self.inorder(head.left)
        print(head.data, end=" ")
        if head.right:
            self.inorder(head.right)

    def infixExp(self):
        # inorder traversal of expression tree give infix expression
        self.inorder(self.root)
        print()

if __name__ == "__main__":
   exp = "p⊐∼∼p"
   et = Solution(exp)
   et.infixExp()