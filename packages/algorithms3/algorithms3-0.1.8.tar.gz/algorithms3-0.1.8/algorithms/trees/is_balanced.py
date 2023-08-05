'''
Given a binary tree, determine if it is height-balanced.

For this problem, a height-balanced binary tree is defined as:

a binary tree in which the depth of the two subtrees of every node never differ by more than 1.

Example 1:

Given the following tree [3,9,20,null,null,15,7]:

    3
   / \
  9  20
    /  \
   15   7
Return true.

Example 2:

Given the following tree [1,2,2,3,3,null,null,4,4]:

       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
Return false.
'''

def is_balanced(root): 

    def height(root):
        if root is None:
            return 0
        else:
            return 1 + max(height(root.left), height(root.right))

    if root is None:
        return True
            
    lheight = height(root.left)
    rheight = height(root.right)

    if abs(lheight-rheight) <= 1 and is_balanced(root.left) and is_balanced(root.right):
        return True
    
    return False 

