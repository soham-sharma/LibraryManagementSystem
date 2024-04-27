import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import mysql.connector


def create_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="library",
    )
    return conn

# def create_conn():
#     conn = mysql.connector.connect(
#         host=st.secrets["database"]["host"],
#         user=st.secrets["database"]["user"],
#         password=st.secrets["database"]["password"],
#         database=st.secrets["database"]["database"],
#     )
#     return conn

db = create_conn()
cursor = db.cursor()

def edit_lib_data():
    st.sidebar.title("Select fields to edit")
    page = st.sidebar.selectbox("Select a page", ["Books", "Book Copies", "Borrowers", "Borrowings"])

    if page == "Books":
        main_books()
    elif page == "Borrowers":
        main_borrowers()
    elif page == "Book Copies":
        main_book_copies()
    elif page == "Borrowings":
        main_borrowings()

def main_books():
    st.title("Book Management")

    options = ["Add Book", "Edit/Delete Book", "View Books"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Add Book":
        add_book()
    elif choice == "Edit/Delete Book":
        edit_delete_book()
    elif choice == "View Books":
        view_books()

def view_books():
    """
    Displays the list of books.
    """
    st.header("View Books")

    # Fetch all books along with their author, genre, and publisher names
    cursor.execute("""
        SELECT Books.book_id, Books.title, Authors.name, Genres.genre_name, Publishers.publisher_name, Books.published_date 
        FROM Books
        INNER JOIN Authors ON Books.author_id = Authors.author_id
        INNER JOIN Genres ON Books.genre_id = Genres.genre_id
        INNER JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
    """)
    books = cursor.fetchall()

    # Prepare data for the table
    table_data = [{"Book ID": book[0], "Title": book[1], "Author": book[2], "Genre": book[3], "Publisher": book[4], "Published Date": book[5]} for book in books]

    # Display the data in a table
    st.table(table_data)

def add_book():
    # Add a book
    st.header("Add a Book")
    title = st.text_input("Title", key="add_book_title")

    # Fetch existing authors from the Authors table
    cursor.execute("SELECT author_id, name FROM Authors")
    authors = cursor.fetchall()
    author_options = {author[0]: author[1] for author in authors}
    author_id = st.selectbox("Author", options=list(author_options.keys()), format_func=lambda x: author_options[x]
                             , key="add_book_author")

    # Fetch existing genres from the Genres table
    cursor.execute("SELECT genre_id, genre_name FROM Genres")
    genres = cursor.fetchall()
    genre_options = {genre[0]: genre[1] for genre in genres}
    genre_id = st.selectbox("Genre", options=list(genre_options.keys()), format_func=lambda x: genre_options[x]
                            , key="add_book_genre")

    # Fetch existing publishers from the Publishers table
    cursor.execute("SELECT publisher_id, publisher_name FROM Publishers")
    publishers = cursor.fetchall()
    publisher_options = {publisher[0]: publisher[1] for publisher in publishers}
    publisher_id = st.selectbox("Publisher", options=list(publisher_options.keys()),
                                format_func=lambda x: publisher_options[x], key="add_book_publisher")

    published_date = st.date_input("Published Date", key="add_book_published_date")

    if st.button("Add Book"):
        # Prepare the SQL statement
        add_book_query = "INSERT INTO Books (title, author_id, genre_id, publisher_id, published_date) VALUES (%s, %s, %s, %s, %s)"
        values = (title, author_id, genre_id, publisher_id, published_date)

        # Execute the SQL statement
        cursor.execute(add_book_query, values)
        db.commit()

        st.success("Book added successfully!")

def edit_delete_book():
    # Edit and delete books
    st.header("Edit/Delete Books")

    # Fetch existing authors from the Authors table
    cursor.execute("SELECT author_id, name FROM Authors")
    authors = cursor.fetchall()
    author_options = {author[0]: author[1] for author in authors}
    # Fetch existing genres from the Genres table
    cursor.execute("SELECT genre_id, genre_name FROM Genres")
    genres = cursor.fetchall()
    genre_options = {genre[0]: genre[1] for genre in genres}
    # Fetch existing publishers from the Publishers table
    cursor.execute("SELECT publisher_id, publisher_name FROM Publishers")
    publishers = cursor.fetchall()
    publisher_options = {publisher[0]: publisher[1] for publisher in publishers}

    # Fetch existing books from the Books table
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    book_options = {book[0]: book[1] for book in books}
    selected_book_id = st.selectbox("Select a book to edit/delete", options=list(book_options.keys()),
                                    format_func=lambda x: book_options[x])

    if selected_book_id:
        # Fetch the book details based on the selected book
        cursor.execute("SELECT title, author_id, genre_id, publisher_id, published_date FROM Books WHERE book_id = %s",
                       (selected_book_id,))
        book_details = cursor.fetchone()
        title = st.text_input("Title", value=book_details[0], key="edit_book_title")
        author_id = st.selectbox("Author", options=list(author_options.keys()), format_func=lambda x: author_options[x],
                                 index=list(author_options.keys()).index(book_details[1]), key="edit_book_author")
        genre_id = st.selectbox("Genre", options=list(genre_options.keys()), format_func=lambda x: genre_options[x],
                                index=list(genre_options.keys()).index(book_details[2]), key="edit_book_genre")
        publisher_id = st.selectbox("Publisher", options=list(publisher_options.keys()),
                                    format_func=lambda x: publisher_options[x],
                                    index=list(publisher_options.keys()).index(book_details[3]),
                                    key="edit_book_publisher")
        published_date = st.date_input("Published Date", value=book_details[4], key="edit_book_published_date")

        if st.button("Save Changes"):
            # Prepare the SQL statement
            update_book_query = "UPDATE Books SET title = %s, author_id = %s, genre_id = %s, publisher_id = %s, published_date = %s WHERE book_id = %s"
            values = (title, author_id, genre_id, publisher_id, published_date, selected_book_id)

            # Execute the SQL statement
            cursor.execute(update_book_query, values)
            db.commit()

            st.success("Book updated successfully!")
            st.rerun()

        if st.button("Delete Book"):
            # Prepare the SQL statement
            delete_book_query = "DELETE FROM Books WHERE book_id = %s"
            values = (selected_book_id,)

            # Execute the SQL statement
            cursor.execute(delete_book_query, values)
            db.commit()

            st.success("Book deleted successfully!")
            st.rerun()

def main_borrowers():
    st.title("Borrower Management")

    options = ["Add Borrower", "Edit/Delete Borrower", "View Borrowers"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Add Borrower":
        add_borrower()
    elif choice == "Edit/Delete Borrower":
        edit_delete_borrower()
    elif choice == "View Borrowers":
        view_borrowers()

def add_borrower():
    st.header("Add a Borrower")
    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number")

    if st.button("Add Borrower"):
        # Prepare the SQL statement
        add_borrower_query = "INSERT INTO Borrowers (name, phone_number) VALUES (%s, %s)"
        values = (name, phone_number)

        # Execute the SQL statement
        cursor.execute(add_borrower_query, values)
        db.commit()

        st.success("Borrower added successfully.")

def edit_delete_borrower():
    st.header("Edit/Delete a Borrower")
    cursor.execute("SELECT borrower_id, name FROM Borrowers")
    borrowers = cursor.fetchall()
    borrower_options = {borrower[0]: borrower[1] for borrower in borrowers}
    selected_borrower_id = st.selectbox("Select a borrower to edit/delete", options=list(borrower_options.keys()),
                                        format_func=lambda x: borrower_options[x])

    if selected_borrower_id:
        cursor.execute("SELECT name, phone_number FROM Borrowers WHERE borrower_id = %s", (selected_borrower_id,))
        borrower_details = cursor.fetchone()
        name = st.text_input("Name", value=borrower_details[0])
        phone_number = st.text_input("Phone Number", value=borrower_details[1])

        if st.button("Save Changes"):
            # Prepare the SQL statement
            edit_borrower_query = "UPDATE Borrowers SET name = %s, phone_number = %s WHERE borrower_id = %s"
            values = (name, phone_number, selected_borrower_id)

            # Execute the SQL statement
            cursor.execute(edit_borrower_query, values)
            db.commit()

            st.success("Borrower details updated successfully.")

        if st.button("Delete Borrower"):
            # Prepare the SQL statement
            delete_borrower_query = "DELETE FROM Borrowers WHERE borrower_id = %s"
            values = (selected_borrower_id,)

            # Execute the SQL statement
            cursor.execute(delete_borrower_query, values)
            db.commit()

            st.success("Borrower deleted successfully.")

def view_borrowers():
    st.header("View Borrowers")

    # Fetch all borrowers
    cursor.execute("SELECT borrower_id, name, phone_number FROM Borrowers")
    borrowers = cursor.fetchall()

    # Prepare data for the table
    table_data = [{"Borrower ID": borrower[0], "Name": borrower[1], "Phone Number": borrower[2]} for borrower in borrowers]

    # Display the data in a table
    st.table(table_data)

def main_book_copies():
    st.sidebar.title("Edit Book Copies")
    option = st.sidebar.selectbox("Select an option", ["Add Book Copies", "Remove Book Copies", "View Book Copies"])

    if option == "Add Book Copies":
        add_book_copies()
    elif option == "Remove Book Copies":
        remove_book_copies()
    elif option == "View Book Copies":
        view_book_copies()

def get_book_details(book_id):
    """
    Fetches the book details and number of copies for a given book_id.
    """
    cursor.execute("SELECT b.title, a.name, g.genre_name, p.publisher_name, b.published_date "
                   "FROM Books b "
                   "JOIN Authors a ON b.author_id = a.author_id "
                   "JOIN Genres g ON b.genre_id = g.genre_id "
                   "JOIN Publishers p ON b.publisher_id = p.publisher_id "
                   "WHERE b.book_id = %s",
                   (book_id,))
    book_details = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM BookCopies WHERE book_id = %s", (book_id,))
    num_copies = cursor.fetchone()[0]

    return book_details, num_copies

def add_book_copies():
    st.header("Add Book Copies")

    # Fetch existing books from the Books table
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    book_options = {book[0]: book[1] for book in books}
    selected_book_id = st.selectbox("Select a book", options=list(book_options.keys()),
                                    format_func=lambda x: book_options[x])

    if selected_book_id:
        book_details, num_copies = get_book_details(selected_book_id)

        st.subheader("Book Details")
        st.write("Title:", book_details[0])
        st.write("Author:", book_details[1])
        st.write("Genre:", book_details[2])
        st.write("Publisher:", book_details[3])
        st.write("Published Date:", book_details[4])
        st.write("Number of Copies:", num_copies)

        num_new_copies = st.number_input("Number of Copies to Add", min_value=1, value=1)

        if st.button("Add Copies"):
            # Get the maximum copy_id for the selected book_id
            cursor.execute("SELECT MAX(copy_id) FROM BookCopies WHERE book_id = %s", (selected_book_id,))
            max_copy_id = cursor.fetchone()[0]
            if max_copy_id is None:
                max_copy_id = 0

            # Insert the new copies into the BookCopies table
            add_copies_query = "INSERT INTO BookCopies (copy_id, book_id) VALUES (%s, %s)"
            values = [(max_copy_id + i + 1, selected_book_id) for i in range(num_new_copies)]
            cursor.executemany(add_copies_query, values)
            db.commit()

            st.success(f"Added {num_new_copies} copies to the book.")

def remove_book_copies():
    st.header("Remove Book Copies")

    # Fetch existing books from the Books table
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    book_options = {book[0]: book[1] for book in books}
    selected_book_id = st.selectbox("Select a book", options=list(book_options.keys()),
                                    format_func=lambda x: book_options[x])

    if selected_book_id:
        book_details, num_copies = get_book_details(selected_book_id)

        st.subheader("Book Details")
        st.write("Title:", book_details[0])
        st.write("Author:", book_details[1])
        st.write("Genre:", book_details[2])
        st.write("Publisher:", book_details[3])
        st.write("Published Date:", book_details[4])
        st.write("Number of Copies:", num_copies)

        # Fetch copies that are currently checked out
        cursor.execute("SELECT bc.copy_id, bc.book_id "
                       "FROM BookCopies bc "
                       "JOIN Borrowings b ON bc.copy_id = b.copy_id AND bc.book_id = b.book_id ")
        checked_out_copies = {(copy[0], copy[1]) for copy in cursor.fetchall()}

        # Fetch all copies for the selected book
        cursor.execute("SELECT copy_id FROM BookCopies WHERE book_id = %s", (selected_book_id,))
        all_copies = [(copy[0], selected_book_id) for copy in cursor.fetchall()]

        # Exclude the checked out copies
        available_copies = [copy[0] for copy in all_copies if copy not in checked_out_copies]

        selected_copies = st.multiselect("Select Copies to Remove", options=available_copies,
                                         format_func=lambda x: f"Copy {x}")

        if st.button("Remove Copies"):
            # Remove the selected copies from the BookCopies table
            remove_copies_query = "DELETE FROM BookCopies WHERE book_id = %s AND copy_id = %s"
            values = [(selected_book_id, copy_id) for copy_id in selected_copies]
            cursor.executemany(remove_copies_query, values)
            db.commit()

            st.success(f"Removed {len(selected_copies)} copies from the book.")

def view_book_copies():
    st.header("View Book Copies")

    # Call the stored procedure
    cursor.callproc("ViewBookCopies")

    # Fetch data from the temporary table
    cursor.execute("SELECT * FROM TempViewBookCopies")
    table_data = cursor.fetchall()

    # Prepare data for the table
    table_data = [{"Title": row[0], "All Copies": row[1], "Total Copies": row[2], "Checked Out Copies": row[3], "Checked Out Count": row[4], "Available Copies": row[5], "Available Count": row[6]} for row in table_data]

    # Display the data in a table
    st.table(table_data)


def main_borrowings():
    st.sidebar.title("Select an option")
    page = st.sidebar.selectbox("Page", ["Create New Borrowing", "Resolve Borrowing", "Extend Borrowing"])

    if page == "Create New Borrowing":
        create_new_borrowing()
    elif page == "Resolve Borrowing":
        resolve_borrowing()
    elif page == "Extend Borrowing":
        extend_borrowing()

def get_book_title(book_id):
    cursor.execute("SELECT title FROM Books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return "N/A"

def get_borrower_name(borrower_id):
    cursor.execute("SELECT name FROM Borrowers WHERE borrower_id = %s", (borrower_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return "N/A"

def create_new_borrowing():
    st.title("Create New Borrowing")
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    book_options = {book[0]: book[1] for book in books}
    book_id = st.selectbox("Book", options=list(book_options.keys()), format_func=lambda x: book_options[x])

    # Fetch copies that are currently checked out
    cursor.execute("SELECT copy_id, book_id FROM Borrowings")
    checked_out_copies = {(copy[0], copy[1]) for copy in cursor.fetchall()}

    # Fetch all copies for the selected book
    cursor.execute("SELECT copy_id FROM BookCopies WHERE book_id = %s", (book_id,))
    all_copies = [(copy[0], book_id) for copy in cursor.fetchall()]

    # Exclude the checked out copies
    available_copies = [copy[0] for copy in all_copies if copy not in checked_out_copies]

    copy_id = st.selectbox("Book Copy", options=available_copies)

    cursor.execute("SELECT borrower_id, name FROM Borrowers")
    borrowers = cursor.fetchall()
    borrower_options = {borrower[0]: borrower[1] for borrower in borrowers}
    borrower_id = st.selectbox("Borrower", options=list(borrower_options.keys()), format_func=lambda x: borrower_options[x])

    borrow_date = datetime.now().date()
    return_date = borrow_date + timedelta(days=14)

    borrow_date = st.date_input("Borrow Date", value=borrow_date)
    return_date = st.date_input("Return Date", value=return_date)

    if st.button("Create Borrowing"):
        # Prepare the SQL statement
        create_borrowing_query = "INSERT INTO Borrowings (copy_id, book_id, borrower_id, borrow_date, return_date) VALUES (%s, %s, %s, %s, %s)"
        values = (copy_id, book_id, borrower_id, borrow_date, return_date)

        # Execute the SQL statement
        cursor.execute(create_borrowing_query, values)
        db.commit()

        st.success("Borrowing created successfully!")

def resolve_borrowing():
    st.title("Resolve Borrowing")
    cursor.execute("SELECT borrowing_id, copy_id, book_id, borrower_id, borrow_date, return_date FROM Borrowings")
    borrowings = cursor.fetchall()

    if len(borrowings) == 0:
        st.warning("No borrowings found.")
        return

    borrowing_table = []
    for borrowing in borrowings:
        borrowing_id, copy_id, book_id, borrower_id, borrow_date, return_date = borrowing
        book_title = get_book_title(book_id)
        borrower_name = get_borrower_name(borrower_id)
        borrowing_table.append((borrowing_id, copy_id, book_title, borrower_name, borrow_date, return_date))

    borrowing_df = pd.DataFrame(borrowing_table, columns=["Borrowing ID", "Copy ID", "Book Title", "Borrower Name", "Borrow Date", "Return Date"])
    st.table(borrowing_df)

    borrowing_id = st.selectbox("Select a Borrowing ID to resolve", options=[row[0] for row in borrowings])

    if st.button("Resolve Borrowing"):
        borrowing_id = int(borrowing_id)
        cursor.execute("SELECT borrowing_id FROM Borrowings")
        existing_borrowing_ids = [row[0] for row in cursor.fetchall()]

        if borrowing_id not in existing_borrowing_ids:
            st.error("Invalid Borrowing ID.")
            return

        # Query the database to retrieve the selected borrowing
        cursor.execute("SELECT copy_id, book_id, borrower_id FROM Borrowings WHERE borrowing_id = %s", (borrowing_id,))
        selected_borrowing = cursor.fetchone()

        copy_id, book_id, borrower_id = selected_borrowing[0], selected_borrowing[1], selected_borrowing[2]

        # Prepare the SQL statement
        resolve_borrowing_query = "DELETE FROM Borrowings WHERE borrowing_id = %s"
        values = (borrowing_id,)

        # Execute the SQL statement
        cursor.execute(resolve_borrowing_query, values)
        db.commit()

        st.success("Borrowing resolved successfully!")

def extend_borrowing():
    st.title("Extend Borrowing")
    cursor.execute("SELECT borrowing_id, copy_id, book_id, borrower_id, return_date FROM Borrowings")
    borrowings = cursor.fetchall()

    if len(borrowings) == 0:
        st.warning("No borrowings found.")
        return

    borrowing_table = []
    for borrowing in borrowings:
        borrowing_id, copy_id, book_id, borrower_id, return_date = borrowing
        book_title = get_book_title(book_id)
        borrower_name = get_borrower_name(borrower_id)
        borrowing_table.append((borrowing_id, copy_id, book_title, borrower_name, return_date))

    borrowing_df = pd.DataFrame(borrowing_table, columns=["Borrowing ID", "Copy ID", "Book Title", "Borrower Name", "Return Date"])
    st.table(borrowing_df)

    borrowing_id = st.selectbox("Select a Borrowing ID to extend", options=[row[0] for row in borrowings])

    if st.button("Extend Borrowing"):
        borrowing_id = int(borrowing_id)
        cursor.execute("SELECT borrowing_id FROM Borrowings")
        existing_borrowing_ids = [row[0] for row in cursor.fetchall()]

        if borrowing_id not in existing_borrowing_ids:
            st.error("Invalid Borrowing ID.")
            return

        # Query the database to retrieve the selected borrowing
        cursor.execute("SELECT return_date FROM Borrowings WHERE borrowing_id = %s", (borrowing_id,))
        selected_borrowing = cursor.fetchone()

        return_date = selected_borrowing[0]

        # Calculate the new return date by adding 14 days to the current return date
        new_return_date = return_date + timedelta(days=14)

        # Prepare the SQL statement
        extend_borrowing_query = "UPDATE Borrowings SET return_date = %s WHERE borrowing_id = %s"
        values = (new_return_date, borrowing_id)

        # Execute the SQL statement
        cursor.execute(extend_borrowing_query, values)
        db.commit()

        st.success("Borrowing extended successfully!")

def main_data_report():
    st.sidebar.title("Select an option")
    page = st.sidebar.selectbox("Page", ["Generate Data Report"])

    if page == "Generate Data Report":
        generate_data_report()

def generate_data_report():
    st.title("Checked Out Books Data Report")

    # Call the stored procedure
    cursor.callproc('GenerateDataReport')

    # Fetch data from the temporary table
    cursor.execute("SELECT * FROM TempReport")
    data = cursor.fetchall()

    # Prepare data for the table
    table_data = []
    for row in data:
        book_title, author, genre, publisher, copy_id, borrow_date, return_date, borrower = row
        table_data.append({
            "Book Title": book_title,
            "Author": author,
            "Genre": genre,
            "Publisher": publisher,
            "Copy ID": copy_id,
            "Borrow Date": borrow_date,
            "Return Date": return_date,
            "Borrower": borrower
        })

    # # Display the data in a table
    # st.table(table_data)
    # Create a DataFrame from the fetched data
    df = pd.DataFrame(table_data)

    # Convert the 'Borrow Date' and 'Return Date' columns to datetime
    df['Borrow Date'] = pd.to_datetime(df['Borrow Date'])
    df['Return Date'] = pd.to_datetime(df['Return Date'])

    # Create input widgets for the filters
    author_filter = st.text_input("Author")
    publisher_filter = st.text_input("Publisher")
    title_filter = st.text_input("Book Title")
    genre_filter = st.selectbox("Genre", options=[""] + df["Genre"].unique().tolist(), index=0)
    borrow_date_filter = st.date_input("Borrow Date", value=[df["Borrow Date"].min(), df["Borrow Date"].max()])
    return_date_filter = st.date_input("Return Date", value=[df["Return Date"].min(), df["Return Date"].max()])

    # Filter the DataFrame based on the input widgets
    df_filtered = df[df["Author"].str.contains(author_filter, case=False) &
                     df["Publisher"].str.contains(publisher_filter, case=False) &
                     df["Book Title"].str.contains(title_filter, case=False) &
                     (df["Genre"] == genre_filter if genre_filter else True) &
                     df["Borrow Date"].between(*pd.to_datetime(borrow_date_filter)) &
                     df["Return Date"].between(*pd.to_datetime(return_date_filter))]

    # Display the filtered data in a table
    st.table(df_filtered)

    # Calculate statistics
    most_borrowed_book = df_filtered['Book Title'].value_counts().idxmax()
    avg_books_per_borrower = df_filtered['Borrower'].value_counts().mean()
    most_frequent_borrower = df_filtered['Borrower'].value_counts().idxmax()
    most_borrowed_genre = df_filtered['Genre'].value_counts().idxmax()
    most_borrowed_author = df_filtered['Author'].value_counts().idxmax()
    most_borrowed_publisher = df_filtered['Publisher'].value_counts().idxmax()

    # Display statistics
    st.subheader("Statistics")
    st.write("The following statistics are based on the filtered data, in case of a tie the first value which appears will be returned:")
    st.markdown(f"* Title of the Book Whose Most Copies are Borrowed: {most_borrowed_book}")
    st.markdown(f"* Average Number of Books Borrowed Per Borrower: {avg_books_per_borrower:.2f}")
    st.markdown(f"* Borrower Who Borrowed Most Books: {most_frequent_borrower}")
    st.markdown(f"* Most Borrowed Genre: {most_borrowed_genre}")
    st.markdown(f"* Most Borrowed Author: {most_borrowed_author}")
    st.markdown(f"* Most Borrowed Publisher: {most_borrowed_publisher}")

def main():
    st.title("Library Management System")

    options = ["Book Management", "Borrower Management", "Edit Book Copies", "Borrowings", "Data Report"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Book Management":
        main_books()
    elif choice == "Borrower Management":
        main_borrowers()
    elif choice == "Edit Book Copies":
        main_book_copies()
    elif choice == "Borrowings":
        main_borrowings()
    elif choice == "Data Report":
        main_data_report()

if __name__ == "__main__":
    main()
