import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet

# --- Constants ---
DATA_FILE = "data_store.json"
LOCKOUT_FILE = "lockout_state.json"
MASTER_PASSWORD = "admin123"
LOCKOUT_DURATION = 60  # seconds

# --- Generate or load encryption key ---
def load_or_create_key(file_path="secret.key"):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                key = f.read()
                # validate key
                Fernet(key)  # will raise ValueError if invalid
                return key
    except Exception:
        st.warning("⚠️ Existing key is invalid. Regenerating a new key (old data will be unreadable).")

    # generate and store new key
    key = Fernet.generate_key()
    with open(file_path, "wb") as f:
        f.write(key)
    return key

KEY = load_or_create_key()
cipher = Fernet(KEY)


# --- Load stored data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        stored_data = json.load(f)
else:
    stored_data = {}

# --- Load lockout state ---
if os.path.exists(LOCKOUT_FILE):
    with open(LOCKOUT_FILE, "r") as f:
        lockout_state = json.load(f)
else:
    lockout_state = {}

# --- Session Initialization ---
if "user" not in st.session_state:
    st.session_state.user = None
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# --- Utilities ---
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f)

def save_lockout_state():
    with open(LOCKOUT_FILE, "w") as f:
        json.dump(lockout_state, f)

def pbkdf2_hash(passkey, salt="somesalt"):
    return hashlib.pbkdf2_hmac("sha256", passkey.encode(), salt.encode(), 100000).hex()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

def is_locked_out(username):
    lock_info = lockout_state.get(username)
    if not lock_info:
        return False
    if time.time() < lock_info["until"]:
        return True
    else:
        del lockout_state[username]
        save_lockout_state()
        return False

def lockout_user(username):
    lockout_state[username] = {"until": time.time() + LOCKOUT_DURATION}
    save_lockout_state()

# --- Styling ---
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Pages ---
def home_page():
    st.title("🔐 Secure Data Encryption System")
    st.markdown("Welcome to your personal encrypted vault. Store and retrieve your data safely with strong encryption and modern security.")

def register_page():
    st.header("📝 Register")
    with st.container():
        username = st.text_input("Choose a username")
        password = st.text_input("Choose a password", type="password")
        if st.button("Register"):
            if username in stored_data:
                st.error("🚫 Username already exists.")
            else:
                stored_data[username] = {"password": pbkdf2_hash(password), "data": []}
                save_data()
                st.success("✅ Registered successfully. Please login.")

def login_page():
    st.header("🔐 Login")
    with st.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if is_locked_out(username):
                st.warning("⏳ Locked out. Try again later.")
                return
            user = stored_data.get(username)
            if user and user["password"] == pbkdf2_hash(password):
                st.session_state.user = username
                st.session_state.failed_attempts = 0
                st.success(f"✅ Welcome back, {username}!")
            else:
                st.session_state.failed_attempts += 1
                st.error(f"❌ Invalid credentials. Attempts left: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3:
                    lockout_user(username)
                    st.warning("🔒 You are temporarily locked out.")

def store_data_page():
    st.header("📦 Store Data")
    if not st.session_state.user:
        st.warning("Please login first.")
        return
    user_data = st.text_area("Enter data to encrypt:")
    if st.button("Encrypt & Save"):
        if user_data:
            encrypted = encrypt_data(user_data)
            stored_data[st.session_state.user]["data"].append(encrypted)
            save_data()
            st.success("✅ Data saved successfully.")
            st.code(encrypted, language="text")
        else:
            st.error("⚠️ Data is empty.")

def retrieve_data_page():
    st.header("🔓 Retrieve Data")
    if not st.session_state.user:
        st.warning("Please login first.")
        return
    encrypted_entries = stored_data[st.session_state.user].get("data", [])
    if not encrypted_entries:
        st.info("You have no saved entries.")
        return
    selected = st.selectbox("Choose encrypted entry:", encrypted_entries)
    if st.button("Decrypt"):
        try:
            decrypted = decrypt_data(selected)
            st.success("✅ Data decrypted successfully.")
            st.text_area("Decrypted content:", decrypted, height=100)
        except:
            st.error("❌ Failed to decrypt data.")

def logout_page():
    st.session_state.user = None
    st.success("🚪 Logged out successfully.")

# --- Sidebar Navigation ---
st.sidebar.title("🔧 Navigation")
menu = ["Home", "Register", "Login", "Store Data", "Retrieve Data", "Logout"]
choice = st.sidebar.radio("Go to", menu)

# --- Routing ---
if choice == "Home":
    home_page()
elif choice == "Register":
    register_page()
elif choice == "Login":
    login_page()
elif choice == "Store Data":
    store_data_page()
elif choice == "Retrieve Data":
    retrieve_data_page()
elif choice == "Logout":
    logout_page()
