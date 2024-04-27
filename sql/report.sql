DELIMITER //
CREATE PROCEDURE GenerateDataReport()
BEGIN
  -- Create a temporary table
  CREATE TEMPORARY TABLE IF NOT EXISTS TempReport AS
    SELECT b.title, a.name AS author, g.genre_name, p.publisher_name, bc.copy_id, br.borrow_date, br.return_date, bo.name AS borrower
    FROM Borrowings br
    INNER JOIN BookCopies bc ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id
    INNER JOIN Books b ON bc.book_id = b.book_id
    INNER JOIN Authors a ON b.author_id = a.author_id
    INNER JOIN Genres g ON b.genre_id = g.genre_id
    INNER JOIN Publishers p ON b.publisher_id = p.publisher_id
    INNER JOIN Borrowers bo ON br.borrower_id = bo.borrower_id;
END //
DELIMITER ;