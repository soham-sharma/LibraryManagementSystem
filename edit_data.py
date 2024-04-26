import streamlit as st
from db_conn import create_conn


db = create_conn()
cursor = db.cursor()


def add_author():
    st.title("Add Author")
    name = st.text_input("Author Name", key="add_author_name")
    email = st.text_input("Author Email", key="add_author_email")

    if st.button("Add Author"):
        # Prepare the SQL statement
        add_author_query = "INSERT INTO Authors (name, email) VALUES (%s, %s)"
        values = (name, email)

        # Execute the SQL statement
        cursor.execute(add_author_query, values)
        db.commit()

        st.success("Author added successfully!")
        st.rerun()


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
        # Prepare the SQL statement
        edit_author_query = "UPDATE Authors SET name = %s, email = %s WHERE author_id = %s"
        values = (name, email, author_id)

        # Execute the SQL statement
        cursor.execute(edit_author_query, values)
        db.commit()

        st.success("Author edited successfully!")
        st.rerun()

    if st.button("Delete Author"):
        # Prepare the SQL statement
        delete_author_query = "DELETE FROM Authors WHERE author_id = %s"
        values = (author_id,)

        # Execute the SQL statement
        cursor.execute(delete_author_query, values)
        db.commit()

        st.success("Author deleted successfully!")
        st.rerun()


def add_genre():
    st.title("Add Genre")
    genre_name = st.text_input("Genre Name", key="add_genre_name")

    if st.button("Add Genre"):
        # Prepare the SQL statement
        add_genre_query = "INSERT INTO Genres (genre_name) VALUES (%s)"
        values = (genre_name,)

        # Execute the SQL statement
        cursor.execute(add_genre_query, values)
        db.commit()

        st.success("Genre added successfully!")
        st.rerun()


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
        # Prepare the SQL statement
        edit_genre_query = "UPDATE Genres SET genre_name = %s WHERE genre_id = %s"
        values = (genre_name, genre_id)

        # Execute the SQL statement
        cursor.execute(edit_genre_query, values)
        db.commit()

        st.success("Genre edited successfully!")
        st.rerun()

    if st.button("Delete Genre"):
        # Prepare the SQL statement
        delete_genre_query = "DELETE FROM Genres WHERE genre_id = %s"
        values = (genre_id,)

        # Execute the SQL statement
        cursor.execute(delete_genre_query, values)
        db.commit()

        st.success("Genre deleted successfully!")
        st.rerun()


def add_publisher():
    st.title("Add Publisher")
    publisher_name = st.text_input("Publisher Name", key="add_publisher_name")

    if st.button("Add Publisher"):
        # Prepare the SQL statement
        add_publisher_query = "INSERT INTO Publishers (publisher_name) VALUES (%s)"
        values = (publisher_name,)

        # Execute the SQL statement
        cursor.execute(add_publisher_query, values)
        db.commit()

        st.success("Publisher added successfully!")
        st.rerun()


def edit_delete_publisher():
    st.title("Edit/Delete Publisher")
    cursor.execute("SELECT publisher_id, publisher_name FROM Publishers")
    publishers = cursor.fetchall()
    publisher_options = {publisher[0]: publisher[1] for publisher in publishers}
    publisher_id = st.selectbox("Publisher", options=list(publisher_options.keys()), format_func=lambda x: publisher_options[x])

    cursor.execute("SELECT publisher_name FROM Publishers WHERE publisher_id = %s", (publisher_id,))
    publisher_details = cursor.fetchone()
    publisher_name = st.text_input("Changed Publisher Name", value=publisher_details[0], key="edit_publisher_name")

    if st.button("Edit Publisher"):
        # Prepare the SQL statement
        edit_publisher_query = "UPDATE Publishers SET publisher_name = %s WHERE publisher_id = %s"
        values = (publisher_name, publisher_id)

        # Execute the SQL statement
        cursor.execute(edit_publisher_query, values)
        db.commit()

        st.success("Publisher edited successfully!")
        st.rerun()

    if st.button("Delete Publisher"):
        # Prepare the SQL statement
        delete_publisher_query = "DELETE FROM Publishers WHERE publisher_id = %s"
        values = (publisher_id,)

        # Execute the SQL statement
        cursor.execute(delete_publisher_query, values)
        db.commit()

        st.success("Publisher deleted successfully!")
        st.rerun()

def view_authors_genres_publishers():
    """
    Displays the list of authors, genres, and publishers.
    """
    st.header("View Authors, Genres, and Publishers")

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


def main():
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


if __name__ == "__main__":
    main()
