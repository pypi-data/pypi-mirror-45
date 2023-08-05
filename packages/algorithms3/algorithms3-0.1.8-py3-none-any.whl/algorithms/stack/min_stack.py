'''
Design a stack that supports push, pop, top, and retrieving the 
minimum element in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.
'''

class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []

    def push(self, x: int) -> None:
        curr_min = self.getMin()
        if curr_min is None or x < curr_min:
            curr_min = x
        self.stack.append((x, curr_min))
        
    def pop(self) -> None:
        if not self.stack: raise IndexError
        self.stack.pop()

    def top(self) -> int:
        if not self.stack: raise IndexError
        return self.stack[-1][0]

    def getMin(self) -> int:
        if not self.stack: return None
        return self.stack[-1][1]