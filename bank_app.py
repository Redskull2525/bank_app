import streamlit as st
import getpass
import random

# Use session_state to store user data
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ''

st.set_page_config(page_title="MyBank App", page_icon="🏦", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton>button { background-color: #007BFF; color: white; border-radius: 5px; height: 3em; width: 100%; font-weight: bold; }
    .stTextInput>div>input { border-radius: 5px; }
    .stTitle { color: #003366; }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def create_account(name, acc_no, pin):
    if acc_no in st.session_state.accounts:
        return False
    st.session_state.accounts[acc_no] = {
        'name': name,
        'pin': pin,
        'balance': 0
    }
    return True

def authenticate(acc_no, pin):
    acc = st.session_state.accounts.get(acc_no)
    if acc and acc['pin'] == pin:
        st.session_state.logged_in = True
        st.session_state.current_user = acc_no
        return True
    return False

def get_user():
    return st.session_state.accounts[st.session_state.current_user]

def home():
    st.title("Welcome to MyBank 🏦")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account"):
            st.session_state.page = 'create'
    with col2:
        if st.button("Login"):
            st.session_state.page = 'login'

def create_page():
    st.title("Create Account")
    name = st.text_input("Full Name")
    acc_no = st.text_input("Set Account Number")
    pin = st.text_input("Set 4-digit PIN", type="password")
    if st.button("Create"):
        if len(pin) == 4 and pin.isdigit():
            if create_account(name, acc_no, pin):
                st.success("Account created! Redirecting to Login...")
                st.session_state.page = 'login'
            else:
                st.error("Account number already exists.")
        else:
            st.warning("PIN must be 4 digits.")

def login_page():
    st.title("Login")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("4-digit PIN", type="password")
    if st.button("Login"):
        if authenticate(acc_no, pin):
            st.success("Login successful!")
        else:
            st.error("Invalid account number or PIN.")

def dashboard():
    st.title(f"Hello, {get_user()['name']} 👋")
    choice = st.sidebar.radio("Menu", ["Deposit", "Withdraw", "Check Balance", "Logout"])

    if choice == "Deposit":
        st.subheader("Deposit Money")
        amt = st.number_input("Enter amount to deposit", min_value=1, step=1)
        pin = st.text_input("Enter PIN to confirm", type="password")
        if st.button("Confirm Deposit"):
            if pin == get_user()['pin']:
                get_user()['balance'] += amt
                st.success(f"₹{amt} deposited successfully!")
            else:
                st.error("Incorrect PIN")

    elif choice == "Withdraw":
        st.subheader("Withdraw Money")
        amt = st.number_input("Enter amount to withdraw", min_value=1, step=1)
        upi = st.text_input("Enter your UPI ID")
        pin = st.text_input("Enter PIN to confirm", type="password")
        if st.button("Confirm Withdrawal"):
            user = get_user()
            if pin == user['pin']:
                if amt <= user['balance']:
                    user['balance'] -= amt
                    st.success(f"₹{amt} will be transferred to {upi}")
                else:
                    st.error("Insufficient balance")
            else:
                st.error("Incorrect PIN")

    elif choice == "Check Balance":
        st.subheader("Account Balance")
        pin = st.text_input("Enter PIN to view balance", type="password")
        if st.button("Show Balance"):
            if pin == get_user()['pin']:
                st.info(f"Your current balance is ₹{get_user()['balance']}")
            else:
                st.error("Incorrect PIN")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_user = ''
        st.success("You have been logged out.")

# Control page flow
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.logged_in:
    dashboard()
elif st.session_state.page == 'home':
    home()
elif st.session_state.page == 'create':
    create_page()
elif st.session_state.page == 'login':
    login_page()
