import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
# import time
# import threading
import os


def create_conn():
    conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        port=33201,
        user="root",
        password="wgvnGfUsLShmwCiSGkKYzVoKMWCCfsQL",
        database="railway"
    )
    os.write(1, f"Connected to the database with ID: {conn.connection_id}\n".encode())
    return conn


db = create_conn()
cursor = db.cursor()
# Set the transaction isolation level to REPEATABLE READ as it is a
# good balance between performance and consistency
cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ")


# def refresh_conn():
#     global db
#     global cursor
#     while True:
#         # Wait for 30 minutes
#         time.sleep(1800)
#         # Close the existing connection
#         if db is not None:
#             db.close()
#         # Create a new connection
#         db = create_conn()
#         cursor = db.cursor()
#         cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ")
#
#
# threading.Thread(target=refresh_conn, daemon=True).start()


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


def add_author():
    st.title("Add Author")
    name = st.text_input("Author Name", key="add_author_name")
    email = st.text_input("Author Email", key="add_author_email")

    if st.button("Add Author"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            add_author_query = "INSERT INTO Authors (name, email) VALUES (%s, %s)"
            values = (name, email)

            # Execute the SQL statement
            cursor.execute(add_author_query, values)

            # Commit the transaction
            db.commit()

            st.success("Author added successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def edit_delete_author():
    st.title("Edit/Delete Author")

    cursor.execute("SELECT author_id, name FROM Authors")
    authors = cursor.fetchall()
    author_options = {author[0]: author[1] for author in authors}
    author_id = st.selectbox("Author", options=list(author_options.keys()), format_func=lambda x: author_options[x])

    cursor.execute("SELECT name, email FROM Authors WHERE author_id = %s", (author_id,))
    author_details = cursor.fetchone()
    name = st.text_input("Changed Author Name", value=author_details[0], key="edit_author_name")
    email = st.text_input("Changed Author Email", value=author_details[1], key="edit_author_email")

    if st.button("Edit Author"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            edit_author_query = "UPDATE Authors SET name = %s, email = %s WHERE author_id = %s"
            values = (name, email, author_id)

            # Execute the SQL statement
            cursor.execute(edit_author_query, values)

            # Commit the transaction
            db.commit()

            st.success("Author edited successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")

    if st.button("Delete Author"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            delete_author_query = "DELETE FROM Authors WHERE author_id = %s"
            values = (author_id,)

            # Execute the SQL statement
            cursor.execute(delete_author_query, values)

            # Commit the transaction
            db.commit()

            st.success("Author deleted successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def add_genre():
    st.title("Add Genre")
    genre_name = st.text_input("Genre Name", key="add_genre_name")

    if st.button("Add Genre"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            add_genre_query = "INSERT INTO Genres (genre_name) VALUES (%s)"
            values = (genre_name,)

            # Execute the SQL statement
            cursor.execute(add_genre_query, values)

            # Commit the transaction
            db.commit()

            st.success("Genre added successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def edit_delete_genre():
    st.title("Edit/Delete Genre")

    cursor.execute("SELECT genre_id, genre_name FROM Genres")
    genres = cursor.fetchall()
    genre_options = {genre[0]: genre[1] for genre in genres}
    genre_id = st.selectbox("Genre", options=list(genre_options.keys()), format_func=lambda x: genre_options[x])

    cursor.execute("SELECT genre_name FROM Genres WHERE genre_id = %s", (genre_id,))
    genre_details = cursor.fetchone()
    genre_name = st.text_input("Changed Genre Name", value=genre_details[0], key="edit_genre_name")

    if st.button("Edit Genre"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            edit_genre_query = "UPDATE Genres SET genre_name = %s WHERE genre_id = %s"
            values = (genre_name, genre_id)

            # Execute the SQL statement
            cursor.execute(edit_genre_query, values)

            # Commit the transaction
            db.commit()

            st.success("Genre edited successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")

    if st.button("Delete Genre"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            delete_genre_query = "DELETE FROM Genres WHERE genre_id = %s"
            values = (genre_id,)

            # Execute the SQL statement
            cursor.execute(delete_genre_query, values)

            # Commit the transaction
            db.commit()

            st.success("Genre deleted successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def add_publisher():
    st.title("Add Publisher")
    publisher_name = st.text_input("Publisher Name", key="add_publisher_name")

    if st.button("Add Publisher"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            add_publisher_query = "INSERT INTO Publishers (publisher_name) VALUES (%s)"
            values = (publisher_name,)

            # Execute the SQL statement
            cursor.execute(add_publisher_query, values)

            # Commit the transaction
            db.commit()

            st.success("Publisher added successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def edit_delete_publisher():
    st.title("Edit/Delete Publisher")

    cursor.execute("SELECT publisher_id, publisher_name FROM Publishers")
    publishers = cursor.fetchall()
    publisher_options = {publisher[0]: publisher[1] for publisher in publishers}
    publisher_id = st.selectbox("Publisher", options=list(publisher_options.keys()),
                                format_func=lambda x: publisher_options[x])

    cursor.execute("SELECT publisher_name FROM Publishers WHERE publisher_id = %s", (publisher_id,))
    publisher_details = cursor.fetchone()
    publisher_name = st.text_input("Changed Publisher Name", value=publisher_details[0], key="edit_publisher_name")

    if st.button("Edit Publisher"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            edit_publisher_query = "UPDATE Publishers SET publisher_name = %s WHERE publisher_id = %s"
            values = (publisher_name, publisher_id)

            # Execute the SQL statement
            cursor.execute(edit_publisher_query, values)

            # Commit the transaction
            db.commit()

            st.success("Publisher edited successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")

    if st.button("Delete Publisher"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            delete_publisher_query = "DELETE FROM Publishers WHERE publisher_id = %s"
            values = (publisher_id,)

            # Execute the SQL statement
            cursor.execute(delete_publisher_query, values)

            # Commit the transaction
            db.commit()

            st.success("Publisher deleted successfully!")
            st.rerun()
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def view_authors_genres_publishers():
    """
    Displays the list of authors, genres, and publishers.
    """
    st.header("View Authors, Genres, and Publishers")

    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

        # Fetch all authors
        cursor.execute("SELECT author_id, name, email FROM Authors")
        authors = cursor.fetchall()

        # Prepare data for the authors table
        authors_table_data = [{"Author ID": author[0], "Name": author[1], "Email": author[2]} for author in authors]

        # Display the authors table
        st.subheader("Authors")
        st.table(authors_table_data)

        # Fetch all genres
        cursor.execute("SELECT genre_id, genre_name FROM Genres")
        genres = cursor.fetchall()

        # Prepare data for the genres table
        genres_table_data = [{"Genre ID": genre[0], "Name": genre[1]} for genre in genres]

        # Display the genres table
        st.subheader("Genres")
        st.table(genres_table_data)

        # Fetch all publishers
        cursor.execute("SELECT publisher_id, publisher_name FROM Publishers")
        publishers = cursor.fetchall()

        # Prepare data for the publishers table
        publishers_table_data = [{"Publisher ID": publisher[0], "Name": publisher[1]} for publisher in publishers]

        # Display the publishers table
        st.subheader("Publishers")
        st.table(publishers_table_data)

        # Commit the transaction
        db.commit()
    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        db.rollback()
        st.error(f"An error occurred: {err}")


def edit_data():
    st.sidebar.title("Select fields to edit")
    page = st.sidebar.selectbox("Select a page", ["Authors", "Genres", "Publishers",
                                                  "View Authors, Genres, and Publishers"])

    if page == "Authors":
        add_author()
        edit_delete_author()
    elif page == "Genres":
        add_genre()
        edit_delete_genre()
    elif page == "Publishers":
        add_publisher()
        edit_delete_publisher()
    elif page == "View Authors, Genres, and Publishers":
        view_authors_genres_publishers()


def view_books():
    """
    Displays the list of books.
    """
    st.header("View Books")

    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

        # Fetch all books along with their author, genre, and publisher names
        cursor.execute("""
            SELECT Books.book_id, Books.title, Authors.name, Genres.genre_name, Publishers.publisher_name, Books.published_date 
            FROM Books
            INNER JOIN Authors ON Books.author_id = Authors.author_id
            INNER JOIN Genres ON Books.genre_id = Genres.genre_id
            INNER JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
        """)
        books = cursor.fetchall()

        # Commit the transaction
        cursor.execute("COMMIT")

        # Prepare data for the table
        table_data = [{"Book ID": book[0], "Title": book[1], "Author": book[2], "Genre": book[3], "Publisher": book[4],
                       "Published Date": book[5]} for book in books]

        # Display the data in a table
        st.table(table_data)

    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        cursor.execute("ROLLBACK")
        st.error(f"An error occurred: {err}")


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
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            add_book_query = "INSERT INTO Books (title, author_id, genre_id, publisher_id, published_date) VALUES (%s, %s, %s, %s, %s)"
            values = (title, author_id, genre_id, publisher_id, published_date)

            # Execute the SQL statement
            cursor.execute(add_book_query, values)

            # Commit the transaction
            cursor.execute("COMMIT")

            st.success("Book added successfully!")
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            cursor.execute("ROLLBACK")
            st.error(f"An error occurred: {err}")


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
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Prepare the SQL statement
                update_book_query = "UPDATE Books SET title = %s, author_id = %s, genre_id = %s, publisher_id = %s, published_date = %s WHERE book_id = %s"
                values = (title, author_id, genre_id, publisher_id, published_date, selected_book_id)

                # Execute the SQL statement
                cursor.execute(update_book_query, values)

                # Commit the transaction
                cursor.execute("COMMIT")

                st.success("Book updated successfully!")
                st.rerun()
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                cursor.execute("ROLLBACK")
                st.error(f"An error occurred: {err}")

        if st.button("Delete Book"):
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Prepare the SQL statement
                delete_book_query = "DELETE FROM Books WHERE book_id = %s"
                values = (selected_book_id,)

                # Execute the SQL statement
                cursor.execute(delete_book_query, values)

                # Commit the transaction
                cursor.execute("COMMIT")

                st.success("Book deleted successfully!")
                st.rerun()
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                cursor.execute("ROLLBACK")
                st.error(f"An error occurred: {err}")


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
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            add_borrower_query = "INSERT INTO Borrowers (name, phone_number) VALUES (%s, %s)"
            values = (name, phone_number)

            # Execute the SQL statement
            cursor.execute(add_borrower_query, values)

            # Commit the transaction
            db.commit()

            st.success("Borrower added successfully.")
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


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
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Prepare the SQL statement
                edit_borrower_query = "UPDATE Borrowers SET name = %s, phone_number = %s WHERE borrower_id = %s"
                values = (name, phone_number, selected_borrower_id)

                # Execute the SQL statement
                cursor.execute(edit_borrower_query, values)

                # Commit the transaction
                db.commit()

                st.success("Borrower details updated successfully.")
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                db.rollback()
                st.error(f"An error occurred: {err}")

        if st.button("Delete Borrower"):
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Prepare the SQL statement
                delete_borrower_query = "DELETE FROM Borrowers WHERE borrower_id = %s"
                values = (selected_borrower_id,)

                # Execute the SQL statement
                cursor.execute(delete_borrower_query, values)

                # Commit the transaction
                db.commit()

                st.success("Borrower deleted successfully.")
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                db.rollback()
                st.error(f"An error occurred: {err}")


def view_borrowers():
    st.header("View Borrowers")
    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

        # Fetch all borrowers
        cursor.execute("SELECT borrower_id, name, phone_number FROM Borrowers")
        borrowers = cursor.fetchall()

        # Commit the transaction
        db.commit()

        # Prepare data for the table
        table_data = [{"Borrower ID": borrower[0], "Name": borrower[1], "Phone Number": borrower[2]} for borrower in
                      borrowers]

        # Display the data in a table
        st.table(table_data)
    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        db.rollback()
        st.error(f"An error occurred: {err}")


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
    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

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

        # Commit the transaction
        db.commit()

        return book_details, num_copies
    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        db.rollback()
        print(f"An error occurred: {err}")


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
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Get the maximum copy_id for the selected book_id
                cursor.execute("SELECT MAX(copy_id) FROM BookCopies WHERE book_id = %s", (selected_book_id,))
                max_copy_id = cursor.fetchone()[0]
                if max_copy_id is None:
                    max_copy_id = 0

                # Insert the new copies into the BookCopies table
                add_copies_query = "INSERT INTO BookCopies (copy_id, book_id) VALUES (%s, %s)"
                values = [(max_copy_id + i + 1, selected_book_id) for i in range(num_new_copies)]
                cursor.executemany(add_copies_query, values)

                # Commit the transaction
                db.commit()

                st.success(f"Added {num_new_copies} copies to the book.")
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                db.rollback()
                st.error(f"An error occurred: {err}")


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
            try:
                # Start a new transaction
                cursor.execute("START TRANSACTION")

                # Remove the selected copies from the BookCopies table
                remove_copies_query = "DELETE FROM BookCopies WHERE book_id = %s AND copy_id = %s"
                values = [(selected_book_id, copy_id) for copy_id in selected_copies]
                cursor.executemany(remove_copies_query, values)

                # Commit the transaction
                db.commit()

                st.success(f"Removed {len(selected_copies)} copies from the book.")
            except mysql.connector.Error as err:
                # If an error occurred, rollback the transaction
                db.rollback()
                st.error(f"An error occurred: {err}")


def view_book_copies():
    st.header("View Book Copies")

    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

        # Call the stored procedure
        cursor.callproc("ViewBookCopies")

        # Fetch data from the temporary table
        cursor.execute("SELECT * FROM TempViewBookCopies")
        table_data = cursor.fetchall()

        # Commit the transaction
        db.commit()

        # Prepare data for the table
        table_data = [{"Title": row[0], "All Copies": row[1], "Total Copies": row[2], "Checked Out Copies": row[3],
                       "Checked Out Count": row[4], "Available Copies": row[5], "Available Count": row[6]} for row in
                      table_data]

        # Display the data in a table
        st.table(table_data)
    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        db.rollback()
        st.error(f"An error occurred: {err}")


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
    borrower_id = st.selectbox("Borrower", options=list(borrower_options.keys()),
                               format_func=lambda x: borrower_options[x])

    borrow_date = datetime.now().date()
    return_date = borrow_date + timedelta(days=14)

    borrow_date = st.date_input("Borrow Date", value=borrow_date)
    return_date = st.date_input("Return Date", value=return_date)

    if st.button("Create Borrowing"):
        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Prepare the SQL statement
            create_borrowing_query = "INSERT INTO Borrowings (copy_id, book_id, borrower_id, borrow_date, return_date) VALUES (%s, %s, %s, %s, %s)"
            values = (copy_id, book_id, borrower_id, borrow_date, return_date)

            # Execute the SQL statement
            cursor.execute(create_borrowing_query, values)

            # Commit the transaction
            db.commit()

            st.success("Borrowing created successfully!")
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


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

    borrowing_df = pd.DataFrame(borrowing_table,
                                columns=["Borrowing ID", "Copy ID", "Book Title", "Borrower Name", "Borrow Date",
                                         "Return Date"])
    st.table(borrowing_df)

    borrowing_id = st.selectbox("Select a Borrowing ID to resolve", options=[row[0] for row in borrowings])

    if st.button("Resolve Borrowing"):
        borrowing_id = int(borrowing_id)
        cursor.execute("SELECT borrowing_id FROM Borrowings")
        existing_borrowing_ids = [row[0] for row in cursor.fetchall()]

        if borrowing_id not in existing_borrowing_ids:
            st.error("Invalid Borrowing ID.")
            return

        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

            # Query the database to retrieve the selected borrowing
            cursor.execute("SELECT copy_id, book_id, borrower_id FROM Borrowings WHERE borrowing_id = %s",
                           (borrowing_id,))
            selected_borrowing = cursor.fetchone()

            copy_id, book_id, borrower_id = selected_borrowing[0], selected_borrowing[1], selected_borrowing[2]

            # Prepare the SQL statement
            resolve_borrowing_query = "DELETE FROM Borrowings WHERE borrowing_id = %s"
            values = (borrowing_id,)

            # Execute the SQL statement
            cursor.execute(resolve_borrowing_query, values)

            # Commit the transaction
            db.commit()

            st.success("Borrowing resolved successfully!")
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


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

    borrowing_df = pd.DataFrame(borrowing_table,
                                columns=["Borrowing ID", "Copy ID", "Book Title", "Borrower Name", "Return Date"])
    st.table(borrowing_df)

    borrowing_id = st.selectbox("Select a Borrowing ID to extend", options=[row[0] for row in borrowings])

    if st.button("Extend Borrowing"):
        borrowing_id = int(borrowing_id)
        cursor.execute("SELECT borrowing_id FROM Borrowings")
        existing_borrowing_ids = [row[0] for row in cursor.fetchall()]

        if borrowing_id not in existing_borrowing_ids:
            st.error("Invalid Borrowing ID.")
            return

        try:
            # Start a new transaction
            cursor.execute("START TRANSACTION")

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

            # Commit the transaction
            db.commit()

            st.success("Borrowing extended successfully!")
        except mysql.connector.Error as err:
            # If an error occurred, rollback the transaction
            db.rollback()
            st.error(f"An error occurred: {err}")


def main_data_report():
    st.sidebar.title("Select an option")
    page = st.sidebar.selectbox("Page", ["Generate Data Report"])

    if page == "Generate Data Report":
        generate_data_report()


def generate_data_report():
    st.title("Checked Out Books Data Report")

    try:
        # Start a new transaction
        cursor.execute("START TRANSACTION")

        # Call the stored procedure
        cursor.callproc('GenerateDataReport')

        # Fetch data from the temporary table
        cursor.execute("SELECT * FROM TempReport")
        data = cursor.fetchall()

        # Commit the transaction
        db.commit()

    except mysql.connector.Error as err:
        # If an error occurred, rollback the transaction
        db.rollback()
        st.error(f"An error occurred: {err}")
        return  # Exit the function

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

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(table_data)

    # Convert the 'Borrow Date' and 'Return Date' columns to datetime
    df['Borrow Date'] = pd.to_datetime(df['Borrow Date']).dt.date
    df['Return Date'] = pd.to_datetime(df['Return Date']).dt.date

    # Create input widgets for the filters
    author_filter = st.text_input("Author")
    publisher_filter = st.text_input("Publisher")
    title_filter = st.text_input("Book Title")
    genre_filter = st.selectbox("Genre", options=[""] + df["Genre"].unique().tolist(), index=0)
    # borrow_date_filter = st.date_input("Borrow Date", value=[df["Borrow Date"].min(), df["Borrow Date"].max()])
    # return_date_filter = st.date_input("Return Date", value=[df["Return Date"].min(), df["Return Date"].max()])
    borrow_start_date_filter = st.date_input("Borrow Start Date", value=df["Borrow Date"].min())
    borrow_end_date_filter = st.date_input("Borrow End Date", value=df["Borrow Date"].max())

    # Add two date input widgets for the start and end dates of the return period
    return_start_date_filter = st.date_input("Return Start Date", value=df["Return Date"].min())
    return_end_date_filter = st.date_input("Return End Date", value=df["Return Date"].max())

    # Filter the DataFrame based on the input widgets
    df_filtered = df[df["Author"].str.contains(author_filter, case=False) &
                     df["Publisher"].str.contains(publisher_filter, case=False) &
                     df["Book Title"].str.contains(title_filter, case=False) &
                     (df["Genre"] == genre_filter if genre_filter else True) &
                     df["Borrow Date"].between(borrow_start_date_filter, borrow_end_date_filter) &
                     df["Return Date"].between(return_start_date_filter, return_end_date_filter)]
    # df["Borrow Date"].between(*pd.to_datetime(borrow_date_filter)) &
    # df["Return Date"].between(*pd.to_datetime(return_date_filter))]

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
    st.write(
        "The following statistics are based on the filtered data, in case of a tie the first value which appears will be returned:")
    st.markdown(f"* Title of the Book Whose Most Copies are Borrowed: {most_borrowed_book}")
    st.markdown(f"* Average Number of Books Borrowed Per Borrower: {avg_books_per_borrower:.2f}")
    st.markdown(f"* Borrower Who Borrowed Most Books: {most_frequent_borrower}")
    st.markdown(f"* Most Borrowed Genre: {most_borrowed_genre}")
    st.markdown(f"* Most Borrowed Author: {most_borrowed_author}")
    st.markdown(f"* Most Borrowed Publisher: {most_borrowed_publisher}")


def main():
    st.title("Library Management System")

    options = ["Book Data Management", "Book Management", "Borrower Management", "Edit Book Copies", "Borrowings",
               "Data Report"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Book Data Management":
        edit_data()
    elif choice == "Book Management":
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
