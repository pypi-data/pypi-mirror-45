'''
Given an array with n integers, your task is to check if it could become non-decreasing by modifying at
 most 1 element.

We define an array is non-decreasing if array[i] <= array[i + 1] holds for every i (1 <= i < n).

Example 1:
Input: [4,2,3]
Output: True
Explanation: You could modify the first 4 to 1 to get a non-decreasing array.
Example 2:
Input: [4,2,1]
Output: False
Explanation: You can't get a non-decreasing array by modify at most one element.
'''

def non_decreasing_array(nums):
    count = None
    
    for i in range(len(nums)-1):
        if nums[i] > nums[i+1]:
            if count is not None: return False
            count = i 
    
    return (count is None or count == 0 or count == len(nums)-2 or 
            nums[count-1] <= nums[count+1] or nums[count] <= nums[count+2])