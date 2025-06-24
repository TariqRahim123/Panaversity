import streamlit as st
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# --- Constants ---
LIBRARY_FILE = "library.json"
DEFAULT_BOOKS = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "genre": "Fiction", "read": True, "link": "https://en.wikipedia.org/wiki/To_Kill_a_Mockingbird"},
    {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian", "read": False, "link": "https://en.wikipedia.org/wiki/Nineteen_Eighty-Four"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "genre": "Romance", "read": True, "link": "https://en.wikipedia.org/wiki/Pride_and_Prejudice"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "genre": "Fiction", "read": True, "link": "https://en.wikipedia.org/wiki/The_Great_Gatsby"},
    {"title": "Moby-Dick", "author": "Herman Melville", "year": 1851, "genre": "Adventure", "read": False, "link": "https://en.wikipedia.org/wiki/Moby-Dick"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "genre": "Fiction", "read": True, "link": "https://en.wikipedia.org/wiki/The_Catcher_in_the_Rye"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "read": True, "link": "https://en.wikipedia.org/wiki/The_Hobbit"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "genre": "Dystopian", "read": False, "link": "https://en.wikipedia.org/wiki/Fahrenheit_451"},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "year": 1847, "genre": "Romance", "read": True, "link": "https://en.wikipedia.org/wiki/Jane_Eyre"},
    {"title": "The Odyssey", "author": "Homer", "year": -800, "genre": "Epic", "read": False, "link": "https://en.wikipedia.org/wiki/Odyssey"},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian", "read": True, "link": "https://en.wikipedia.org/wiki/Brave_New_World"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988, "genre": "Adventure", "read": True, "link": "https://en.wikipedia.org/wiki/The_Alchemist_(novel)"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "year": 1869, "genre": "Historical", "read": False, "link": "https://en.wikipedia.org/wiki/War_and_Peace"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year": 1866, "genre": "Philosophical", "read": False, "link": "https://en.wikipedia.org/wiki/Crime_and_Punishment"},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "year": 2003, "genre": "Fiction", "read": True, "link": "https://en.wikipedia.org/wiki/The_Kite_Runner"},
    {"title": "Frankenstein", "author": "Mary Shelley", "year": 1818, "genre": "Gothic", "read": False, "link": "https://en.wikipedia.org/wiki/Frankenstein"},
    {"title": "Dracula", "author": "Bram Stoker", "year": 1897, "genre": "Horror", "read": False, "link": "https://en.wikipedia.org/wiki/Dracula"},
    {"title": "The Book Thief", "author": "Markus Zusak", "year": 2005, "genre": "Historical", "read": True, "link": "https://en.wikipedia.org/wiki/The_Book_Thief"},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "year": 1847, "genre": "Romance", "read": False, "link": "https://en.wikipedia.org/wiki/Wuthering_Heights"},
    {"title": "Les Misérables", "author": "Victor Hugo", "year": 1862, "genre": "Historical", "read": False, "link": "https://en.wikipedia.org/wiki/Les_Mis%C3%A9rables"}
]

# --- Helper Functions ---
def load_library():
    # If file missing or empty, load defaults
    if not os.path.exists(LIBRARY_FILE):
        return DEFAULT_BOOKS.copy()
    try:
        with open(LIBRARY_FILE, "r") as f:
            data = json.load(f)
        # If file exists but is empty list, treat as defaults
        if not data:
            return DEFAULT_BOOKS.copy()
        return data
    except Exception:
        return DEFAULT_BOOKS.copy()

def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

def get_statistics(library):
    total = len(library)
    read = sum(1 for book in library if book.get("read"))
    df = pd.DataFrame(library) if library else pd.DataFrame()
    genre_counts = df["genre"].value_counts() if not df.empty and "genre" in df.columns else pd.Series()
    year_counts = df["year"].value_counts().sort_index() if not df.empty and "year" in df.columns else pd.Series()
    return total, read, (read / total * 100 if total > 0 else 0), genre_counts, year_counts

# --- UI Styling ---
def style():
    st.markdown("""
        <style>
        .main { background-color: #f0f8ff; }
        .block-container {
            padding: 2rem;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        h2 { color: #004080; }
        </style>
    """, unsafe_allow_html=True)

# --- Main App ---
def main():
    style()
    st.title("📚 Personal Library Manager")
    st.markdown("Manage your reading collection with ease — add, remove, reset, and track your books.")

    if "library" not in st.session_state:
        st.session_state.library = load_library()

    # Sidebar menu with reset
    menu = st.sidebar.radio("Menu", ["Add Book", "View Library", "Search", "Statistics", "Remove Book", "Reset Library"])

    if menu == "Add Book":
        st.subheader("➕ Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=-1000, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Mark as Read")
        link = st.text_input("Optional Link (Wikipedia, Goodreads, etc.)")

        if st.button("Add Book"):
            if title and author and genre:
                st.session_state.library.append({
                    "title": title.strip(),
                    "author": author.strip(),
                    "year": int(year),
                    "genre": genre.strip(),
                    "read": read,
                    "link": link.strip()
                })
                save_library(st.session_state.library)
                st.success(f"'{title}' added to your library.")
            else:
                st.warning("Please fill in title, author, and genre.")

    elif menu == "View Library":
        st.subheader("📖 Your Book List")
        df = pd.DataFrame(st.session_state.library)
        if not df.empty:
            df_display = df.copy()
            df_display["read"] = df_display["read"].apply(lambda x: "✅" if x else "❌")
            if "link" in df_display.columns:
                df_display["link"] = df_display["link"].apply(lambda x: f"[Link]({x})" if x else "")
                st.dataframe(df_display, use_container_width=True)
            else:
                st.dataframe(df_display, use_container_width=True)
            st.download_button("⬇️ Download as CSV", df.to_csv(index=False), file_name="my_library.csv")
        else:
            st.info("No books in your library yet.")

    elif menu == "Search":
        st.subheader("🔍 Search Your Library")
        keyword = st.text_input("Enter title or author keyword")
        if keyword:
            results = [book for book in st.session_state.library
                       if keyword.lower() in book.get('title', '').lower() or keyword.lower() in book.get('author', '').lower()]
            if results:
                st.success(f"Found {len(results)} result(s)")
                st.dataframe(pd.DataFrame(results), use_container_width=True)
            else:
                st.warning("No matching books found.")

    elif menu == "Statistics":
        st.subheader("📊 Reading Statistics")
        total, read, percent, genre_counts, year_counts = get_statistics(st.session_state.library)
        st.metric("Total Books", total)
        st.metric("Books Read", read)
        st.metric("% Completed", f"{percent:.2f}%")

        if not genre_counts.empty:
            st.subheader("Books by Genre")
            fig1, ax1 = plt.subplots()
            genre_counts.plot(kind='bar', ax=ax1, color='skyblue')
            ax1.set_ylabel("Books")
            ax1.set_title("Books per Genre")
            st.pyplot(fig1)

        if not year_counts.empty:
            st.subheader("Books by Publication Year")
            fig2, ax2 = plt.subplots()
            year_counts.plot(kind='line', marker='o', ax=ax2, color='green')
            ax2.set_ylabel("Books")
            ax2.set_xlabel("Year")
            ax2.set_title("Books Added Over Years")
            st.pyplot(fig2)

    elif menu == "Remove Book":
        st.subheader("❌ Remove a Book")
        titles = [book.get('title', '') for book in st.session_state.library]
        if titles:
            selected = st.selectbox("Select a book to remove", titles)
            if st.button("Remove"):
                st.session_state.library = [b for b in st.session_state.library if b.get('title') != selected]
                save_library(st.session_state.library)
                st.success(f"'{selected}' removed.")
        else:
            st.info("Your library is empty.")

    elif menu == "Reset Library":
        st.subheader("🔄 Reset Library to Defaults")
        if st.button("Reset to Default Books"):
            st.session_state.library = DEFAULT_BOOKS.copy()
            save_library(st.session_state.library)
            st.success("Library reset to default books.")

if __name__ == "__main__":
    main()
