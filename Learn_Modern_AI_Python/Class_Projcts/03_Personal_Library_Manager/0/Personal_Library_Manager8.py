import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import random
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem !important;
    color: #1E3A8A;
    font-weight: 700;
    margin-bottom: 1rem;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.sub-header {
    font-size: 1.8rem !important;
    color: #3B82F6;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.success-message {
    padding: 1rem;
    background-color: #ECFDF5;
    border-left: 5px solid #10B981;
    border-radius: 0.375rem;
}
.warning-message {
    padding: 1rem;
    background-color: #FEF3C7;
    border-left: 5px solid #F59E0B;
    border-radius: 0.375rem;
}
.book-card {
    background-color: #F3F4F6;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 5px solid #3B82F6;
    transition: transform 0.3s ease;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.book-card:hover {
    transform: translateY(-5px);
}
.read-badge {
    background-color: #10B981;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 600;
}
.unread-badge {
    background-color: #F87171;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 600;
}
.action-button {
    margin-right: 0.5rem;
}
.stButton>button {
    border-radius: 0.375rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

# Load library

def load_library():
    try:
        if os.path.exists("library.json"):
            with open("library.json", 'r') as file:
                st.session_state.library = json.load(file)
            return True
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False

# Save library

def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

# Add a book

def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

# Remove a book

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# Search books

def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []
    for book in st.session_state.library:
        if search_by == "Title" and search_term in book.get('title', '').lower():
            results.append(book)
        elif search_by == "Author" and search_term in book.get('author', '').lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book.get('genre', '').lower():
            results.append(book)
    st.session_state.search_results = results

# Get library statistics

def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book.get('read_status'))
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        genres[book.get('genre', 'Unknown')] = genres.get(book.get('genre', 'Unknown'), 0) + 1
        authors[book.get('author', 'Unknown')] = authors.get(book.get('author', 'Unknown'), 0) + 1
        try:
            decade = (int(book.get('publication_year', 0)) // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        except:
            pass

    genres = dict(sorted(genres.items(), key=lambda x: x[1], reverse=True))
    authors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))
    decades = dict(sorted(decades.items(), key=lambda x: x[0]))

    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'genres': genres,
        'authors': authors,
        'decades': decades
    }

# Load the library data
load_library()

# Main title
st.markdown("<div class='main-header'>📚 Personal Library Manager</div>", unsafe_allow_html=True)

# Sidebar navigation
view = st.sidebar.radio("Choose an option:", ["Add Book", "View Library", "Search", "Statistics"])

if view == "Add Book":
    st.markdown("### Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=datetime.now().year, value=2020)
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read it?", ["No", "Yes"])
        submitted = st.form_submit_button("Add Book")
        if submitted:
            add_book(title, author, year, genre, read == "Yes")
            st.success("Book added successfully!")

elif view == "View Library":
    st.markdown("### Your Library")
    if not st.session_state.library:
        st.info("No books found.")
    else:
        for i, book in enumerate(st.session_state.library):
            status = "✅ Read" if book.get('read_status') else "📖 Unread"
            st.markdown(f"""
            <div class="book-card">
                <strong>{book.get('title', 'Unknown')}</strong> by {book.get('author', 'Unknown')} ({book.get('publication_year', 'N/A')})<br>
                <em>{book.get('genre', 'Unknown')}</em><br>
                Status: <span class="{'read-badge' if book.get('read_status') else 'unread-badge'}">{status}</span>
                <br><small>Added on: {book.get('added_date', '')}</small>
            </div>
            """, unsafe_allow_html=True)

elif view == "Search":
    st.markdown("### Search Your Library")
    search_term = st.text_input("Enter keyword:")
    search_by = st.selectbox("Search by", ["Title", "Author", "Genre"])
    if st.button("Search"):
        search_books(search_term, search_by)
    for book in st.session_state.search_results:
        status = "✅ Read" if book.get('read_status') else "📖 Unread"
        st.markdown(f"""
        <div class="book-card">
            <strong>{book.get('title', 'Unknown')}</strong> by {book.get('author', 'Unknown')} ({book.get('publication_year', 'N/A')})<br>
            <em>{book.get('genre', 'Unknown')}</em><br>
            Status: <span class="{'read-badge' if book.get('read_status') else 'unread-badge'}">{status}</span>
        </div>
        """, unsafe_allow_html=True)

elif view == "Statistics":
    st.markdown("### Library Statistics")
    stats = get_library_stats()
    st.write(f"**Total Books:** {stats['total_books']}")
    st.write(f"**Books Read:** {stats['read_books']} ({stats['percent_read']:.2f}%)")
    st.write("**Books by Genre:**")
    st.write(stats['genres'])
    st.write("**Books by Author:**")
    st.write(stats['authors'])
    st.write("**Books by Decade:**")
    st.write(stats['decades'])
