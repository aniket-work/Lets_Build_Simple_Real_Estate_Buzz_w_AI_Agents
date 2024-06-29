import streamlit as st
from agent_manager import AgentManager
from config import Config

def main():
    st.set_page_config(page_title="RealEstate Insights", page_icon="🏠", layout="wide")

    st.title("🏡 RealEstate Insights: Your Housing Consultancy Expert")

    st.markdown("""
    Welcome to RealEstate Insights! We're here to provide you with expert housing consultancy.
    Ask us anything about housing prices, features, and trends in our database.
    """)

    agent_manager = AgentManager()

    user_question = st.text_input("What would you like to know about housing?", 
                                  "What is the typical price for a 3 bedroom home?")

    if st.button("Get Insights"):
        with st.spinner("Analyzing our vast real estate database..."):
            response = agent_manager.query(user_question)
            st.success("Here's what we found:")
            st.write(response)

    st.markdown("---")
    st.markdown("### Sample Questions")
    st.markdown("""
    - What is the average price of houses with 4 bedrooms and 3 bathrooms?
    - For a budget of $500,000, what kind of houses are available?
    - What's the correlation between house size and price in our database?
    - How does the presence of air conditioning affect house prices?
    """)

if __name__ == "__main__":
    main()