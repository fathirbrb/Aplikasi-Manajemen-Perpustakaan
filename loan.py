from datetime import datetime

class Loan:
    def __init__(self, book_id, member_id):
        self.book_id = book_id
        self.member_id = member_id
        self.date = datetime.now().strftime("%Y-%m-%d")
