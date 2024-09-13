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

def isPalindrome(self, s: str) -> bool:
        new = ''
        for a in s:
            if a.isalpha() or a.isdigit():
                new += a.lower()
        return (new == new[::-1])

def best_time_buy_sell(self, prices: List[int]) -> int:
        res = 0
        lowest = prices[0]
        for price in prices:
            if price < lowest:
                lowest = price
            res = max(res, price - lowest)
        return res

def binary_search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            m = l + ((r - l) // 2)  # (l + r) // 2 can lead to overflow
            if nums[m] > target:
                r = m - 1
            elif nums[m] < target:
                l = m + 1
            else:
                return m
        return -1

def binarySearchSqrt(x):
    if x == 0 or x == 1:
        return x
    low, high = 0, x
    result = 0
    while low <= high:
        mid = (low + high) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            low = mid + 1
            result = mid
        else:
            high = mid - 1
    return result

def isValid(self, s: str) -> bool:
        Map = {")": "(", "]": "[", "}": "{"}
        stack = []
        for c in s:
            if c not in Map:
                stack.append(c)
                continue
            if not stack or stack[-1] != Map[c]:
                return False
            stack.pop()
        return not stack

def findPeakElement(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left

def findLeaders(arr):
    leaders = []
    max_from_right = arr[-1]
    leaders.append(max_from_right)
    for i in range(len(arr) - 2, -1, -1):
        if arr[i] > max_from_right:
            leaders.append(arr[i])
            max_from_right = arr[i]
    return leaders[::-1]

def rotateMatrix90(matrix):
    n = len(matrix)
    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
    return matrix

def unionOfSortedArrays(arr1, arr2):
    i, j = 0, 0
    union = []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            union.append(arr1[i])
            i += 1
        elif arr1[i] > arr2[j]:
            union.append(arr2[j])
            j += 1
        else:
            union.append(arr1[i])
            i += 1
            j += 1
    # Add remaining elements from arr1 or arr2
    while i < len(arr1):
        union.append(arr1[i])
        i += 1
    while j < len(arr2):
        union.append(arr2[j])
        j += 1
    return union
def rotateArray(nums, k):
    n = len(nums)
    k = k % n  # In case k > n
    nums[:] = nums[-k:] + nums[:-k]
    return nums

def kthSmallest(nums, k):
    nums.sort()
    return nums[k-1]
def kthLargest(nums, k):
    nums.sort(reverse=True)
    return nums[k-1]



for i in range(len(nums) - 1, -1, -1):
    print(i)

```
