import streamlit as st
import edit_data
import books
import edit_book_copies
import borrowers
import borrowings
import data_report

def edit_lib_data():
    st.sidebar.title("Select fields to edit")
    page = st.sidebar.selectbox("Select a page", ["Books", "Book Copies", "Borrowers", "Borrowings"])

    if page == "Books":
        books.main()
    elif page == "Borrowers":
        borrowers.main()
    elif page == "Book Copies":
        edit_book_copies.main()
    elif page == "Borrowings":
        borrowings.main()
def main():
    st.title("Library Management System")
    st.sidebar.title("Library Management System")
    page = st.sidebar.selectbox("Select a page", ["View/ Edit Library Data",
                                                  "View/ Edit Book Data", "Data Report"])
    if page == "View/ Edit Library Data":
        edit_lib_data()
    elif page == "View/ Edit Book Data":
        edit_data.main()
    elif page == "Data Report":
        data_report.main()


if __name__ == "__main__":
    main()
