import streamlit as st
import re

st.set_page_config(page_title="Password Strength Meter", layout="centered")

# --- Helper Function ---
def check_strength(password):
    score = 0
    remarks = []

    if len(password) >= 8:
        score += 1
    else:
        remarks.append("❌ Password must be at least 8 characters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        remarks.append("❌ Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        remarks.append("❌ Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        remarks.append("❌ Add digits.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        remarks.append("❌ Add special characters (!@#$...).")

    return score, remarks

# --- Main App ---
st.title("🔐 Password Strength Meter")
password = st.text_input("Enter your password", type="password")

if password:
    score, feedback = check_strength(password)

    st.markdown("### Strength:")
    if score <= 2:
        st.error("Weak 🔴")
    elif score == 3:
        st.warning("Moderate 🟠")
    elif score == 4:
        st.info("Strong 🟡")
    elif score == 5:
        st.success("Very Strong 🟢")

    st.markdown("### Suggestions:")
    if feedback:
        for item in feedback:
            st.write("-", item)
    else:
        st.write("✅ Great password!")
