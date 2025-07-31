import streamlit as st
import json
import os

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file)

def create_account(name, acc_no, pin):
    accounts = load_accounts()
    if acc_no in accounts:
        return False, "🚫 Account already exists."
    accounts[acc_no] = {"name": name, "pin": pin, "balance": 0}
    save_accounts(accounts)
    return True, "✅ Account created successfully!"

def authenticate(acc_no, pin):
    accounts = load_accounts()
    user = accounts.get(acc_no)
    if user and user["pin"] == pin:
        return True, user["name"]
    return False, None

def deposit(acc_no, amount):
    accounts = load_accounts()
    accounts[acc_no]["balance"] += amount
    save_accounts(accounts)
    return accounts[acc_no]["balance"]

def withdraw(acc_no, amount):
    accounts = load_accounts()
    if accounts[acc_no]["balance"] >= amount:
        accounts[acc_no]["balance"] -= amount
        save_accounts(accounts)
        return True, accounts[acc_no]["balance"]
    return False, accounts[acc_no]["balance"]

def get_balance(acc_no):
    return load_accounts()[acc_no]["balance"]

def home():
    st.title("🏦 Welcome to MyBank")
    choice = st.selectbox("Choose an option", ["Select", "Create Account", "Login"])

    if choice == "Create Account":
        name = st.text_input("👤 Your Name")
        acc_no = st.text_input("🆔 Create Account Number")
        pin = st.text_input("🔑 4-Digit PIN", type="password")

        if st.button("Create Account"):
            if not name or not acc_no or not pin:
                st.error("Please fill all fields.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be a 4-digit number.")
            else:
                success, msg = create_account(name, acc_no, pin)
                if success:
                    st.success(msg)
                    st.session_state.page = "Login"
                else:
                    st.error(msg)

    elif choice == "Login":
        login()

def login():
    st.subheader("🔐 Login to MyBank")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        success, name = authenticate(acc_no, pin)
        if success:
            st.session_state.logged_in = True
            st.session_state.acc_no = acc_no
            st.session_state.name = name
            st.session_state.page = "Dashboard"
        else:
            st.error("Invalid credentials.")

def dashboard():
    st.title(f"👋 Welcome, {st.session_state.name}")
    action = st.selectbox("Select action", ["Select", "Deposit", "Withdraw", "Check Balance", "Logout"])

    if action == "Deposit":
        amt = st.number_input("Enter amount", min_value=1)
        pin = st.text_input("Confirm PIN", type="password", key="dep_pin")
        if st.button("Deposit"):
            if authenticate(st.session_state.acc_no, pin)[0]:
                new_bal = deposit(st.session_state.acc_no, amt)
                st.success(f"₹{amt} deposited. New Balance: ₹{new_bal}")
            else:
                st.error("Wrong PIN")

    elif action == "Withdraw":
        amt = st.number_input("Enter amount", min_value=1)
        pin = st.text_input("Confirm PIN", type="password", key="with_pin")
        if st.button("Withdraw"):
            if authenticate(st.session_state.acc_no, pin)[0]:
                ok, new_bal = withdraw(st.session_state.acc_no, amt)
                if ok:
                    st.success(f"₹{amt} withdrawn. New Balance: ₹{new_bal}")
                else:
                    st.error("Insufficient balance")
            else:
                st.error("Wrong PIN")

    elif action == "Check Balance":
        pin = st.text_input("Enter PIN", type="password", key="bal_pin")
        if st.button("Show Balance"):
            if authenticate(st.session_state.acc_no, pin)[0]:
                bal = get_balance(st.session_state.acc_no)
                st.info(f"💰 Current Balance: ₹{bal}")
            else:
                st.error("Wrong PIN")

    elif action == "Logout":
        st.session_state.clear()
        st.success("✅ Logged out")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if st.session_state.page == "Home":
        home()
    elif st.session_state.page == "Login":
        login()
    elif st.session_state.page == "Dashboard" and st.session_state.get("logged_in"):
        dashboard()
    else:
        st.session_state.page = "Home"

main()
