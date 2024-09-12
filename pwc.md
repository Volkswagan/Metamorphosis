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


Here are some Python-specific tricky and complex interview questions asked in PwC interviews for data engineers, along with their answers:

### 1. **How do you handle large files in Python without reading the entire file into memory?**

#### Answer:
To process large files without loading them entirely into memory, you can read and process the file line by line using Python’s built-in `open()` function and iterate over the file object.

Example:
```python
def process_large_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            # Process each line here
            print(line.strip())  # Example: printing each line
```

This approach is memory-efficient and scalable for large datasets.

### 2. **Explain the difference between `deepcopy()` and `copy()` in Python with examples.**

#### Answer:
- **`copy()`** creates a shallow copy, meaning it copies the object but references the original elements inside the object.
- **`deepcopy()`** creates a deep copy, meaning it copies the object as well as all nested objects.

Example:
```python
import copy

original = [[1, 2, 3], [4, 5, 6]]
shallow_copy = copy.copy(original)
deep_copy = copy.deepcopy(original)

shallow_copy[0][0] = 100
deep_copy[0][0] = 200

print(original)       # Output: [[100, 2, 3], [4, 5, 6]]
print(shallow_copy)   # Output: [[100, 2, 3], [4, 5, 6]]
print(deep_copy)      # Output: [[200, 2, 3], [4, 5, 6]]
```
Here, `shallow_copy` modifies the original list’s nested objects, while `deep_copy` works independently.

### 3. **What is the difference between `is` and `==` in Python?**

#### Answer:
- **`==`** checks for **value equality** — whether two objects have the same value.
- **`is`** checks for **identity** — whether two references point to the same object in memory.

Example:
```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # Output: True, because their values are the same.
print(a is b)  # Output: False, because they are different objects in memory.
```

### 4. **How can you improve the performance of your Python code?**

#### Answer:
- **Use built-in functions**: They are implemented in C and optimized for performance.
- **Use list comprehensions**: They are faster than traditional `for` loops for creating lists.
- **Avoid global variables**: Accessing local variables is faster than accessing global ones.
- **Use the `join()` method** for string concatenation instead of `+`.
- **Profile your code** using libraries like `cProfile` to identify bottlenecks.

Example of optimizing string concatenation:
```python
# Less efficient
result = ""
for s in ["Python", "is", "fast"]:
    result += s

# More efficient
result = " ".join(["Python", "is", "fast"])
```

### 5. **How do you handle missing data in a Pandas DataFrame?**

#### Answer:
Handling missing data in a DataFrame can be done using Pandas functions such as:
- **`dropna()`**: Remove rows/columns with missing data.
- **`fillna()`**: Fill missing values with a specific value, forward-fill, or backward-fill.

Example:
```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [None, 2, 3, None]
})

# Drop rows with missing values
df_clean = df.dropna()

# Fill missing values with a default value
df_filled = df.fillna(0)

print(df_clean)
print(df_filled)
```

### 6. **What are `*args` and `**kwargs` in Python? How do you use them?**

#### Answer:
- **`*args`** allows you to pass a variable number of positional arguments to a function.
- **`**kwargs`** allows you to pass a variable number of keyword arguments (dictionaries).

Example:
```python
def example_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

example_function(1, 2, 3, name="John", age=30)
# Output:
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'John', 'age': 30}
```

### 7. **Explain how you would use the `itertools` library for generating combinations and permutations.**

#### Answer:
The `itertools` library in Python provides efficient tools for iterating over data. To generate combinations and permutations, you can use `itertools.combinations()` and `itertools.permutations()`.

Example:
```python
import itertools

items = [1, 2, 3]

# Generate combinations of 2 items
combinations = list(itertools.combinations(items, 2))
print(combinations)  # Output: [(1, 2), (1, 3), (2, 3)]

# Generate permutations of 2 items
permutations = list(itertools.permutations(items, 2))
print(permutations)  # Output: [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

### 8. **How would you handle multithreading and multiprocessing in Python?**

#### Answer:
- **Multithreading** is useful when tasks involve I/O-bound operations. The `threading` library can be used to manage threads.
- **Multiprocessing** is useful for CPU-bound tasks, as it utilizes multiple cores. The `multiprocessing` library can manage multiple processes.

Example using `multiprocessing`:
```python
from multiprocessing import Pool

def square(n):
    return n * n

if __name__ == "__main__":
    with Pool(4) as p:
        result = p.map(square, [1, 2, 3, 4])
    print(result)  # Output: [1, 4, 9, 16]
```

Here are concise explanations and simple examples for **local, shared, and global variables** in Python:

1. **Local Variable**:  
   A variable declared inside a function and accessible only within that function.  
   *Use when you need to limit the scope to a specific function.*  
   ```python
   def my_function():
       x = 10  # Local variable
       print(x)
   my_function()  # Output: 10
   ```

2. **Shared Variable**:  
   A variable shared across multiple functions or threads, typically managed using threading or multiprocessing libraries.  
   *Use when multiple parts of your program need to modify and access the same data concurrently.*  
   ```python
   import threading
   shared_var = 0
   def increment():
       global shared_var
       shared_var += 1

   t1 = threading.Thread(target=increment)
   t2 = threading.Thread(target=increment)
   t1.start()
   t2.start()
   t1.join()
   t2.join()
   print(shared_var)  # Output may vary, could be 1 or 2 due to race condition
   ```

3. **Global Variable**:  
   A variable declared outside of functions and accessible throughout the entire program.  
   *Use when you need a variable to be shared across multiple functions or the entire module.*  
   ```python
   x = 10  # Global variable

   def my_function():
       print(x)

   my_function()  # Output: 10
   ```

In general:
- **Local variables** help contain changes to a small section of code.
- **Shared variables** are useful in multi-threaded or multi-process applications where you need shared state.
- **Global variables** are suitable for configuration or values needed across the entire program but should be used cautiously to avoid unexpected behavior.




Here’s the simplest Python code with logging, error handling, and a recovery mechanism to read, transform, and insert data into an MS SQL Server database:

### Prerequisites:
- Install required libraries:
   ```bash
   pip install pyodbc pandas
   ```

### Python Code:

```python
import logging
import pyodbc
import pandas as pd

# Configure logging
logging.basicConfig(filename='data_pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection string
CONN_STRING = 'DRIVER={SQL Server};SERVER=your_server;DATABASE=your_db;UID=user;PWD=password'

def connect_db():
    """Connect to the MS SQL Server database."""
    try:
        conn = pyodbc.connect(CONN_STRING)
        logging.info('Successfully connected to the database.')
        return conn
    except Exception as e:
        logging.error(f'Error connecting to the database: {e}')
        raise

def read_data(file_path):
    """Read data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f'Data read successfully from {file_path}.')
        return df
    except Exception as e:
        logging.error(f'Error reading the file: {e}')
        raise

def transform_data(df):
    """Transform data (dummy transformation for example)."""
    try:
        # Example transformation: Remove rows with missing values
        transformed_df = df.dropna()
        logging.info('Data transformation successful.')
        return transformed_df
    except Exception as e:
        logging.error(f'Error during data transformation: {e}')
        raise

def insert_data(conn, df):
    """Insert data into SQL Server table."""
    try:
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO your_table (column1, column2) VALUES (?, ?)
            """, row['column1'], row['column2'])
        conn.commit()
        logging.info('Data inserted successfully.')
    except Exception as e:
        conn.rollback()
        logging.error(f'Error inserting data into the database: {e}')
        raise

def main():
    try:
        # Step 1: Connect to the database
        conn = connect_db()

        # Step 2: Read data from a CSV file
        file_path = 'data.csv'
        data = read_data(file_path)

        # Step 3: Transform data
        transformed_data = transform_data(data)

        # Step 4: Insert transformed data into the SQL Server table
        insert_data(conn, transformed_data)

    except Exception as e:
        logging.error(f'Pipeline failed: {e}')
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logging.info('Database connection closed.')

if __name__ == '__main__':
    main()
```

### Key Components:
1. **Logging**:
   - Logs successful operations and errors into a file (`data_pipeline.log`).
   
2. **Error Handling**:
   - Uses `try-except` blocks to catch errors in each function (reading, transforming, and inserting data).

3. **Recovery Mechanism**:
   - In case of an error during data insertion, the transaction is rolled back using `conn.rollback()`.
   - In case of an exception during the pipeline, the `finally` block ensures the database connection is closed.

### Replace:
- **`your_server`**, **`your_db`**, **`user`**, **`password`** with your actual database connection details.
- **`your_table`**, **`column1`, `column2`** with your table and column names.

This code is a simple yet effective data pipeline that reads data from a file, transforms it, and loads it into a SQL Server database while handling errors and logging the process.
