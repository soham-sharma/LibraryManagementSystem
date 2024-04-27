CREATE INDEX idx_bk_id ON Books (book_id);
CREATE INDEX idx_br_id ON Borrowers (borrower_id);
CREATE INDEX idx_bc_cid_bid ON BookCopies (copy_id, book_id);
CREATE INDEX idx_bw_ids ON Borrowings (borrowing_id, copy_id, book_id, borrower_id);