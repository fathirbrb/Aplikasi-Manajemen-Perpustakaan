class Book:
    def __init__(self, book_id, title, author, category):
        self.id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.available = True

    def __repr__(self):
        return f"{self.title} by {self.author} ({'Tersedia' if self.available else 'Dipinjam'})"
