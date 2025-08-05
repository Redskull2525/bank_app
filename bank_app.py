import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'prev_page' not in st.session_state:
    st.session_state.prev_page = None
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def go_to(page_name):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page_name

def back_button():
    if st.session_state.page != 'home' and st.session_state.prev_page:
        if st.button("🔙 Back"):
            go_to(st.session_state.prev_page)

# Page Functions
def home():
    st.title("🏦 Welcome to MyBank")
    st.subheader("Your Digital Banking Partner")
    if st.button("Create Account"):
        go_to('create')
    if st.button("Login"):
        go_to('login')

def create_account():
    st.title("📝 Create Account")
    name = st.text_input("Enter your name")
    acc_no = st.text_input("Enter account number")
    pin = st.text_input("Enter 4-digit PIN", type="password")
    balance = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create"):
        if name and acc_no and len(pin) == 4:
            st.session_state.accounts[acc_no] = {
                'name': name,
                'pin': pin,
                'balance': balance
            }
            st.success("Account created successfully!")
            go_to('login')
        else:
            st.error("Fill all fields correctly with a 4-digit PIN.")

def login():
    st.title("🔐 Login")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        acc = st.session_state.accounts.get(acc_no)
        if acc and acc['pin'] == pin:
            st.session_state.current_user = acc_no
            st.success("Login Successful!")
            go_to('dashboard')
        else:
            st.error("Invalid account number or PIN")

def dashboard():
    user = st.session_state.accounts.get(st.session_state.current_user)
    st.title(f"Welcome, {user['name']} 👋")
    st.write(f"Your balance: ₹{user['balance']}")

    if st.button("Deposit"):
        go_to('deposit')
    if st.button("Withdraw"):
        go_to('withdraw')
    if st.button("Check Balance"):
        go_to('check_balance')
    if st.button("Logout"):
        st.session_state.current_user = None
        go_to('home')

def deposit():
    st.title("💰 Deposit Money")
    amount = st.number_input("Enter amount", min_value=1)
    pin = st.text_input("Enter PIN", type="password")

    user = st.session_state.accounts[st.session_state.current_user]

    if st.button("Confirm Deposit"):
        if pin == user['pin']:
            user['balance'] += amount
            st.success(f"Deposited ₹{amount}")
            go_to('dashboard')
        else:
            st.error("Incorrect PIN")
    back_button()

def withdraw():
    st.title("🏧 Withdraw Money")
    amount = st.number_input("Enter amount", min_value=1)
    pin = st.text_input("Enter PIN", type="password")

    user = st.session_state.accounts[st.session_state.current_user]

    if st.button("Confirm Withdrawal"):
        if pin == user['pin']:
            if user['balance'] >= amount:
                user['balance'] -= amount
                st.success(f"Withdrawn ₹{amount}")
                go_to('dashboard')
            else:
                st.error("Insufficient balance")
        else:
            st.error("Incorrect PIN")
    back_button()

def check_balance():
    st.title("📊 Check Balance")
    pin = st.text_input("Enter PIN", type="password")

    user = st.session_state.accounts[st.session_state.current_user]

    if st.button("Show Balance"):
        if pin == user['pin']:
            st.info(f"Your current balance is ₹{user['balance']}")
            go_to('dashboard')
        else:
            st.error("Incorrect PIN")
    back_button()

# Routing
pages = {
    'home': home,
    'create': create_account,
    'login': login,
    'dashboard': dashboard,
    'deposit': deposit,
    'withdraw': withdraw,
    'check_balance': check_balance
}

pages[st.session_state.page]()
