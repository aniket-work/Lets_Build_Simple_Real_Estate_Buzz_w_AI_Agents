import streamlit as st
from agent_manager import AgentManager
from csv_reader import CSVReader
from database_manager import DatabaseManager
from config import Config
import plotly.express as px
import plotly.graph_objects as go

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

def create_price_by_bedrooms_plot(db_manager):
    df = db_manager.get_data("SELECT bedrooms, AVG(price) as avg_price FROM housing GROUP BY bedrooms")
    fig = px.bar(df, x='bedrooms', y='avg_price', title='Average Price by Number of Bedrooms')
    fig.update_layout(xaxis_title='Number of Bedrooms', yaxis_title='Average Price')
    return fig

def create_price_range_by_area_plot(db_manager):
    df = db_manager.get_data("SELECT area, price FROM housing")
    fig = px.scatter(df, x='area', y='price', title='Price Range by Area')
    fig.update_layout(xaxis_title='Area (sq ft)', yaxis_title='Price')
    return fig

def create_demand_by_parking_plot(db_manager):
    df = db_manager.get_data("SELECT parking, COUNT(*) as count FROM housing GROUP BY parking")
    fig = px.pie(df, values='count', names='parking', title='Demand by Number of Parking Spaces')
    return fig

def create_price_by_stories_plot(db_manager):
    df = db_manager.get_data("SELECT stories, AVG(price) as avg_price FROM housing GROUP BY stories")
    fig = px.line(df, x='stories', y='avg_price', title='Average Price by Number of Stories')
    fig.update_layout(xaxis_title='Number of Stories', yaxis_title='Average Price')
    return fig

def main():
    st.set_page_config(page_title="RealEstate Insights", page_icon="🏠", layout="wide")
    load_css()

    st.markdown('<h1 class="main-header">🏡 NestQuest AI: Your Intelligent Housing Consultancy</h1>', unsafe_allow_html=True)

    db_manager = DatabaseManager(Config.DB_FOLDER, Config.DB_NAME)

    agent_manager = AgentManager()

    st.markdown('<p class="description">Welcome to NestQuest AI! We leverage advanced AI and comprehensive market data to provide you with expert housing consultancy. Explore market trends, get personalized recommendations, and make informed decisions about your real estate investments.</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="sub-header">Ask Our AI Consultant</h2>', unsafe_allow_html=True)
    user_question = st.text_input("What would you like to know about housing?",
                                  "What is the typical price for a 3 bedroom home?")

    if st.button("Get Insights"):
        with st.spinner("Analyzing our vast real estate database..."):
            response = agent_manager.query(user_question)
            st.success("Here's what we found:")
            st.write(response)

    st.markdown('<h2 class="sub-header">Market Insights</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_price_by_bedrooms_plot(db_manager), use_container_width=True)
        st.plotly_chart(create_demand_by_parking_plot(db_manager), use_container_width=True)

    with col2:
        st.plotly_chart(create_price_range_by_area_plot(db_manager), use_container_width=True)
        st.plotly_chart(create_price_by_stories_plot(db_manager), use_container_width=True)

    st.markdown('<h2 class="sub-header">Our Services</h2>', unsafe_allow_html=True)
    services = [
        ("🔍 Market Analysis", "Get in-depth analysis of housing market trends and predictions."),
        ("💰 Investment Advisory", "Receive personalized advice on real estate investments."),
        ("🏘️ Property Valuation", "Accurate estimations of property values based on multiple factors."),
        ("📊 Comparative Studies", "Compare different properties and neighborhoods."),
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
        "What is the average price of houses with 4 bedrooms and 3 bathrooms?",
        "For a budget of $500,000, what kind of houses are available?",
        "What's the correlation between house size and price ?",
        "How does the presence of air conditioning affect house prices?",
        "Which areas have the highest appreciation rates for properties?",
    ]
    for question in sample_questions:
        st.markdown(f"- {question}")

    st.markdown('<h2 class="sub-header">Contact Us</h2>', unsafe_allow_html=True)
    st.markdown("Have more questions? Our team of expert real estate consultants is here to help!")
    st.button("Schedule a Consultation")

if __name__ == "__main__":
    main()