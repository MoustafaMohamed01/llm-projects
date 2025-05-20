from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from api_key import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_model_response(file_documents, user_query):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please check api_key.py.")

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    context = '\n\n'.join(str(p.page_content) for p in file_documents)
    data_chunks = text_splitter.split_text(context)

    if not data_chunks:
        return "No data available to create embeddings. Please check your CSV file."

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001',
        google_api_key=GEMINI_API_KEY
    )
    retriever = Chroma.from_texts(data_chunks, embeddings).as_retriever()
    records = retriever.get_relevant_documents(user_query)

    prompt_template = """
    You are an AI assistant specialized in analyzing CSV datasets.
    Answer the question based ONLY on the provided context. If the answer
    is not found in the context, politely state that you cannot answer.

    Context: {context}
    Question: {question}
    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

    model = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        temperature=0.7,
        google_api_key=GEMINI_API_KEY
    )

    chain = load_qa_chain(llm=model, chain_type='stuff', prompt=prompt)

    try:
        response = chain(
            {'input_documents': records, 'question': user_query},
            return_only_outputs=True
        )
        return response['output_text']
    except Exception as e:
        return f"An error occurred: {e}"
