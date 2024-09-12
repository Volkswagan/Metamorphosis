1. **Decorators**:  
   A decorator is a function that takes another function as an argument and extends or alters its behavior without modifying the original function's code.
   ```python
   def decorator(func):
       def wrapper():
           print("Before function call")
           func()
           print("After function call")
       return wrapper

   @decorator
   def hello():
       print("Hello!")

   hello()  # Output: Before function call, Hello!, After function call
   ```

2. **Generators**:  
   A generator is a function that returns an iterator and allows you to iterate over a sequence of values lazily (one at a time) using the `yield` keyword.
   ```python
   def count_up_to(n):
       for i in range(1, n + 1):
           yield i

   for number in count_up_to(3):
       print(number)  # Output: 1, 2, 3
   ```

3. **Iterators**:  
   An iterator is an object with methods `__iter__()` and `__next__()` that allows you to iterate through a collection, returning one element at a time.
   ```python
   my_list = [1, 2, 3]
   my_iter = iter(my_list)
   
   print(next(my_iter))  # Output: 1
   print(next(my_iter))  # Output: 2
   ```

4. **Lambda Function**:  
   A lambda function is an anonymous, inline function defined with the `lambda` keyword, often used for short, throwaway functions.
   ```python
   square = lambda x: x ** 2
   print(square(4))  # Output: 16
   ```
########################################################################################################################################
Here’s a Python script that reads a text file, counts the words, writes the result to another text file, and handles exceptions gracefully using `sys.argv`:

```python
import sys

def count_words_in_file(input_file, output_file):
    try:
        # Read input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Count words
        words = content.split()
        word_count = len(words)

        # Write the word count to the output file
        with open(output_file, 'w') as file:
            file.write(f"Word count: {word_count}\n")

        print(f"Word count successfully written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for '{input_file}' or '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        count_words_in_file(input_file, output_file)
```

### Steps:
1. **`sys.argv`** is used to accept the input and output file paths from the command line.
2. The code reads the content from the input file, splits the content into words, and counts them.
3. The result is written to the specified output file.
4. It handles potential exceptions like:
   - **FileNotFoundError**: If the input file doesn't exist.
   - **PermissionError**: If there's an issue with file permissions.
   - **Other unexpected errors** are caught by a generic exception handler.

### How to run:
```bash
python script.py input.txt output.txt
```
