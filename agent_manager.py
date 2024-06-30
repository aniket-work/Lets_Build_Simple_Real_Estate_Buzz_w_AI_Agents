from langchain_groq.chat_models import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from config import Config
from database_manager import DatabaseManager
import re


def format_price(price):
    try:
        price_float = float(price.replace(',', ''))
        return f"${price_float:,.2f}"
    except ValueError:
        return price


def clean_text(text):
    clean = re.sub(r'[^\x00-\x7F]+', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


class AgentManager:
    def __init__(self):
        self.model = ChatGroq(model_name=Config.MODEL_NAME, api_key=Config.GROQ_API_KEY)
        self.db_manager = DatabaseManager()

    def query(self, question, table_name):
        agent_executor = create_sql_agent(
            self.model,
            db=self.db_manager.get_sql_database(),
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            table_names=[table_name]
        )

        response = agent_executor.invoke(question)['output']
        response = clean_text(response)

        price_match = re.search(r'(\d+) bedroom home is approximately (\d+)', response)
        if price_match:
            bedrooms = price_match.group(1)
            price = price_match.group(2)
            formatted_price = format_price(price)
            return f"Based on our analysis, the typical price for a {bedrooms}-bedroom home is approximately {formatted_price}."
        else:
            return f"Based on our analysis: {response}"