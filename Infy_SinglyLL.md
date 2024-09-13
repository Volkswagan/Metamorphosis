```python
# Definition for singly-linked list node.
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

# Implementation for Singly Linked List
class LinkedList:
    def __init__(self):
        # Init the list with a 'dummy' node
        self.head = ListNode(-1)
        self.tail = self.head

    def insertEnd(self, val):
        self.tail.next = ListNode(val)
        self.tail = self.tail.next

    def remove(self, index):
        i = 0
        curr = self.head
        while i < index and curr:
            i += 1
            curr = curr.next

        # Remove the node ahead of curr
        if curr and curr.next:
            if curr.next == self.tail:
                self.tail = curr
            curr.next = curr.next.next

    def print(self):
        curr = self.head.next
        while curr:
            print(curr.val, " -> ", end="")
            curr = curr.next
        print()

    # Function to reverse a linked list
    def reverse(self):
        prev = None
        curr = self.head.next
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head.next = prev

    # Function to detect cycle in linked list
    def hasCycle(self):
        slow = fast = self.head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    # Function to add an element at the nth position
    def insertAt(self, val, n):
        new_node = ListNode(val)
        curr = self.head
        i = 0
        while i < n and curr.next:
            curr = curr.next
            i += 1
        new_node.next = curr.next
        curr.next = new_node

    # Function to remove the nth node from the end of the list
    def removeNthFromEnd(self, n):
        fast = slow = self.head
        # Move fast n+1 steps ahead
        for _ in range(n + 1):
            if fast:
                fast = fast.next
            else:
                return  # n is larger than the list size
        # Move both fast and slow till fast reaches the end
        while fast:
            fast = fast.next
            slow = slow.next
        # Remove the nth node from end
        slow.next = slow.next.next
        if slow.next is None:
            self.tail = slow


# Function to merge two sorted linked lists
def mergeTwoLists(l1, l2):
    dummy = ListNode(-1)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next


# Testing the code

# Input for first list
ll1 = LinkedList()
ll1.insertEnd(1)
ll1.insertEnd(3)
ll1.insertEnd(5)
ll1.insertEnd(7)

# Input for second list
ll2 = LinkedList()
ll2.insertEnd(2)
ll2.insertEnd(4)
ll2.insertEnd(6)
ll2.insertEnd(8)

# Print original linked lists
print("Original Linked List 1:")
ll1.print()

print("Original Linked List 2:")
ll2.print()

# Add element at the 2nd position in Linked List 1
ll1.insertAt(10, 2)
print("Linked List 1 after adding 10 at position 2:")
ll1.print()

# Remove the 2nd node from the end of Linked List 1
ll1.removeNthFromEnd(2)
print("Linked List 1 after removing 2nd node from end:")
ll1.print()

# Check for cycle in Linked List 1
has_cycle = ll1.hasCycle()
print(f"Linked List 1 has a cycle: {has_cycle}")

# Reverse the first linked list
ll1.reverse()
print("Reversed Linked List 1:")
ll1.print()

# Merging two sorted linked lists
merged_head = mergeTwoLists(ll1.head.next, ll2.head.next)
print("Merged Sorted Lists:")

# Print merged list
curr = merged_head
while curr:
    print(curr.val, " -> ", end="")
    curr = curr.next
print()

```
