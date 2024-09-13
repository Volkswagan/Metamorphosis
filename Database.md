Here are concise one-liner definitions for each term:

1. **Data Warehouse**: A centralized repository for structured data, optimized for reporting and analysis from multiple sources.
   
2. **Data Lake**: A storage system that holds vast amounts of raw, unstructured, and structured data, supporting a variety of analytics.

3. **Data Mart**: A subset of a data warehouse focused on specific business functions or departments.

4. **Fact Table**: A central table in a star schema storing quantitative data for analysis, typically used for transaction records or performance metrics.

5. **Dimension Table**: A table in a star schema that contains descriptive, categorical data (e.g., dates, customer information) to help slice and dice fact table data.

6. **Star Schema**: A database schema where a central fact table connects to multiple dimension tables, used for simple and fast queries.

7. **Snowflake Schema**: A more normalized form of a star schema where dimension tables are further normalized, used when data integrity and storage optimization are important.

8. **Factless Fact Table**: A fact table that records events without any associated measurable facts, typically used for tracking occurrences.

9. **Master Table**: A table that holds core, reference data for the business (e.g., products, employees), often used across different transactional systems.

10. **Transaction Table**: A table that records transactions or events (e.g., orders, sales), typically growing over time as more transactions occur.

11. **SCD Type 1**: A method for managing slowly changing dimensions where old data is overwritten with new data.

12. **SCD Type 2**: A method where historical data is preserved by creating new rows for changes, maintaining a full history of changes.

13. **SCD Type 3**: A method that stores only limited history of changes, usually keeping the current and previous versions of a dimension.

14. **Normalization**: The process of organizing data to reduce redundancy, used to optimize updates, inserts, and consistency.

15. **Denormalization**: The process of combining data from multiple tables into one, used to optimize read performance in analytical queries.

16. **1NF (First Normal Form)**: Ensures that each table cell contains atomic (indivisible) values, eliminating repeating groups.
   
17. **2NF (Second Normal Form)**: Builds on 1NF by ensuring that non-key columns are fully dependent on the primary key.

18. **3NF (Third Normal Form)**: Builds on 2NF by removing transitive dependencies, ensuring non-key columns depend only on the primary key.

19. **BCNF (Boyce-Codd Normal Form)**: A stricter version of 3NF, ensuring that every determinant is a candidate key, used when complex relationships exist.

### When to Use What:

- **Fact Table**: Use when storing transactional or measurable data for analysis (e.g., sales, revenue).
- **Dimension Table**: Use when you need descriptive data (e.g., customer info) to support queries against fact tables.
- **Star Schema**: Use for simpler, faster reporting with less complex queries.
- **Snowflake Schema**: Use when you want to normalize data for better storage efficiency or to handle complex relationships.
- **Normalization**: Use when you want to minimize data redundancy, particularly in transactional databases.
- **Denormalization**: Use when optimizing for read-heavy queries, especially in analytical databases. 
- **1NF/2NF/3NF/BCNF**: Use normalization forms progressively to remove redundancies and optimize relational database structures; BCNF is used in cases of complex relationships and dependencies.

- Here are concise one-liner definitions for each key:

1. **Primary Key**: A unique identifier for each record in a table, ensuring no duplicates and null values.

2. **Foreign Key**: A field in one table that creates a relationship by referencing the primary key of another table.

3. **Candidate Key**: A column or combination of columns that can uniquely identify a record and could potentially become a primary key.

4. **Super Key**: A set of one or more columns that uniquely identifies a record, potentially containing extra, non-minimal columns.

5. **Surrogate Key**: An artificially generated unique identifier (usually a numeric ID) used as the primary key, without any business meaning.

Here’s a brief explanation of different constraints and a trigger in SQL Server, along with simple examples:

### 1. **Constraints**

- **PRIMARY KEY**: Ensures uniqueness and identifies each record in a table.
- **FOREIGN KEY**: Ensures that the value in one table corresponds to the value in another table.
- **UNIQUE**: Ensures all values in a column are distinct.
- **CHECK**: Ensures that values in a column meet a specific condition.
- **DEFAULT**: Assigns a default value to a column if no value is provided.
  
  ```sql
  CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
    LastName VARCHAR(50) UNIQUE
    CHECK (Salary >= 0)
    SalaryDate DATE NOT NULL
    CreatedDate DATE DEFAULT GETDATE()
  
  );
  ```

### 2. **Trigger**

A **trigger** is a stored procedure that is automatically executed when a specified event occurs in a database (e.g., insert, update, or delete).

Example: A trigger that prevents deletion from the `Employees` table if the employee's `DepartmentID` is NULL.

```sql
CREATE TRIGGER PreventDeleteWithoutDepartment
ON Employees
FOR DELETE
AS
BEGIN
  IF EXISTS (SELECT * FROM deleted WHERE DepartmentID IS NULL)
  BEGIN
    RAISERROR ('Cannot delete employees without a department!', 16, 1);
    ROLLBACK TRANSACTION;
  END
END;
```
