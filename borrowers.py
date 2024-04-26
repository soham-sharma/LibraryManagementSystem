import streamlit as st
from db_conn import create_conn


db = create_conn()
cursor = db.cursor()


def add_borrower(name, phone_number):
    """
    Adds a new borrower to the database.
    """
    add_borrower_query = "INSERT INTO Borrowers (name, phone_number) VALUES (%s, %s)"
    values = (name, phone_number)
    cursor.execute(add_borrower_query, values)
    db.commit()
    st.rerun()


def edit_borrower(borrower_id, name, phone_number):
    """
    Edits the details of a borrower in the database.
    """
    edit_borrower_query = "UPDATE Borrowers SET name = %s, phone_number = %s WHERE borrower_id = %s"
    values = (name, phone_number, borrower_id)
    cursor.execute(edit_borrower_query, values)
    db.commit()
    st.rerun()


def delete_borrower(borrower_id):
    """
    Deletes a borrower from the database.
    """
    delete_borrower_query = "DELETE FROM Borrowers WHERE borrower_id = %s"
    values = (borrower_id,)
    cursor.execute(delete_borrower_query, values)
    db.commit()
    st.rerun()

def view_borrowers():
    """
    Displays the list of borrowers.
    """
    st.header("View Borrowers")

    # Fetch all borrowers
    cursor.execute("SELECT borrower_id, name, phone_number FROM Borrowers")
    borrowers = cursor.fetchall()

    # Prepare data for the table
    table_data = [{"Borrower ID": borrower[0], "Name": borrower[1], "Phone Number": borrower[2]} for borrower in borrowers]

    # Display the data in a table
    st.table(table_data)


def main():
    st.title("Borrower Management")

    options = ["Add Borrower", "Edit/Delete Borrower", "View Borrowers"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Add Borrower":
        st.header("Add a Borrower")
        name = st.text_input("Name")
        phone_number = st.text_input("Phone Number")

        if st.button("Add Borrower"):
            add_borrower(name, phone_number)
            st.success("Borrower added successfully.")

    elif choice == "Edit/Delete Borrower":
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
                edit_borrower(selected_borrower_id, name, phone_number)
                st.success("Borrower details updated successfully.")

            if st.button("Delete Borrower"):
                delete_borrower(selected_borrower_id)
                st.success("Borrower deleted successfully.")
    elif choice == "View Borrowers":
        view_borrowers()


if __name__ == "__main__":
    main()
