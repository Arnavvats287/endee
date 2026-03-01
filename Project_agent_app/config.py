import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ENDEE_URL = "http://localhost:8080"  
INDEX_NAME = "hr_policies"
EMBEDDING_DIM = 384