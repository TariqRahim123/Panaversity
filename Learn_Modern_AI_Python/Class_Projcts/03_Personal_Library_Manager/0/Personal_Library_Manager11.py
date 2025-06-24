import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import random
import requests
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if 'selected_book_index' not in st.session_state:
    st.session_state.selected_book_index = None

# Load library

def load_library():
    if os.path.exists("library.json"):
        with open("library.json", 'r') as file:
            st.session_state.library = json.load(file)

def save_library():
    with open('library.json', 'w') as file:
        json.dump(st.session_state.library, file)

# Add book

def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': int(publication_year),
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

# Remove book

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True

# Update book

def update_book(index, title, author, publication_year, genre, read_status):
    if 0 <= index < len(st.session_state.library):
        st.session_state.library[index].update({
            'title': title,
            'author': author,
            'publication_year': int(publication_year),
            'genre': genre,
            'read_status': read_status
        })
        save_library()

# Search books

def search_books(search_term, search_by):
    results = []
    for book in st.session_state.library:
        if search_by == "Title" and search_term.lower() in book.get('title', '').lower():
            results.append(book)
        elif search_by == "Author" and search_term.lower() in book.get('author', '').lower():
            results.append(book)
        elif search_by == "Genre" and search_term.lower() in book.get('genre', '').lower():
            results.append(book)
    st.session_state.search_results = results

# Statistics

def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book.get('read_status'))
    unread_books = total_books - read_books
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

    return {
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': unread_books,
        'percent_read': percent_read,
        'genres': genres,
        'authors': authors,
        'decades': decades
    }

load_library()

st.title("📚 Personal Library Manager")

view = st.sidebar.radio("Choose an option:", ["Add Book", "View Library", "Search", "Statistics"])

if view == "Add Book":
    st.subheader("Add a New Book")
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
    if st.session_state.selected_book_index is not None:
        index = st.session_state.selected_book_index
        book = st.session_state.library[index]
        st.subheader("Edit Book Details")
        with st.form("edit_book_form"):
            title = st.text_input("Title", value=book['title'])
            author = st.text_input("Author", value=book['author'])
            year = st.number_input("Publication Year", min_value=0, max_value=datetime.now().year, value=int(book['publication_year']))
            genre = st.text_input("Genre", value=book['genre'])
            read = st.selectbox("Have you read it?", ["No", "Yes"], index=1 if book['read_status'] else 0)
            update = st.form_submit_button("Update Book")
            delete = st.form_submit_button("Delete Book")
            if update:
                update_book(index, title, author, year, genre, read == "Yes")
                st.success("Book updated successfully.")
            if delete:
                remove_book(index)
                st.success("Book deleted.")
                st.session_state.selected_book_index = None

        if st.button("Back to Library"):
            st.session_state.selected_book_index = None

    else:
        st.subheader("Your Library")
        if not st.session_state.library:
            st.info("No books in your library.")
        else:
            for i, book in enumerate(st.session_state.library):
                with st.expander(f"{book['title']} by {book['author']}"):
                    st.markdown(f"""
                    **Title**: {book['title']}  
                    **Author**: {book['author']}  
                    **Year**: {book.get('publication_year', 'Unknown')}  
                    **Genre**: {book['genre']}  
                    **Status**: {'Read' if book['read_status'] else 'Unread'}  
                    **Added**: {book['added_date']}
                    """)
                    if st.button(f"Edit Book {i}"):
                        st.session_state.selected_book_index = i
                        st.experimental_rerun()

elif view == "Search":
    st.subheader("Search Your Library")
    search_term = st.text_input("Search keyword")
    search_by = st.selectbox("Search by", ["Title", "Author", "Genre"])
    if st.button("Search"):
        search_books(search_term, search_by)

    for book in st.session_state.search_results:
        st.markdown(f"""
        **Title**: {book['title']}  
        **Author**: {book['author']}  
        **Year**: {book.get('publication_year', 'Unknown')}  
        **Genre**: {book['genre']}  
        **Status**: {'Read' if book['read_status'] else 'Unread'}  
        **Added**: {book['added_date']}
        """)

elif view == "Statistics":
    st.subheader("Library Statistics")
    stats = get_library_stats()

    st.markdown(f"**Total Books:** {stats['total_books']}")
    st.markdown(f"**Books Read:** {stats['read_books']}")
    st.markdown(f"**Books Unread:** {stats['unread_books']}")
    st.markdown(f"**Read Percentage:** {stats['percent_read']:.2f}%")

    df_genre = pd.DataFrame(list(stats['genres'].items()), columns=["Genre", "Count"])
    df_author = pd.DataFrame(list(stats['authors'].items()), columns=["Author", "Count"])
    df_decade = pd.DataFrame(list(stats['decades'].items()), columns=["Decade", "Count"])

    st.subheader("📊 Tabular Overview")
    st.write("**By Genre**")
    st.dataframe(df_genre)
    st.write("**By Author (Top 10)**")
    st.dataframe(df_author.sort_values("Count", ascending=False).head(10))
    st.write("**By Decade**")
    st.dataframe(df_decade)

    st.subheader("📊 Charts")
    fig, ax = plt.subplots()
    sns.barplot(data=df_genre, x="Count", y="Genre", ax=ax)
    ax.set_title("Books by Genre")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.barplot(data=df_author.sort_values("Count", ascending=False).head(10), x="Count", y="Author", ax=ax)
    ax.set_title("Top 10 Authors")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.barplot(data=df_decade, x="Decade", y="Count", ax=ax)
    ax.set_title("Books by Decade")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.pie([stats['read_books'], stats['unread_books']], labels=['Read', 'Unread'], autopct='%1.1f%%', startangle=140, colors=['#10B981', '#F87171'])
    ax.axis('equal')
    st.pyplot(fig)
