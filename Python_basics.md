1. Monkey patching refers to modifying or extending code at runtime, which can be powerful but also dangerous and difficult to maintain.
2. The is operator checks for object identity, while == checks for value equality.
3. Python does not support function overloading in the traditional sense, but similar behavior can be achieved using default arguments or variable-length arguments.
4.  Python supports multiple inheritance and uses the Method Resolution Order (MRO) to determine the order in which base classes are searched when executing a method.
5. Starting from Python 3.7, dictionaries maintain insertion order.
6. Lists and dictionaries are mutable, whereas tuples, strings, and frozensets are immutable.
7. Dictionary keys and set elements must be hashable, which generally means they must be immutable.
8. None is a singleton in Python, meaning there's only one instance of None in a Python process.
9. The variable used in a list comprehension is local to the comprehension and doesn't leak into the enclosing scope (from Python 3.x onward).
10. Python is dynamically typed or loosely typed, meaning the type of a variable is determined at runtime.
11. Functions in Python are first-class citizens, meaning they can be passed as arguments to other functions, returned as values from other functions, and assigned to variables. Python functions support positional, keyword, and arbitrary argument lists, and the order in which they are declared is significant.
12. PEP 8 is the style guide for Python code, outlining conventions for writing clean, readable code.
13. Copying a list in Python using = only creates a reference to the original list, while copy() or slicing ([:]) creates a shallow copy.
14. True Division (/): Works with both integers and floats but always returns a float.
    Floor Division (//): The result is always rounded down to the nearest integer, even if the result is a float. For negative numbers, it rounds towards the lower number.
    ```python
    print(-9.0 / 2) # -4.5
    print(-9.0 // 2)  # -5.0 (floors towards the lesser integer)
    ```
15. one-liners:
     ```python
     reversed_string = string[::-1]
     is_palindrome = string == string[::-1]
     reversed_list = my_list[::-1]
     last_element = my_list[-1]
     first_n_elements = my_list[:n]
     max_value = max(my_list)
     max_index = my_list.index(max(my_list))
     a, b = b, a #swapping
     intersection = list(set(list1) & set(list2))
     all_unique = len(my_list) == len(set(my_list))
     is_empty = not my_list
     most_frequent_in_a_list = max(set(my_list), key=my_list.count)
     even_numbers = list(range(0, n+1, 2)) #Create a List of Even Numbers up to a Given Number
     has_odd = any(x % 2 != 0 for x in my_list)
     single_integer = int(''.join(map(str, my_list))) #Convert a List of Integers to a Single Integer
     merged_dict = {**dict1, **dict2}
     transposed_matrix = list(zip(*matrix))
     no_whitespace = my_string.strip()

     #Count Occurrences of Each Element in a List
     from collections import Counter
     counts = Counter(my_list)
    ```
    
