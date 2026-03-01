from config import GEMINI_API_KEY
try:
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )
except ImportError:
    llm = None

# Simple intent detection

def detect_intent(query):
    
    if llm is not None:
        prompt = f"""
Classify the intent:

lead_capture -> greeting, introduction, giving name/designation
policy_query -> asking HR policy question

Query: {query}

Return ONLY:
lead_capture
OR
policy_query
"""
        response = llm.invoke(prompt)
        intent = response.content.strip().lower()
        if "lead_capture" in intent:
            return "lead_capture"
        return "policy_query"

    # fallback simple heuristic based on keywords
    low = query.lower()
    if any(word in low for word in ["my name", "i am", "i'm", "name is", "hello", "hi"]):
        return "lead_capture"
    return "policy_query"

