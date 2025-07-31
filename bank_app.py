import streamlit as st
import getpass

st.set_page_config(page_title="MyBank App", page_icon="🏦", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            width: 100%;
            padding: 0.75em;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Session state setup
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def home():
    st.title("🏦 Welcome to MyBank")
    st.subheader("Your Digital Banking Partner")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.page = 'login'
    with col2:
        if st.button("📝 Create Account"):
            st.session_state.page = 'create'

def create_account():
    st.title("📝 Create Account")
    name = st.text_input("Full Name")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Set 4-digit PIN", type="password")

    if st.button("Create"):
        if len(pin) == 4 and pin.isdigit() and name and acc_no:
            if acc_no in st.session_state.accounts:
                st.error("Account number already exists!")
            else:
                st.session_state.accounts[acc_no] = {
                    'name': name,
                    'pin': pin,
                    'balance': 0
                }
                st.success("Account created successfully! Please log in.")
                st.session_state.page = 'login'
        else:
            st.error("Fill all details and use a 4-digit PIN.")

def login():
    st.title("🔐 Login")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Login"):
        user = st.session_state.accounts.get(acc_no)
        if user and user['pin'] == pin:
            st.success(f"Welcome back, {user['name']}!")
            st.session_state.current_user = acc_no
            st.session_state.page = 'dashboard'
        else:
            st.error("Invalid account number or PIN")

def dashboard():
    user = st.session_state.accounts[st.session_state.current_user]
    st.title(f"🏠 Welcome {user['name']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 Deposit"):
            st.session_state.page = 'deposit'
    with col2:
        if st.button("🏧 Withdraw"):
            st.session_state.page = 'withdraw'

    col3, col4 = st.columns(2)
    with col3:
        if st.button("📊 Check Balance"):
            st.session_state.page = 'balance'
    with col4:
        if st.button("🚪 Logout"):
            st.session_state.current_user = None
            st.session_state.page = 'home'

def deposit():
    st.title("💰 Deposit Money")
    pin = st.text_input("Enter your 4-digit PIN", type="password")
    amount = st.number_input("Enter amount to deposit", min_value=1)

    if st.button("Confirm Deposit"):
        user = st.session_state.accounts[st.session_state.current_user]
        if user['pin'] == pin:
            user['balance'] += amount
            st.success(f"₹{amount} deposited successfully!")
            st.session_state.page = 'dashboard'
        else:
            st.error("Incorrect PIN")

def withdraw():
    st.title("🏧 Withdraw Money")
    pin = st.text_input("Enter your 4-digit PIN", type="password")
    amount = st.number_input("Enter amount to withdraw", min_value=1)
    upi = st.text_input("Enter UPI ID to receive funds")

    if st.button("Confirm Withdrawal"):
        user = st.session_state.accounts[st.session_state.current_user]
        if user['pin'] == pin:
            if user['balance'] >= amount:
                user['balance'] -= amount
                st.success(f"₹{amount} will be sent to {upi}")
                st.session_state.page = 'dashboard'
            else:
                st.error("Insufficient balance")
        else:
            st.error("Incorrect PIN")

def check_balance():
    st.title("📊 Account Balance")
    pin = st.text_input("Enter your 4-digit PIN", type="password")

    if st.button("Show Balance"):
        user = st.session_state.accounts[st.session_state.current_user]
        if user['pin'] == pin:
            st.info(f"Your current balance is ₹{user['balance']}")
        else:
            st.error("Incorrect PIN")
        st.session_state.page = 'dashboard'

# Routing
if st.session_state.page == 'home':
    home()
elif st.session_state.page == 'create':
    create_account()
elif st.session_state.page == 'login':
    login()
elif st.session_state.page == 'dashboard':
    dashboard()
elif st.session_state.page == 'deposit':
    deposit()
elif st.session_state.page == 'withdraw':
    withdraw()
elif st.session_state.page == 'balance':
    check_balance()
