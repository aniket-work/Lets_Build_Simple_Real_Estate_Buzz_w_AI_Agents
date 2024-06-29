import streamlit as st

def display_error(message):
    st.error(f"An error occurred: {message}")

def format_currency(amount):
    return f"${amount:,.2f}"