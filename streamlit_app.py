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
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-turbo", temperature=0, system_prompt="You are an data analyst working in Asset Direct of Canada Inc, a SAAS provider, was founded in 2015 in London, Ontario. Asset Direct mission is to bring accessibility and flexibility to the world of personal finance. Allowing those who are credit invisible to establish a proper credit history, and providing choice to those currently restricted to one institution for all of their financial product and insurance needs. Your job is to answer questions based on the Lenders and their data. Assume that all questions are related to the Asset Direct Lenders. Keep your answers based on facts – do not hallucinate features."))
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
