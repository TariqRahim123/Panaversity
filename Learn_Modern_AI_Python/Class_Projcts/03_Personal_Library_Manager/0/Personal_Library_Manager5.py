import streamlit as st
import json
import os

# JSON file to persist data
LIBRARY_FILE = "library.json"

# Load existing library
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save library
def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

# Add a new book
def add_book(library, title, author, year, genre, read):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    library.append(book)
    save_library(library)
    st.success(f"✅ '{title}' added to library!")

# Remove a book by title
def remove_book(library, title):
    updated_library = [book for book in library if book['title'].lower() != title.lower()]
    if len(updated_library) < len(library):
        save_library(updated_library)
        st.success(f"✅ '{title}' removed from library!")
    else:
        st.warning("❌ Book not found!")
    return updated_library

# Search books
def search_books(library, keyword, search_by="title"):
    return [book for book in library if keyword.lower() in book[search_by].lower()]

# Display a book
def display_book(book):
    read_status = "✅ Read" if book['read'] else "❌ Unread"
    st.markdown(
        f"**{book['title']}** by *{book['author']}* ({book['year']})  \n"
        f"Genre: _{book['genre']}_  \n"
        f"Status: {read_status}"
    )

# Display statistics
def display_statistics(library):
    total = len(library)
    read_count = sum(book['read'] for book in library)
    read_percent = (read_count / total) * 100 if total > 0 else 0

    st.subheader("📊 Library Statistics")
    st.write(f"**Total books:** {total}")
    st.write(f"**Books read:** {read_count}")
    st.progress(int(read_percent))
    st.write(f"**Percentage read:** {read_percent:.1f}%")

# Main Streamlit App
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

library = load_library()

# Sidebar for navigation
option = st.sidebar.radio(
    "Choose an action:",
    ("Add Book", "Remove Book", "Search Book", "View All Books", "Statistics")
)

# === Add Book ===
if option == "Add Book":
    st.header("➕ Add a Book")
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read it?", value=False)
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if title and author and genre:
                add_book(library, title, author, year, genre, read)
            else:
                st.warning("❗ Please fill all required fields.")

# === Remove Book ===
elif option == "Remove Book":
    st.header("➖ Remove a Book")
    if library:
        titles = [book['title'] for book in library]
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove"):
            library = remove_book(library, book_to_remove)
    else:
        st.info("📂 No books to remove.")

# === Search Book ===
elif option == "Search Book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    keyword = st.text_input("Enter search keyword")
    if keyword:
        results = search_books(library, keyword, search_by)
        if results:
            st.success(f"Found {len(results)} matching book(s):")
            for book in results:
                display_book(book)
                st.markdown("---")
        else:
            st.warning("❌ No matches found.")

# === View All Books ===
elif option == "View All Books":
    st.header("📖 All Books in Library")
    if library:
        for book in library:
            display_book(book)
            st.markdown("---")
    else:
        st.info("📂 Your library is empty.")

# === Statistics ===
elif option == "Statistics":
    display_statistics(library)
