# https://github.com/codebasics/data-structures-algorithms-python/blob/master/data_structures/7_Tree/7_tree.py
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

    def inorder(self):
        if self.left:
            self.left.inorder()
        print(self.data, end = '')
        if self.right:
            self.right.inorder()

    def tree_to_string(self):
        node = self.inorder()
        while node:
            node = node + self.inorder()
        return node

    def add_child_left(self, left):
        if left != None:
            left.parent = self
        self.left = left

    def add_child_right(self, right):
        if right != None: 
            right.parent = self
        self.right = right