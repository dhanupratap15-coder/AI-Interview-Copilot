from ChatModel import mistral_chat_modle
from SelectRollBasicOfResume import resumeroll
from prompt_roll import prompt

from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()

llm = mistral_chat_modle.llm
from prompt_roll import prompt
try:
    chain = prompt | llm | parser

    response_roll = chain.invoke({
        "resume": resumeroll.resume
    })
except KeyError as e:
    print(f"Missing input variable: {e}")

except AttributeError as e:
    print(f"Attribute Error: {e}")
    print("Check if 'resumeroll.resume' exists.")

except Exception as e:
    print(f"An error occurred: {e}")
    