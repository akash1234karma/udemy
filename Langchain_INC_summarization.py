from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

llm = OpenAI(model='gpt-4o-mini', temperature=0.5)

prompt=ChatPromptTemplate.from_template(
    """ You are an experienced IT production support engineer.
    Analyze the following production incident
    Incident:{incident}

    Provide your response in this format:

    Issue Summary:
    Possible causes:
    Troubleshooting steps:
    Recommendation:
    
""")

parser=StrOutputParser()
chain = prompt | llm | parser

st.title("Langchain")

incident = st.text_input("Enter incident description")

if incident:
    response = chain.invoke({"incident": incident})
    st.write(response)