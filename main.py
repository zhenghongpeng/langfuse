from langfuse import observe
from langfuse.openai import openai # OpenAI integration
from dotenv import load_dotenv
import os
import base64
load_dotenv(".env.local")


openai_api_key = os.getenv("OPENAI_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")


openai.api_key = openai_api_key

# 🇪🇺 EU region
# LANGFUSE_HOST="https://cloud.langfuse.com"
# 🇺🇸 US region
LANGFUSE_HOST=os.getenv("LANGFUSE_HOST")


LANGFUSE_BASEURL=os.getenv("LANGFUSE_HOST")
# LANGFUSE_HOST="http://127.0.0.1:3000"

print(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST)

from langfuse import get_client
 
langfuse = get_client()
 
# Create a span without a context manager
span = langfuse.start_span(name="user-request")
 
# Your processing logic here
span.update(output="Request processed")
 
# Child spans must be created using the parent span object
nested_span = span.start_span(name="nested-span")
nested_span.update(output="Nested span output")
 
# Important: Manually end the span
nested_span.end()
 
# Important: Manually end the parent span
span.end()
 
 
# Flush events in short-lived applications
langfuse.flush()

# from langfuse.callback import CallbackHandler
from langfuse.langchain import CallbackHandler  # Correct import if CallbackHandler exists in the main langfuse module

langfuse_handler = CallbackHandler(
    public_key=LANGFUSE_PUBLIC_KEY,
    # secret_key=LANGFUSE_SECRET_KEY,
    # host="http://localhost:3000"
)

# <Your Langchain code here>
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI chat model
llm = ChatOpenAI(
    temperature=0.7,  # Controls randomness
    openai_api_key=openai_api_key,
    model="gpt-3.5-turbo"  # Specify the model
)

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    You are a helpful assistant. Use the conversation history and the user's input to provide a thoughtful response.

    Conversation History:
    {history}

    User Input:
    {input}

    Response:
    """
)

# Initialize memory to store conversation history
memory = ConversationBufferMemory()

# Create the chain
conversation_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# Start a conversation
# print("Assistant: Hello! How can I help you today?")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Assistant: Goodbye!")
#         break
#     response = conversation_chain.run(input=user_input)
#     print(f"Assistant: {response}")
 
# Add handler to run/invoke/call/chat
conversation_chain.invoke({"input": "who is president of the united states?"}, config={"callbacks": [langfuse_handler]})