''''
Merge two sorted linked lists and return it as a new list. The new list 
should be made by splicing together the nodes of the first two lists.

Example:

Input: 1->2->4, 1->3->4
Output: 1->1->2->3->4->4


Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
'''
from .singly_linked_list_implementation import Node as ListNode
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    newList = ListNode(0)
    current = newList
    
    while l1 and l2:
        if l1.val < l2.val:
            newNode = ListNode(l1.val)
            l1 = l1.next
        else:
            newNode = ListNode(l2.val)
            l2 = l2.next
        
        current.next = newNode
        current = current.next
        
    current.next = l1 or l2
    return newList.next
