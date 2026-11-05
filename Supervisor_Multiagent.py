from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini', temperature=0.4)

def search_duckduckgo(query:str):
    """Search duckduckgo using langchain DuckDuckGoSearchRun tool"""
    search=DuckDuckGoSearchRun()
    return search.invoke(query)

def add(a:int, b:int) ->int:
    """Adding two number a and b"""
    return a+b

def Multiply(a:int, b:int) ->int:
    """Multiply two number a and b"""
    return a*b

#create agent

math_agent = create_agent(model=model, tools=[add,Multiply], name="Maths",
                          system_prompt='you are an expert mathematician, always use one tool at a time')

search_agent = create_agent(model=model, tools=[search_duckduckgo], name="search",
                            system_prompt='you are a world class researcher with access to web search, do not do any math')

#create supervisor

workflow=create_supervisor(
    [math_agent,search_agent],
    model=model,
    prompt=(
        'you are a team supervisor managing a research expert and a math expert'
        'for current events, use search_agent tool'
        'for math problem, use math_agent tool'
    )
)

app=workflow.compile()

import streamlit as st

st.title("Supervisor agent")
question=st.text_input("Enter you question?")

if question:
    #ans=app.invoke({'role':'user',"content":question})
    ans=app.invoke({"messages":[{'role':'user','content':question}]})
    st.write(ans['messages'][-1].content)
    



