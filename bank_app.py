import streamlit as st

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
if 'prev_page' not in st.session_state:
    st.session_state.prev_page = None

def go_to(page_name):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page_name

def back_button():
    if st.button("🔙 Back"):
        st.session_state.page = st.session_state.prev_page

def home():
    st.title("🏦 Welcome to MyBank")
    st.subheader("Your Digital Banking Partner")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            go_to('login')
    with col2:
        if st.button("📝 Create Account"):
            go_to('create')

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
                go_to('login')
        else:
            st.error("Fill all details and use a 4-digit PIN.")
    back_button()

def login():
    st.title("🔐 Login")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Login"):
        user = st.session_state.accounts.get(acc_no)
        if user and user['pin'] == pin:
            st.success(f"Welcome back, {user['name']}!")
            st.session_state.current_user = acc_no
            go_to('dashboard')
        else:
            st.error("Invalid account number or PIN")
    back_button()

def dashboard():
    user = st.session_state.accounts[st.session_state.current_user]
    st.title(f"🏠 Welcome {user['name']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 Deposit"):
            go_to('deposit')
    with col2:
        if st.button("🏧 Withdraw"):
            go_to('withdraw')

    col3, col4 = st.columns(2)
    with col3:
        if st.button("📊 Check Balance"):
            go_to('balance')
    with col4:
        if st.button("🚪 Logout"):
            st.session_state.current_user = None
            go_to('home')

def deposit():
    st.title("💰 Deposit Money")
    pin = st.text_input("Enter your 4-digit PIN", type="password")
    amount = st.number_input("Enter amount to deposit", min_value=1)

    if st.button("Confirm Deposit"):
        user = st.session_state.accounts[st.session_state.current_user]
        if user['pin'] == pin:
            user['balance'] += amount
            st.success(f"₹{amount} deposited successfully!")
            go_to('dashboard')
        else:
            st.error("Incorrect PIN")
    back_button()

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
                go_to('dashboard')
            else:
                st.error("Insufficient balance")
        else:
            st.error("Incorrect PIN")
    back_button()

def check_balance():
    st.title("📊 Account Balance")
    pin = st.text_input("Enter your 4-digit PIN", type="password")

    if st.button("Show Balance"):
        user = st.session_state.accounts[st.session_state.current_user]
        if user['pin'] == pin:
            st.info(f"Your current balance is ₹{user['balance']}")
            go_to('dashboard')
        else:
            st.error("Incorrect PIN")
    back_button()

# Routing
page = st.session_state.page

if page == 'home':
    home()
elif page == 'create':
    create_account()
elif page == 'login':
    login()
elif page == 'dashboard':
    dashboard()
elif page == 'deposit':
    deposit()
elif page == 'withdraw':
    withdraw()
elif page == 'balance':
    check_balance()
