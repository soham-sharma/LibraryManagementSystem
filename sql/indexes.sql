CREATE INDEX idx_bk_id ON Books (book_id);
CREATE INDEX idx_br_id ON Borrowers (borrower_id);
CREATE INDEX idx_bc_cid_bid ON BookCopies (copy_id, book_id);
CREATE INDEX idx_gr_id ON Genres (genre_id);
CREATE INDEX idx_pb_id ON Publishers (publisher_id);