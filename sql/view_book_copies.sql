DELIMITER //
CREATE PROCEDURE ViewBookCopies()
BEGIN
    -- Create a temporary table
    CREATE TEMPORARY TABLE TempViewBookCopies (
        Title VARCHAR(255),
        AllCopies TEXT,
        TotalCopies INT,
        CheckedOutCopies TEXT,
        CheckedOutCount INT,
        AvailableCopies TEXT,
        AvailableCount INT
    );

    BEGIN
        -- Declare variables
        DECLARE done INT DEFAULT 0;
        DECLARE b_title VARCHAR(255);
        DECLARE all_copies TEXT;
        DECLARE total_copies INT;
        DECLARE checked_out_copies TEXT;
        DECLARE checked_out_count INT;
        DECLARE available_copies TEXT;
        DECLARE available_count INT;

        -- Declare a cursor for the books and copies
        DECLARE cur CURSOR FOR
            SELECT b.title, GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id) AS all_copies, COUNT(bc.copy_id)
            FROM Books b
            JOIN BookCopies bc ON b.book_id = bc.book_id
            GROUP BY b.title;

        -- Declare a handler for the end of the cursor loop
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

        -- Open the cursor
        OPEN cur;

        -- Start the cursor loop
        read_loop: LOOP
            -- Fetch the next row from the cursor
            FETCH cur INTO b_title, all_copies, total_copies;

            -- If we're done, exit the loop
            IF done THEN
                LEAVE read_loop;
            END IF;

            -- Fetch the names and count of checked out copies for the current book
            SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) INTO checked_out_copies, checked_out_count
            FROM Borrowings br
            JOIN BookCopies bc ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id
            JOIN Books b ON bc.book_id = b.book_id
            WHERE b.title = b_title;

            -- Fetch the names and count of available copies for the current book
            SELECT GROUP_CONCAT('Copy ', bc.copy_id ORDER BY bc.copy_id), COUNT(bc.copy_id) INTO available_copies, available_count
            FROM BookCopies bc
            JOIN Books b ON bc.book_id = b.book_id
            LEFT JOIN Borrowings br ON br.copy_id = bc.copy_id AND br.book_id = bc.book_id
            WHERE b.title = b_title AND br.copy_id IS NULL;

            -- Insert the results into the temporary table
            INSERT INTO TempViewBookCopies VALUES (b_title, all_copies, total_copies, checked_out_copies, checked_out_count, available_copies, available_count);
        END LOOP;

        -- Close the cursor
        CLOSE cur;
    END;
END
//
DELIMITER ;
