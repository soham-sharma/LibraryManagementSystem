import streamlit as st
from db_conn import create_conn


db = create_conn()
cursor = db.cursor()


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
        # selected_book = books.index((selected_book_id, book_options[selected_book_id]))

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


def main():
    st.title("Book Management")

    options = ["Add Book", "Edit/Delete Book", "View Books"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Add Book":
        add_book()
    elif choice == "Edit/Delete Book":
        edit_delete_book()
    elif choice == "View Books":
        view_books()


if __name__ == "__main__":
    main()
