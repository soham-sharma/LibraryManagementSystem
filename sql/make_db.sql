-- Drop the tables if they exist
DROP TABLE IF EXISTS Borrowings;
DROP TABLE IF EXISTS Borrowers;
DROP TABLE IF EXISTS BookCopies;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS Authors;

-- Create the Authors table
CREATE TABLE Authors (
  author_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL
);

-- Create the Genres table
CREATE TABLE Genres (
  genre_id INT PRIMARY KEY AUTO_INCREMENT,
  genre_name VARCHAR(100) NOT NULL
);

-- Create the Publishers table
CREATE TABLE Publishers (
  publisher_id INT PRIMARY KEY AUTO_INCREMENT,
  publisher_name VARCHAR(100) NOT NULL
);

-- Create the Books table
CREATE TABLE Books (
  book_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  author_id INT,
  genre_id INT,
  publisher_id INT,
  published_date DATE,
  FOREIGN KEY (author_id) REFERENCES Authors(author_id),
  FOREIGN KEY (genre_id) REFERENCES Genres(genre_id),
  FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);

-- Create the BookCopies table
CREATE TABLE BookCopies (
  copy_id INT,
  book_id INT,
  PRIMARY KEY (copy_id, book_id),
  FOREIGN KEY (book_id) REFERENCES Books(book_id)
);

-- Create the Borrowers table
CREATE TABLE Borrowers (
  borrower_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  phone_number VARCHAR(15) NOT NULL
);

-- Create the Borrowings table
CREATE TABLE Borrowings (
  borrowing_id INT PRIMARY KEY AUTO_INCREMENT,
  copy_id INT,
  book_id INT,
  borrower_id INT,
  borrow_date DATE,
  return_date DATE,
  FOREIGN KEY (copy_id, book_id) REFERENCES BookCopies(copy_id, book_id),
  FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);