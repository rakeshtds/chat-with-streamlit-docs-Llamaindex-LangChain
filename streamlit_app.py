import streamlit as st



import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

st.set_page_config(page_title="Chat easily with Lenders Data, powered by Sylphia Consulting(SCi)", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Chat with the AssetDirect docs, powered by Sylphia Consulting(SCi) ")
    
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Asset Direct Lenders!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
        # index = VectorStoreIndex.from_documents(docs)
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-turbo", temperature=0, system_prompt="This application is designed to help users explore and analyze a dataset containing information about various loan and financial products offered by different companies across Canada. The dataset includes details such as loan amounts, interest rates, eligibility criteria, and operational regions. The key fields in the dataset are:
        Id: Unique identifier for each record.
        Name: Name of the product or service.
        Min_range: Minimum loan amount or range.
        Max_range: Maximum loan amount or range.
        Interest_rate: Interest rate applicable to the product/service.
        Period: Duration of the loan/service in months.
        Provinces: Canadian provinces where the product/service is available.
        Employment: Types of employment eligible for the product/service.
        Monthly_income: Required monthly income to qualify.
Residency_reqd: Residency requirements for applicants.
Credit_type: Acceptable credit score types for eligibility.
Debt_percentage: Debt-to-income ratio for eligibility.
Status: Current status of the product/service (e.g., Active, Pending).
Type_id: Identifier for the type of service offered.
Product_type: Type of financial product (e.g., Unsecured Loan).
Interest_rate1: Additional interest rate information.
Language_csv: Language options in CSV format.
Preapproved: Indicates if preapproval is available.
Company: Name of the company offering the product/service.
Actions: Possible actions related to the product/service.

Using this application, users can:

Filter and search for financial products by specific criteria such as province, interest rate, loan amount, or company.
Compare products to find the best options based on their financial needs and eligibility.
Gain insights into the types of financial products available in different regions.
Identify companies offering specific types of loans and their operational details.
This tool aims to provide a comprehensive and user-friendly interface for exploring and analyzing loan and financial product data, facilitating better decision-making for both consumers and financial advisors."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
