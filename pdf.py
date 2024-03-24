from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import streamlit as st
import shutil
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SUMMARIZE_PROMPT_TEMPLATE = """
You are a university student and is asked by the professor to write a summary of the uploaded document. 
The summary should have close to {word_approx} words but must not exceed {word_limit} words and {para_limit} paragraphs.  
Focus on capturing the main ideas and key points discussed in the document. Use your own words and layman's terms.
"""


@st.cache_data(show_spinner=False)
def process_file(file_name):
    upload_path = os.path.join(BASE_DIR, "tmp", file_name)
    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(upload_path)
    pages = loader.load_and_split()
    # cleaning up
    try:
        shutil.rmtree(os.path.join(BASE_DIR, "tmp"))
    except FileNotFoundError:
        pass
    return pages


st.title("PDF Summarizer")
# create a tmp folder to store the uploaded file
try:
    os.mkdir(os.path.join(BASE_DIR, "tmp"))
except FileExistsError:
    pass
# Create a file uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")
if uploaded_file:
    with st.spinner("Processing file..."):
        pages = process_file(uploaded_file.name)
    st.success("File processed!")

word_limit = st.sidebar.number_input("Word limit", value=300)
word_approx = st.sidebar.number_input("Approx. word count", value=200)
para_limit = st.sidebar.number_input("Paragraphs", value=1)
summarize = st.sidebar.button("Summarize", disabled=not bool(uploaded_file))
if summarize:
    with st.spinner("Generating summary..."):
        question = SUMMARIZE_PROMPT_TEMPLATE.format(
            word_limit=word_limit, word_approx=word_approx, para_limit=para_limit
        )
        faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(question)

        llm = ChatOpenAI(temperature=0, model_name="gpt-4")
        chain = load_qa_chain(llm, chain_type="stuff")

        result = chain.run(input_documents=docs, question=question)
    st.write(result)
