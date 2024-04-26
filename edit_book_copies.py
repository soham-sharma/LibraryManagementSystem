import streamlit as st
from db_conn import create_conn


db = create_conn()
cursor = db.cursor()


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
    """
    Displays the form to add book copies.
    """
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
            st.rerun()


def remove_book_copies():
    """
    Displays the form to remove book copies.
    """
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
            st.rerun()

    st.write("Note: Copies that are currently checked out cannot be removed.")

def view_book_copies():
    """
    Displays the list of books and their copy counts.
    """
    st.header("View Book Copies")

    # Fetch the titles and copy counts of all books
    cursor.execute("SELECT b.title, GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id) AS all_copies, COUNT(bc.copy_id) "
                   "FROM Books b "
                   "JOIN BookCopies bc ON b.book_id = bc.book_id "
                   "GROUP BY b.title")
    books_and_copies = cursor.fetchall()

    # Prepare data for the table
    table_data = []
    for book_title, all_copies, total_copies in books_and_copies:
        # Fetch the names and count of checked out copies for the current book
        cursor.execute("SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) "
                       "FROM Borrowings br "
                       "JOIN BookCopies bc ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id "
                       "JOIN Books b ON bc.book_id = b.book_id "
                       "WHERE b.title = %s", (book_title,))
        result = cursor.fetchone()
        checked_out_copies, checked_out_count = result[0], result[1]

        # Fetch the names and count of available copies for the current book
        cursor.execute("SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) "
                       "FROM BookCopies bc "
                       "JOIN Books b ON bc.book_id = b.book_id "
                       "LEFT JOIN Borrowings br ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id "
                       "WHERE b.title = %s AND br.copy_id IS NULL", (book_title,))
        result = cursor.fetchone()
        available_copies, available_count = result[0], result[1]

        table_data.append({
            "Title": book_title,
            "All Copies": all_copies,
            "Total Copies": total_copies,
            "Checked Out Copies": checked_out_copies,
            "Checked Out Count": checked_out_count,
            "Available Copies": available_copies,
            "Available Count": available_count
        })

    # Display the data in a table
    st.table(table_data)





def main():
    st.sidebar.title("Edit Book Copies")
    option = st.sidebar.selectbox("Select an option", ["Add Book Copies", "Remove Book Copies", "View Book Copies"])

    if option == "Add Book Copies":
        add_book_copies()
    elif option == "Remove Book Copies":
        remove_book_copies()
    elif option == "View Book Copies":
        view_book_copies()


if __name__ == "__main__":
    main()
