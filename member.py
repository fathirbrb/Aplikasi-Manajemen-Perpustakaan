class Member:
    def __init__(self, member_id, name):
        self.id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow(self, book_id):
        self.borrowed_books.append(book_id)

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
