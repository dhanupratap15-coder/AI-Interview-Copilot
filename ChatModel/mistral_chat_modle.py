from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
import os
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key
)