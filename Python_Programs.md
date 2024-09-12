```python
words = "aabbbcccc"
count = {}

for word in words:
    count[word] = count.get(word, 0) + 1

output = ""
for k,v in count.items():
	output = output + f"{k}{v}"
print(output)
```
```python
text = "my name is ram, ram name is good"
words = text.replace(",", "").split()  # Remove commas and split into words
count = {}

for word in words:
    count[word] = count.get(word, 0) + 1

output = ""
for k,v in count.items():
	output = output + f"{k}{v}" + "\n"
print(output)
```
```python
import logging
import pyodbc
import pandas as pd

# Configure logging
logging.basicConfig(filename='data_pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection string
CONN_STRING = 'DRIVER={SQL Server};SERVER=your_server;DATABASE=your_db;UID=user;PWD=password'

def data_pipeline(file_path):
    conn = None
    try:
        # Step 1: Connect to the database
        conn = pyodbc.connect(CONN_STRING)
        logging.info('Successfully connected to the database.')

        # Step 2: Read data from a CSV file
        df = pd.read_csv(file_path)
        logging.info(f'Data read successfully from {file_path}.')

        # Step 3: Transform data (e.g., drop rows with missing values)
        transformed_df = df.dropna()
        logging.info('Data transformation successful.')

        # Step 4: Insert transformed data into the SQL Server table
        cursor = conn.cursor()
        for index, row in transformed_df.iterrows():
            cursor.execute("""
                INSERT INTO your_table (column1, column2) VALUES (?, ?)
            """, row['column1'], row['column2'])
        conn.commit()
        logging.info('Data inserted successfully.')

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f'Pipeline failed: {e}')
        raise  # Raise the error after logging

    finally:
        if conn:
            conn.close()
            logging.info('Database connection closed.')

# Running the pipeline
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python pipeline.py <input_file>")
    	else:
        	input_file = sys.argv[1]
        	count_words_in_file(input_file)
    		data_pipeline(input_file,)

```
