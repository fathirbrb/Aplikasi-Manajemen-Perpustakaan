import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from services.library_service import LibraryService

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Perpustakaan")
        self.root.geometry("950x650")
        self.root.configure(bg="#0B1A30")  # Navy Midnight
        self.root.resizable(True, True)

        # Warna tema biru elegan
        self.bg_color = "#0B1A30"
        self.panel_bg = "#122640"
        self.fg_color = "#E0F0FF"
        self.fg_secondary = "#A0C4E8"
        self.button_bg = "#3A7CA5"
        self.button_fg = "#FFFFFF"
        self.highlight = "#5DA9E9"
        self.entry_bg = "#122640"

        self.service = LibraryService()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        try:
            style.theme_use('default')
        except:
            pass
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.map('TNotebook.Tab',
                  background=[('selected', self.button_bg), ('!selected', self.panel_bg)],
                  foreground=[('selected', "#000000"), ('!selected', self.fg_color)])

        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        book_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(book_tab, text="📚 Buku")
        self.create_book_tab(book_tab)

        member_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(member_tab, text="👥 Anggota")
        self.create_member_tab(member_tab)

        loan_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(loan_tab, text="📖 Peminjaman")
        self.create_loan_tab(loan_tab)

        other_tab = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(other_tab, text="🔍 Lainnya")
        self.create_other_tab(other_tab)

    def create_book_tab(self, parent):
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(pady=10)

        btn_config = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "font": ("Arial", 9, "bold"),
            "activebackground": "#4A8DB5",
            "activeforeground": "#FFFFFF",
            "relief": "flat",
            "padx": 8,
            "pady": 4,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="➕ Tambah Buku", command=self.add_book, **btn_config).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="❌ Hapus Buku", command=self.delete_book, **btn_config).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Refresh", command=self.show_books, **btn_config).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Urutkan Judul", command=self.sort_books_by_title, **btn_config).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Urutkan ID", command=self.sort_books_by_id, **btn_config).pack(side=tk.LEFT, padx=3)

        list_frame = tk.Frame(parent, bg=self.bg_color)
        list_frame.pack(pady=10, fill='both', expand=True)

        self.book_listbox = tk.Listbox(
            list_frame,
            bg=self.entry_bg,
            fg=self.fg_color,
            selectbackground=self.highlight,
            selectforeground="#000000",
            font=("Consolas", 10),
            relief="flat",
            borderwidth=0
        )
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.book_listbox.yview)
        self.book_listbox.config(yscrollcommand=scrollbar.set)

        self.book_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_member_tab(self, parent):
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(pady=10)

        btn_config = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "font": ("Arial", 10, "bold"),
            "activebackground": "#4A8DB5",
            "activeforeground": "#FFFFFF",
            "relief": "flat",
            "padx": 10,
            "pady": 5,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="➕ Tambah Anggota", command=self.add_member, **btn_config).pack(pady=5)
        tk.Button(btn_frame, text="❌ Hapus Anggota", command=self.delete_member, **btn_config).pack(pady=5)
        tk.Button(btn_frame, text="Refresh", command=self.show_members, **btn_config).pack(pady=5)

        self.member_listbox = tk.Listbox(
            parent,
            bg=self.entry_bg,
            fg=self.fg_color,
            selectbackground=self.highlight,
            selectforeground="#000000",
            font=("Consolas", 10),
            relief="flat",
            borderwidth=0
        )
        self.member_listbox.pack(pady=10, fill='both', expand=True)

    def create_loan_tab(self, parent):
        btn_config = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "font": ("Arial", 10, "bold"),
            "activebackground": "#4A8DB5",
            "activeforeground": "#FFFFFF",
            "relief": "flat",
            "padx": 15,
            "pady": 6,
            "cursor": "hand2"
        }

        tk.Button(parent, text="📖 Pinjam Buku", command=self.borrow_book, **btn_config).pack(pady=6)
        tk.Button(parent, text="↩️ Kembalikan Buku", command=self.return_book, **btn_config).pack(pady=6)
        tk.Button(parent, text="📜 Riwayat Peminjaman", command=self.show_history, **btn_config).pack(pady=6)

    def create_other_tab(self, parent):
        btn_config = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "font": ("Arial", 10, "bold"),
            "activebackground": "#4A8DB5",
            "activeforeground": "#FFFFFF",
            "relief": "flat",
            "padx": 15,
            "pady": 6,
            "cursor": "hand2"
        }

        tk.Button(parent, text="🌳 Tampilkan Kategori Buku", command=self.show_categories, **btn_config).pack(pady=8)

    # === FUNGSI BUKU ===
    def add_book(self):
        try:
            book_id = simpledialog.askstring("Input", "ID Buku (contoh: B005):", parent=self.root)
            if not book_id: return
            title = simpledialog.askstring("Input", "Judul Buku:", parent=self.root)
            if not title: return
            author = simpledialog.askstring("Input", "Penulis:", parent=self.root)
            if not author: return
            category = simpledialog.askstring("Input", "Kategori:", parent=self.root)
            if not category: return
            self.service.add_book(book_id, title, author, category)
            messagebox.showinfo("✅ Sukses", "Buku berhasil ditambahkan!", parent=self.root)
            self.show_books()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menambah buku: {e}", parent=self.root)

    def delete_book(self):
        try:
            book_id = simpledialog.askstring("Hapus Buku", "Masukkan ID Buku yang akan dihapus:", parent=self.root)
            if not book_id: return
            book = self.service.books.get(book_id)
            if not book:
                messagebox.showwarning("⚠️ Tidak Ditemukan", "ID Buku tidak ditemukan.", parent=self.root)
                return
            if not book.available:
                messagebox.showwarning("⚠️ Tidak Bisa Dihapus", "Buku sedang dipinjam, tidak bisa dihapus.", parent=self.root)
                return
            self.service.books.remove(book_id)
            messagebox.showinfo("✅ Sukses", "Buku berhasil dihapus!", parent=self.root)
            self.show_books()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menghapus buku: {e}", parent=self.root)

    def show_books(self):
        try:
            self.book_listbox.delete(0, tk.END)
            books = self.service.get_all_books()
            if not books:
                self.book_listbox.insert(tk.END, "Belum ada buku.")
                return
            for book in books:
                status = "Tersedia" if book.available else "Dipinjam"
                self.book_listbox.insert(tk.END, f"{book.id} | {book.title} | {book.author} | {status}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal memuat buku: {e}", parent=self.root)

    def sort_books_by_title(self):
        try:
            self.book_listbox.delete(0, tk.END)
            books = self.service.get_all_books()
            if not books:
                self.book_listbox.insert(tk.END, "Belum ada buku.")
                return
            from services.sorter import merge_sort
            sorted_books = merge_sort(books, key=lambda b: b.title.lower())
            for book in sorted_books:
                status = "Tersedia" if book.available else "Dipinjam"
                self.book_listbox.insert(tk.END, f"{book.id} | {book.title} | {book.author} | {status}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal mengurutkan berdasarkan judul: {e}", parent=self.root)

    def sort_books_by_id(self):
        try:
            self.book_listbox.delete(0, tk.END)
            books = self.service.get_all_books()
            if not books:
                self.book_listbox.insert(tk.END, "Belum ada buku.")
                return
            from services.sorter import merge_sort
            def extract_id_num(book):
                try:
                    return int(''.join(filter(str.isdigit, book.id)))
                except:
                    return book.id
            sorted_books = merge_sort(books, key=extract_id_num)
            for book in sorted_books:
                status = "Tersedia" if book.available else "Dipinjam"
                self.book_listbox.insert(tk.END, f"{book.id} | {book.title} | {book.author} | {status}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal mengurutkan berdasarkan ID: {e}", parent=self.root)

    # === FUNGSI ANGGOTA ===
    def add_member(self):
        try:
            member_id = simpledialog.askstring("Input", "ID Anggota (contoh: M003):", parent=self.root)
            if not member_id: return
            name = simpledialog.askstring("Input", "Nama Lengkap:", parent=self.root)
            if not name: return
            self.service.add_member(member_id, name)
            messagebox.showinfo("✅ Sukses", "Anggota berhasil ditambahkan!", parent=self.root)
            self.show_members()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menambah anggota: {e}", parent=self.root)

    def delete_member(self):
        try:
            member_id = simpledialog.askstring("Hapus Anggota", "Masukkan ID Anggota yang akan dihapus:", parent=self.root)
            if not member_id: return
            member = self.service.members.get(member_id)
            if not member:
                messagebox.showwarning("⚠️ Tidak Ditemukan", "ID Anggota tidak ditemukan.", parent=self.root)
                return
            if len(member.borrowed_books) > 0:
                messagebox.showwarning("⚠️ Tidak Bisa Dihapus", "Anggota masih meminjam buku, tidak bisa dihapus.", parent=self.root)
                return
            self.service.members.remove(member_id)
            messagebox.showinfo("✅ Sukses", "Anggota berhasil dihapus!", parent=self.root)
            self.show_members()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menghapus anggota: {e}", parent=self.root)

    def show_members(self):
        try:
            self.member_listbox.delete(0, tk.END)
            members = self.service.get_all_members()
            if not members:
                self.member_listbox.insert(tk.END, "Belum ada anggota.")
                return
            for m in members:
                self.member_listbox.insert(tk.END, f"{m.id} | {m.name} | Meminjam: {len(m.borrowed_books)} buku")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal memuat anggota: {e}", parent=self.root)

    # === FUNGSI PEMINJAMAN ===
    def borrow_book(self):
        try:
            book_id = simpledialog.askstring("Input", "ID Buku:", parent=self.root)
            if not book_id: return
            member_id = simpledialog.askstring("Input", "ID Anggota:", parent=self.root)
            if not member_id: return
            result = self.service.borrow_book(book_id, member_id)
            if result is True:
                messagebox.showinfo("✅ Sukses", "Buku berhasil dipinjam!", parent=self.root)
            elif result == "antrian":
                messagebox.showwarning("⏳ Antrian", "Buku sedang dipinjam. Anda masuk antrian!", parent=self.root)
            else:
                messagebox.showerror("❌ Gagal", "ID buku atau anggota tidak ditemukan!", parent=self.root)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal meminjam buku: {e}", parent=self.root)

    def return_book(self):
        try:
            book_id = simpledialog.askstring("Input", "ID Buku:", parent=self.root)
            if not book_id: return
            member_id = simpledialog.askstring("Input", "ID Anggota:", parent=self.root)
            if not member_id: return
            if self.service.return_book(book_id, member_id):
                messagebox.showinfo("✅ Sukses", "Buku berhasil dikembalikan!", parent=self.root)
            else:
                messagebox.showerror("❌ Gagal", "Gagal mengembalikan buku. Periksa ID!", parent=self.root)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal mengembalikan buku: {e}", parent=self.root)

    def show_history(self):
        try:
            history = []
            temp_stack = []
            while not self.service.loan_history.is_empty():
                item = self.service.loan_history.pop()
                history.append(item)
                temp_stack.append(item)
            for item in reversed(temp_stack):
                self.service.loan_history.push(item)
            msg = "\n".join(history) if history else "Belum ada riwayat peminjaman."
            messagebox.showinfo("📜 Riwayat", msg, parent=self.root)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal memuat riwayat: {e}", parent=self.root)

    # === FITUR TAMBAHAN ===
    def show_categories(self):
        try:
            categories = self.service.get_category_tree_display()
            if not categories:
                msg = "Tidak ada kategori buku."
            else:
                msg = "KATEGORI BUKU DI PERPUSTAKAAN:\n" + "\n".join(categories)
            messagebox.showinfo("🌳 Kategori Buku", msg, parent=self.root)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menampilkan kategori: {e}", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
