import streamlit as st
import getpass

# Fake getpass workaround for streamlit
def get_pin_input(label):
    return st.text_input(label, type="password", max_chars=4)

accounts = {}

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

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

st.title("🏦 Simple Bank App")

menu = st.sidebar.selectbox("Menu", ["Home", "Create Account", "Login", "Logout"])

# CREATE ACCOUNT
if menu == "Create Account":
    st.header("📝 Create New Account")
    name = st.text_input("Enter your name")
    acc_no = st.text_input("Enter unique account number")
    pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

    if st.button("Create"):
        if len(pin) == 4 and pin.isdigit() and acc_no not in accounts:
            accounts[acc_no] = BankAccount(name, acc_no, pin)
            st.success("✅ Account created!")
        else:
            st.error("❌ Invalid PIN or Account Number already exists.")

# LOGIN
elif menu == "Login":
    st.header("🔐 Login")
    acc_no = st.text_input("Enter your account number")
    pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4)

    if st.button("Login"):
        if acc_no in accounts and accounts[acc_no].check_pin(pin):
            st.session_state.logged_in = True
            st.session_state.current_user = accounts[acc_no]
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid account number or PIN.")

# LOGOUT
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.info("🔓 Logged out.")

# LOGGED IN MENU
if st.session_state.logged_in:
    user = st.session_state.current_user
    st.header(f"Welcome, {user.name} 👋")
    
    option = st.radio("Choose an action", ["Deposit", "Withdraw", "Check Balance"])
    pin_check = get_pin_input("Confirm your 4-digit PIN")

    if user.check_pin(pin_check):
        if option == "Deposit":
            amount = st.number_input("Enter deposit amount", min_value=1.0)
            if st.button("Deposit"):
                user.deposit(amount)
                st.success(f"✅ ₹{amount} deposited.")

        elif option == "Withdraw":
            amount = st.number_input("Enter withdraw amount", min_value=1.0)
            if st.button("Withdraw"):
                if amount <= user.balance:
                    user.withdraw(amount)
                    st.success(f"✅ ₹{amount} withdrawn.")
                else:
                    st.error("❌ Not enough balance.")

        elif option == "Check Balance":
            st.info(f"💰 Your current balance: ₹{user.balance}")
    elif pin_check:
        st.warning("❌ Wrong PIN.")
