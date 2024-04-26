import streamlit as st
import pandas as pd
from db_conn import create_conn


db = create_conn()
cursor = db.cursor()

# def view_book_copies():
#     """
#     Displays the list of books and their copy counts.
#     """
#     st.header("View Book Copies")
#     # Fetch the titles and copy counts of all books
#     cursor.execute("SELECT b.title, GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id) AS all_copies, COUNT(bc.copy_id) "
#                    "FROM Books b "
#                    "JOIN BookCopies bc ON b.book_id = bc.book_id "
#                    "GROUP BY b.title")
#     books_and_copies = cursor.fetchall()
#
#     # Prepare data for the table
#     table_data = []
#     for book_title, all_copies, total_copies in books_and_copies:
#         # Fetch the names and count of checked out copies for the current book
#         cursor.execute("SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) "
#                        "FROM Borrowings br "
#                        "JOIN BookCopies bc ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id "
#                        "JOIN Books b ON bc.book_id = b.book_id "
#                        "WHERE b.title = %s", (book_title,))
#         result = cursor.fetchone()
#         checked_out_copies, checked_out_count = result[0], result[1]
#
#         # Fetch the names and count of available copies for the current book
#         cursor.execute("SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) "
#                        "FROM BookCopies bc "
#                        "JOIN Books b ON bc.book_id = b.book_id "
#                        "LEFT JOIN Borrowings br ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id "
#                        "WHERE b.title = %s AND br.copy_id IS NULL", (book_title,))
#         result = cursor.fetchone()
#         available_copies, available_count = result[0], result[1]
#
#         table_data.append({
#             "Title": book_title,
#             "All Copies": all_copies,
#             "Total Copies": total_copies,
#             "Checked Out Copies": checked_out_copies,
#             "Checked Out Count": checked_out_count,
#             "Available Copies": available_copies,
#             "Available Count": available_count
#         })
#
#     # Display the data in a table
#     st.table(table_data)

def combined_data_report():
    # Fetch all necessary data from the database
    cursor.execute("""
        SELECT 
            Books.title AS Title,
            Authors.name AS Author,
            Publishers.publisher_name AS Publisher,
            Books.published_date AS 'Release Date',
            Genres.genre_name AS Genre,
            GROUP_CONCAT(DISTINCT BookCopies.copy_id) AS 'All Copies',
            COUNT(DISTINCT BookCopies.copy_id) AS 'Total Copies',
            GROUP_CONCAT(CASE WHEN Borrowings.return_date IS NULL THEN BookCopies.copy_id END) AS 'Checked Out Copies',
            COUNT(CASE WHEN Borrowings.return_date IS NULL THEN BookCopies.copy_id END) AS 'Checked Out Count',
            GROUP_CONCAT(CASE WHEN Borrowings.return_date IS NOT NULL THEN BookCopies.copy_id END) AS 'Available Copies',
            COUNT(CASE WHEN Borrowings.return_date IS NOT NULL THEN BookCopies.copy_id END) AS 'Available Count'
        FROM Books
        INNER JOIN Authors ON Books.author_id = Authors.author_id
        INNER JOIN Genres ON Books.genre_id = Genres.genre_id
        INNER JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
        INNER JOIN BookCopies ON Books.book_id = BookCopies.book_id
        LEFT JOIN Borrowings ON BookCopies.copy_id = Borrowings.copy_id AND BookCopies.book_id = Borrowings.book_id
        GROUP BY Books.book_id
    """)
    data = cursor.fetchall()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=['Title', 'Author', 'Publisher', 'Release Date', 'Genre', 'All Copies', 'Total Copies', 'Checked Out Copies', 'Checked Out Count', 'Available Copies', 'Available Count'])

    # Convert the 'Release Date' column to datetime
    df['Release Date'] = pd.to_datetime(df['Release Date'])

    # Create input widgets for the filters
    author_filter = st.text_input("Author")
    publisher_filter = st.text_input("Publisher")
    title_filter = st.text_input("Title")
    genre_filter = st.selectbox("Genre", options=[""] + df["Genre"].unique().tolist(), index=0)
    release_date_filter = st.date_input("Release Date", value=[df["Release Date"].min(), df["Release Date"].max()])

    # Filter the DataFrame based on the input widgets
    df_filtered = df[df["Author"].str.contains(author_filter, case=False) &
                     df["Publisher"].str.contains(publisher_filter, case=False) &
                     df["Title"].str.contains(title_filter, case=False) &
                     (df["Genre"] == genre_filter if genre_filter else True) &
                     df["Release Date"].between(*pd.to_datetime(release_date_filter))]

    # Display the filtered data in a table
    st.table(df_filtered)

def main():
    st.title("Checkout out Books Data Report")
    combined_data_report()

if __name__ == "__main__":
    main()