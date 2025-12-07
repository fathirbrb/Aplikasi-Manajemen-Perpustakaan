from structures.hashtable import HashTableChaining
from structures.queue import CircularQueue
from structures.stack import Stack
from structures.tree import TreeNode, print_tree_recursive
from structures.graph import Graph
from models.book import Book
from models.member import Member
from models.loan import Loan
from services.sorter import merge_sort
from structures.array import Array

class LibraryService:
    def __init__(self):
        self.books = HashTableChaining(20)
        self.members = HashTableChaining(20)
        self.loans = Array()
        self.waiting_queue = CircularQueue(10)
        self.loan_history = Stack()
        self.category_tree = self._build_category_tree()
        self.recommendation_graph = Graph()
        self._build_graph()

    def _build_category_tree(self):
        root = TreeNode("Kategori Buku")
        fiksi = TreeNode("Fiksi")
        nonfiksi = TreeNode("Non-Fiksi")
        root.add_child(fiksi)
        root.add_child(nonfiksi)
        fiksi.add_child(TreeNode("Novel"))
        fiksi.add_child(TreeNode("Fantasi"))
        nonfiksi.add_child(TreeNode("Sains"))
        nonfiksi.add_child(TreeNode("Sejarah"))
        return root

    def _build_graph(self):
        for bid in ["B001", "B002", "B003", "B004"]:
            self.recommendation_graph.add_vertex(bid)
        self.recommendation_graph.add_edge("B001", "B002")
        self.recommendation_graph.add_edge("B002", "B003")
        self.recommendation_graph.add_edge("B001", "B004")

    def add_book(self, book_id, title, author, category):
        book = Book(book_id, title, author, category)
        self.books.put(book_id, book)

    def add_member(self, member_id, name):
        member = Member(member_id, name)
        self.members.put(member_id, member)

    def borrow_book(self, book_id, member_id):
        book = self.books.get(book_id)
        member = self.members.get(member_id)
        if not book or not member:
            return False
        if not book.available:
            self.waiting_queue.enqueue(member_id)
            return "antrian"
        book.available = False
        member.borrow(book_id)
        loan = Loan(book_id, member_id)
        self.loans.append(loan)
        self.loan_history.push(f"{member_id} meminjam {book_id}")
        return True

    def return_book(self, book_id, member_id):
        book = self.books.get(book_id)
        member = self.members.get(member_id)
        if not book or not member:
            return False
        if member.return_book(book_id):
            book.available = True
            self.loan_history.push(f"{member_id} mengembalikan {book_id}")
            # Beri kesempatan ke antrian
            next_member = self.waiting_queue.dequeue()
            if next_member:
                self.borrow_book(book_id, next_member)
            return True
        return False

    def get_all_books(self):
        all_books = []
        for bucket in self.books.table:
            for key, book in bucket:
                all_books.append(book)
        return all_books

    def get_all_members(self):
        all_members = []
        for bucket in self.members.table:
            for key, member in bucket:
                all_members.append(member)
        return all_members

    def get_category_tree_display(self):
        return print_tree_recursive(self.category_tree)

    def get_recommendations(self, book_id):
        return self.recommendation_graph.bfs(book_id)[1:4]  # ambil 3 rekomendasi