import streamlit as st

# Helper: Hideable PIN input
def get_pin_input(label):
    return st.text_input(label, type="password", max_chars=4)

# ========== Persistent State ==========
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'page' not in st.session_state:
    st.session_state.page = "home"

# ========== BankAccount Class ==========
class BankAccount:
    def __init__(self, name, acc_no, pin, balance=0):
        self.name = name
        self.acc_no = acc_no
        self.pin = pin
        self.balance = balance

    def check_pin(self, entered):
        return entered == self.pin

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

# ========== Page: Home ==========
def home():
    st.title("🏦 Simple Bank App")
    st.write("Select an option:")

    if st.button("Create Account"):
        st.session_state.page = "create"

    if st.button("Login"):
        st.session_state.page = "login"

# ========== Page: Create Account ==========
def create_account():
    st.title("📝 Create New Account")

    name = st.text_input("Enter your name")
    acc_no = st.text_input("Choose a unique account number")
    pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

    if st.button("Create"):
        if len(pin) == 4 and pin.isdigit() and acc_no not in st.session_state.accounts:
            account = BankAccount(name, acc_no, pin)
            st.session_state.accounts[acc_no] = account
            st.success("✅ Account created! Please login now.")
            st.session_state.page = "login"
        else:
            st.error("❌ Invalid PIN or account number already exists.")

# ========== Page: Login ==========
def login():
    st.title("🔐 Login")

    acc_no = st.text_input("Enter your account number")
    pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4)

    if st.button("Login"):
        accounts = st.session_state.accounts
        if acc_no in accounts and accounts[acc_no].check_pin(pin):
            st.session_state.logged_in = True
            st.session_state.current_user = accounts[acc_no]
            st.session_state.page = "dashboard"
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid account number or PIN.")

# ========== Page: Dashboard ==========
def dashboard():
    user = st.session_state.current_user
    st.title(f"👋 Welcome, {user.name}")

    action = st.radio("Choose an option:", ["Deposit", "Withdraw", "Check Balance", "Logout"])

    if action == "Deposit":
        pin = get_pin_input("Enter your PIN to continue")
        if user.check_pin(pin):
            amount = st.number_input("Enter amount to deposit", min_value=1.0)
            if st.button("Deposit"):
                user.deposit(amount)
                st.success(f"✅ ₹{amount} deposited.")
        elif pin:
            st.error("❌ Wrong PIN")

    elif action == "Withdraw":
        pin = get_pin_input("Enter your PIN to continue")
        if user.check_pin(pin):
            amount = st.number_input("Enter amount to withdraw", min_value=1.0)
            if st.button("Withdraw"):
                if amount <= user.balance:
                    user.withdraw(amount)
                    st.success(f"✅ ₹{amount} withdrawn.")
                else:
                    st.error("❌ Not enough balance.")
        elif pin:
            st.error("❌ Wrong PIN")

    elif action == "Check Balance":
        pin = get_pin_input("Enter your PIN to continue")
        if user.check_pin(pin):
            st.info(f"💰 Your current balance is: ₹{user.balance}")
        elif pin:
            st.error("❌ Wrong PIN")

    elif action == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.page = "home"
        st.success("🔒 Logged out.")

# ========== Page Routing ==========
if st.session_state.page == "home":
    home()
elif st.session_state.page == "create":
    create_account()
elif st.session_state.page == "login":
    login()
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    dashboard()
else:
    st.session_state.page = "home"
