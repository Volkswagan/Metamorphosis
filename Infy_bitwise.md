```python
from typing import List

class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for i in range(32):
            bit = (n >> i) & 1
            res += (bit << (31 - i))
        return res
    
    def hammingWeight(self, n: int) -> int: #number of 1's bit
        res = 0
        while n:
            n &= n - 1
            res += 1
        return res
    
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        offset = 1

        for i in range(1, n + 1):
            if offset * 2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]
        return dp
    
    def getSum(self, a: int, b: int) -> int: #sum of two integers
        def add(a, b):
            if not a or not b:
                return a or b
            return add(a ^ b, (a & b) << 1)

        if a * b < 0:  # assume a < 0, b > 0
            if a > 0:
                return self.getSum(b, a)
            if add(~a, 1) == b:  # -a == b
                return 0
            if add(~a, 1) < b:  # -a < b
                return add(~add(add(~a, 1), add(~b, 1)), 1)  # -add(-a, -b)

        return add(a, b)  # a*b >= 0 or (-a) > b > 0
    
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res = n ^ res
        return res
    
    def missingNumber(self, nums: List[int]) -> int:
        res = len(nums)

        for i in range(len(nums)):
            res += i - nums[i]
        return res
    
    def missingNumber_xor(self, nums: List[int]) -> int:
        xor1 = 0
        xor2 = 0
        # XOR all array elements
        for num in nums:
            xor2 ^= num
        # XOR all numbers from 1 to n
        for i in range(1, len(nums)+1):
            xor1 ^= i
        # Missing number is the XOR of xor1 and xor2
        return xor1 ^ xor2
    
# Driver Program
if __name__ == "__main__":
    # Test case 1
    nums = [4, 1, 2, 1, 2]
    solution = Solution()
    result = solution.singleNumber(nums)
    print(f"The single number in {nums} is: {result}")
    result1 = solution.missingNumber(nums)
    print(f"The missing number in {nums} is: {result1}")

    # Test case 2
    nums = [2, 2, 1]
    result = solution.singleNumber(nums)
    print(f"The single number in {nums} is: {result}")
    result1 = solution.missingNumber_xor(nums)
    print(f"The missing number in {nums} is: {result1}")

    # Test case 3
    nums = [1]
    result = solution.singleNumber(nums)
    print(f"The single number in {nums} is: {result}")
    result1 = solution.missingNumber(nums)
    print(f"The missing number in {nums} is: {result1}")

```
