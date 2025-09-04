"""
Library Management System
-------------------------
Features:
- Add books
- Borrow books
- Return books
- List available / borrowed books
- Save & Load to JSON
- Export to CSV
"""

import json
import csv
from datetime import datetime

# Book status options (tuple to demonstrate tuple usage)
BOOK_STATUS = ("Available", "Borrowed")

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.status = BOOK_STATUS[0]  # Default: Available
        self.borrowed_date = None

    def borrow(self):
        if self.status == BOOK_STATUS[1]:
            return False
        self.status = BOOK_STATUS[1]
        self.borrowed_date = datetime.today().strftime("%Y-%m-%d")
        return True

    def return_book(self):
        if self.status == BOOK_STATUS[0]:
            return False
        self.status = BOOK_STATUS[0]
        self.borrowed_date = None
        return True

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
            "borrowed_date": self.borrowed_date
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["year"])
        book.status = data["status"]
        book.borrowed_date = data.get("borrowed_date")
        return book


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"✓ '{book.title}' added to library.")

    def list_books(self, status=None):
        if not self.books:
            print("No books in library yet.")
            return
        print("\nBooks in Library:")
        for i, book in enumerate(self.books, 1):
            if status is None or book.status == status:
                print(f"{i}. {book.title} by {book.author} ({book.year}) - {book.status}")

    def borrow_book(self, index):
        try:
            book = self.books[index - 1]
            if book.borrow():
                print(f"✓ You borrowed '{book.title}'.")
            else:
                print(f"! '{book.title}' is already borrowed.")
        except IndexError:
            print("! Invalid book number.")

    def return_book(self, index):
        try:
            book = self.books[index - 1]
            if book.return_book():
                print(f"✓ You returned '{book.title}'.")
            else:
                print(f"! '{book.title}' was not borrowed.")
        except IndexError:
            print("! Invalid book number.")

    def save(self, filename="library.json"):
        try:
            with open(filename, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            print("✓ Library saved.")
        except Exception as e:
            print("! Error saving library:", e)

    def load(self, filename="library.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.books = [Book.from_dict(d) for d in data]
            print("✓ Library loaded.")
        except FileNotFoundError:
            print("! No saved library found.")
        except Exception as e:
            print("! Error loading library:", e)

    def export_csv(self, filename="library.csv"):
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Author", "Year", "Status", "Borrowed Date"])
                for b in self.books:
                    writer.writerow([b.title, b.author, b.year, b.status, b.borrowed_date])
            print("✓ Exported to CSV.")
        except Exception as e:
            print("! Error exporting CSV:", e)


def menu():
    print("""
===== LIBRARY MENU =====
1. Add Book
2. List All Books
3. List Available Books
4. List Borrowed Books
5. Borrow Book
6. Return Book
7. Save Library
8. Load Library
9. Export to CSV
0. Exit
========================
""")


def main():
    library = Library()
    library.load()  # Try to load saved library at start

    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            year = input("Year: ")
            library.add_book(Book(title, author, year))
        elif choice == "2":
            library.list_books()
        elif choice == "3":
            library.list_books(status="Available")
        elif choice == "4":
            library.list_books(status="Borrowed")
        elif choice == "5":
            library.list_books(status="Available")
            try:
                num = int(input("Enter book number to borrow: "))
                library.borrow_book(num)
            except ValueError:
                print("! Please enter a valid number.")
        elif choice == "6":
            library.list_books(status="Borrowed")
            try:
                num = int(input("Enter book number to return: "))
                library.return_book(num)
            except ValueError:
                print("! Please enter a valid number.")
        elif choice == "7":
            library.save()
        elif choice == "8":
            library.load()
        elif choice == "9":
            library.export_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("! Invalid choice, try again.")


try:
    main()
except KeyboardInterrupt:
    print("\nExiting program.")

