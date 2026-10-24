from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
load_dotenv()
#--------------------------------------------------------------------
loader=PyPDFLoader('Attention_all_you_need.pdf')
documents= loader.load()
print("Paged loaded", len(documents))
#--------------------------------------------------------------------
splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunk=splitter.split_documents(documents)
print("Chunks created:",len(chunk))
#----------------------------------------------------------------- 
embedding_model=OpenAIEmbeddings(model='text-embedding-3-small')

vector_store=Chroma.from_documents(documents=chunk,embedding=embedding_model)
retriever=vector_store.as_retriever(search_kwargs={"k":3})

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.4)
prompt=ChatPromptTemplate.from_template("""
You are a researher expert,Answer the user's question using only the information provided in the context.
If the answer is not available in the context, say "I don't know based on the provided document."

Context:
{context}
Question:
{question}

Answer:
    """)

#======================================== 

import streamlit as st
st.title("Attention all you need")
question=st.text_input("Enter your question")
context=retriever.invoke(question)

final=prompt.invoke({'question':question, 'context':context})

if question:
    ans=llm.invoke(final)
    st.write(ans.content)
