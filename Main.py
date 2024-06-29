
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables and set constants
load_dotenv()
DATABASE_FOLDER = 'database'
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize GroqLLM
model = ChatGroq(model_name="llama3-70b-8192", api_key=GROQ_API_KEY)