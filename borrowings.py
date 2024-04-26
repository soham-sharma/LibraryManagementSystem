import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
from db_conn import create_conn

db = create_conn()
cursor = db.cursor()

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
        st.rerun()


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

    # borrowing_id = st.number_input("Enter the Borrowing ID to resolve", min_value=1, step=1)
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
        st.rerun()


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

    # borrowing_id = st.number_input("Enter the Borrowing ID to extend", min_value=1, step=1)
    #
    # borrowing_id = int(borrowing_id)
    # cursor.execute("SELECT borrowing_id FROM Borrowings")
    # existing_borrowing_ids = [row[0] for row in cursor.fetchall()]
    #
    # if borrowing_id not in existing_borrowing_ids:
    #     st.error("Invalid Borrowing ID.")
    #     return

    borrowing_id = st.selectbox("Select a Borrowing ID to extend", options=[row[0] for row in borrowings])
    # Query the database to retrieve the selected borrowing
    cursor.execute("SELECT copy_id, book_id, borrower_id, return_date FROM Borrowings WHERE borrowing_id = %s", (borrowing_id,))
    selected_borrowing = cursor.fetchone()

    copy_id, book_id, borrower_id, return_date = selected_borrowing[0], selected_borrowing[1], selected_borrowing[2], selected_borrowing[3]

    new_return_date = st.date_input("Enter the new return date", value=return_date)

    if st.button("Confirm New Date"):
        # Prepare the SQL statement
        extend_borrowing_query = "UPDATE Borrowings SET return_date = %s WHERE borrowing_id = %s"
        values = (new_return_date, borrowing_id)

        # Execute the SQL statement
        cursor.execute(extend_borrowing_query, values)
        db.commit()

        st.success("Borrowing extended successfully!")
        st.rerun()



def main():
    st.sidebar.title("Select an option")
    page = st.sidebar.selectbox("Page", ["Create New Borrowing", "Resolve Borrowing", "Extend Borrowing"])

    if page == "Create New Borrowing":
        create_new_borrowing()
    elif page == "Resolve Borrowing":
        resolve_borrowing()
    elif page == "Extend Borrowing":
        extend_borrowing()


if __name__ == "__main__":
    main()
