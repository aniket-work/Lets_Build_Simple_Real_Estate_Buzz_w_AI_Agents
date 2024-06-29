from langchain_groq.chat_models import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from config import Config
from csv_reader import CSVReader
from database_manager import DatabaseManager

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
        return self.agent_executor.invoke(question)['output']