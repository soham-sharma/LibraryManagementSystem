# Library Management System

This project is a library management system that allows users to explore the library's collection and manage book borrowings. It uses a MySQL database to store data about books, authors, genres, publishers, book copies, and borrowings.

## Features

- **Data Report:** Users can explore the library's collection through a data report that displays information about book titles, authors, publishers, release dates, genres, and the number of copies available and checked out. The data report can be filtered based on user input.

- **Book Management:** The system allows for the addition of new books to the library's collection.

- **Borrowing Management:** The system also manages book borrowings, keeping track of which copies are checked out and when they are returned.

## Setup

To set up the project, follow these steps:

1. Clone the repository.

    ```bash
    git clone https://github.com/soham-sharma/LibraryManagementSystem.git
    cd LibraryManagementSystem
    ```

2. Install the necessary Python libraries.

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the MySQL database.

    - Install MySQL Server and MySQL Workbench.
    - Create a new schema in MySQL Workbench and run the SQL scripts in the `sql` directory to create the necessary tables.

4. Update the database connection details in `run.py`.

    ```python
    db = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="yourdatabase",
    )
    ```

5. Run the Streamlit app.

    ```bash
    streamlit run run.py
    ```

## Usage

To use the library management system, open the Streamlit app in your web browser. You can explore the library's collection through the data report and manage book borrowings.

## Future Work

In future iterations, I plan to add more advanced visualizations to the library management system to provide users with deeper insights into the library's operations.
