'''
Implement int sqrt(int x).

Compute and return the square root of x, where x is guaranteed to be 
a non-negative integer.

Since the return type is an integer, the decimal digits are truncated 
and only the integer part of the result is returned.

Example 1:

Input: 4
Output: 2
Example 2:

Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since 
             the decimal part is truncated, 2 is returned.
'''

def sqrt_number(x):
    left, right = 1, x
    result = 0
    while left <= right:
        mid = (left + right) // 2
        if mid*mid == x:
            answer = mid
            return mid
        elif mid*mid < x:
            left = mid + 1
            answer = mid
        else:
            right = mid - 1

    return answer