import json
import os

LIBRARY_FILE = 'library.txt'

# Load existing library from file
if os.path.exists(LIBRARY_FILE):
    with open(LIBRARY_FILE, 'r') as file:
        library = json.load(file)
else:
    library = []

def save_library():
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=4)

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = True if read_input == 'yes' else False
    
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    library.append(book)
    print("Book added successfully!\n")

def remove_book():
    title = input("Enter the title of the book to remove: ").strip()
    global library
    library = [book for book in library if book['title'].lower() != title.lower()]
    print("Book removed successfully!\n")

def search_book():
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")
    keyword = input("Enter the search keyword: ").strip().lower()
    results = []
    if choice == '1':
        results = [book for book in library if keyword in book['title'].lower()]
    elif choice == '2':
        results = [book for book in library if keyword in book['author'].lower()]
    print("\nMatching Books:")
    for idx, book in enumerate(results, 1):
        display_book(book, idx)
    print()

def display_book(book, idx=None):
    prefix = f"{idx}. " if idx else ""
    status = 'Read' if book['read'] else 'Unread'
    print(f"{prefix}{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_all_books():
    if not library:
        print("No books in the library.\n")
        return
    print("\nYour Library:")
    for idx, book in enumerate(library, 1):
        display_book(book, idx)
    print()

def display_statistics():
    total_books = len(library)
    if total_books == 0:
        print("No books to calculate statistics.\n")
        return
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100
    print(f"Total books: {total_books}")
    print(f"Percentage read: {percentage_read:.1f}%\n")

def main():
    while True:
        print("""
Welcome to your Personal Library Manager!
1. Add a book
2. Remove a book
3. Search for a book
4. Display all books
5. Display statistics
6. Exit
""")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            search_book()
        elif choice == '4':
            display_all_books()
        elif choice == '5':
            display_statistics()
        elif choice == '6':
            save_library()
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()