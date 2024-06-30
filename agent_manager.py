from langchain_groq.chat_models import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from config import Config
from csv_reader import CSVReader
from database_manager import DatabaseManager
import re


def format_price(price):
    try:
        price_float = float(price.replace(',', ''))
        return f"${price_float:,.2f}"
    except ValueError:
        return price


def clean_text(text):
    # Remove non-ASCII characters
    clean = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove extra spaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


class AgentManager:
    def __init__(self):
        self.model = ChatGroq(model_name=Config.MODEL_NAME, api_key=Config.GROQ_API_KEY)
        csv_reader = CSVReader(Config.CSV_FILE_PATH)
        data = csv_reader.read_csv()
        self.db_manager = DatabaseManager(Config.DB_FOLDER, Config.DB_NAME)
        self.agent_executor = create_sql_agent(
            self.model,
            db=self.db_manager.get_db(),
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def query(self, question):
        response = self.agent_executor.invoke(question)['output']

        # Clean the response
        response = clean_text(response)

        # Extract the relevant information
        price_match = re.search(r'(\d+) bedroom home is approximately (\d+)', response)
        if price_match:
            bedrooms = price_match.group(1)
            price = price_match.group(2)
            formatted_price = format_price(price)
            return f"Based on our analysis, the typical price for a {bedrooms}-bedroom home is approximately {formatted_price}."
        else:
            # If we can't extract the information in the expected format, return the cleaned response
            return f"Based on our analysis: {response}"