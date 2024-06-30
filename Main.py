import streamlit as st
from agent_manager import AgentManager
from database_manager import DatabaseManager
import plotly.express as px

def load_css():
    st.markdown("""
        <style>
        .main-header {color: #1E3A8A; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 30px;}
        .sub-header {font-size: 28px; font-weight: bold; color: #1E3A8A; margin-top: 30px; margin-bottom: 20px;}
        .description {font-size: 18px; color: #4B5563; margin-bottom: 20px;}
        .feature-box {background-color: #F3F4F6; border-radius: 10px; padding: 20px; margin-bottom: 20px;}
        .feature-title {font-size: 20px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
        .feature-desc {font-size: 16px; color: #4B5563;}
        </style>
    """, unsafe_allow_html=True)

def create_city_price_comparison(db_manager):
    query = """
    SELECT 'New York' as city, AVG(price) as avg_price FROM new_york_housing
    UNION ALL
    SELECT 'Los Angeles' as city, AVG(price) as avg_price FROM los_angeles_housing
    UNION ALL
    SELECT 'Chicago' as city, AVG(price) as avg_price FROM chicago_housing
    UNION ALL
    SELECT 'Houston' as city, AVG(price) as avg_price FROM houston_housing
    """
    df = db_manager.get_data(query)
    fig = px.bar(df, x='city', y='avg_price', title='Average Housing Prices by City')
    fig.update_layout(xaxis_title='City', yaxis_title='Average Price')
    return fig

def main():
    st.set_page_config(page_title="NestQuest AI", page_icon="🏠", layout="wide")
    load_css()

    st.markdown('<h1 class="main-header">🏡 NestQuest AI: Your Intelligent Housing Consultancy</h1>', unsafe_allow_html=True)

    db_manager = DatabaseManager()
    agent_manager = AgentManager()

    st.markdown('<p class="description">Welcome to NestQuest AI! We leverage advanced AI and comprehensive market data to provide you with expert housing consultancy across major US cities.</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="sub-header">Select a City</h2>', unsafe_allow_html=True)
    city = st.selectbox("Choose a city to analyze:", ["New York", "Los Angeles", "Chicago", "Houston"])

    city_table_map = {
        "New York": "new_york_housing",
        "Los Angeles": "los_angeles_housing",
        "Chicago": "chicago_housing",
        "Houston": "houston_housing"
    }

    selected_table = city_table_map[city]

    st.markdown('<h2 class="sub-header">Ask Our AI Consultant</h2>', unsafe_allow_html=True)
    user_question = st.text_input(f"What would you like to know about housing in {city}?",
                                  f"What is the typical price for a 2 bedroom home in {city}?")

    if st.button("Get Insights"):
        with st.spinner(f"Analyzing our {city} real estate database..."):
            response = agent_manager.query(user_question, selected_table)
            st.success("Here's what we found:")
            st.write(response)

    st.markdown('<h2 class="sub-header">Market Insights</h2>', unsafe_allow_html=True)
    st.plotly_chart(create_city_price_comparison(db_manager), use_container_width=True)

    st.markdown('<h2 class="sub-header">Our Services</h2>', unsafe_allow_html=True)
    services = [
        ("🔍 City-Specific Analysis", f"Deep dive into {city}'s housing market."),
        ("💰 Investment Advisory", f"Personalized advice on real estate investments in {city}."),
        ("🏘️ Property Valuation", f"Accurate estimations of property values in {city}."),
        ("📊 Market Trends", f"Stay updated with the latest trends in {city}'s housing market."),
    ]
    for title, desc in services:
        st.markdown(f"""
        <div class="feature-box">
            <h3 class="feature-title">{title}</h3>
            <p class="feature-desc">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h2 class="sub-header">Whats Trending</h2>', unsafe_allow_html=True)
    sample_questions = [
        f"What is the average price of houses in {city}?",
        f"What's the price range for 3-bedroom homes in {city}?",
        f"How does the price per square foot vary in different areas of {city}?",
        f"What's the most expensive zip code in {city}?",
        f"How many 4-bedroom houses are available in {city}?",
    ]
    for question in sample_questions:
        st.markdown(f"- {question}")

    st.markdown('<h2 class="sub-header">Contact Us</h2>', unsafe_allow_html=True)
    st.markdown(f"Have more questions about housing in {city}? Our team of expert real estate consultants is here to help!")
    st.button("Schedule a Consultation")

if __name__ == "__main__":
    main()