import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY not found in .env")
    exit()

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key
    )

    response = llm.invoke([
        HumanMessage(content="Say: API key works")
    ])

    print("API key is working")
    print("Response:", response.content)

except Exception as e:
    print("API key not working")
    print("Error:", e)