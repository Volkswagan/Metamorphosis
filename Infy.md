```python
def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))

def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevMap = {}  # val -> index
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i

def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        countS, countT = {}, {}
        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)
        return countS == countT

def maxSubArray(nums):
    # Initialize current sum and max sum
    current_sum = max_sum = nums[0]
    # Traverse through the list starting from the second element
    for num in nums[1:]:
        # Update current sum to either the current number itself or the sum including the current number
        current_sum = max(num, current_sum + num)
        # Update max sum to the largest value seen so far
        max_sum = max(max_sum, current_sum)
    return max_sum

def dutchNationalFlag(nums):
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[high], nums[mid] = nums[mid], nums[high]
            high -= 1

def moveZeroes(nums):
    # Pointer for the position of the next non-zero element
    non_zero_index = 0

    # Traverse the array and move non-zero elements to the front
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[non_zero_index], nums[i] = nums[i], nums[non_zero_index]
            non_zero_index += 1










for i in range(len(nums) - 1, -1, -1):
    print(i)

```
