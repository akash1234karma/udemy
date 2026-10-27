from typing import TypedDict, Literal
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI

llm=ChatOpenAI(model='gpt-4o-mini',temperature=0.4)

class State(TypedDict):
    question:str
    category:str
    answer:str

def classify_question(state:State):
    prompt = f"""Classify the following IT support question.
    
    Return exactly one word:
    techincal
    general
    
    Question: {state['question']}"""

    response = llm.invoke(prompt)
    category = response.content.strip().lower()
    return {"category":category}


def technical_support(state: State):
    prompt = f"""
    You are a technical support assistant.
    Issue: {state["question"]}
    Provide a clear solution to the technical issue.
    """
    response = llm.invoke(prompt)
    return {
        "answer": response.content
    }

def general_support(state:State):
    prompt=f"""You are a helpful IT assistant". Explain the answer in simple language
    Question:{state['question']}"""
    response=llm.invoke(prompt)
    return  {"answer": response.content}

def route_question(state:State) -> Literal['technical', 'general']:
    if state['category'] == "technical":
        return "technical"
    else:
        return "general"

graph_builder = StateGraph(State)
graph_builder.add_node("classifier",classify_question)
graph_builder.add_node("technical_support",technical_support)
graph_builder.add_node("general_support",general_support)
graph_builder.add_edge(START,"classifier")

graph_builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "technical":"technical_support",
        "general":"general_support"
    }
)

graph_builder.add_edge("technical_support",END)
graph_builder.add_edge("general_support",END)

graph=graph_builder.compile()

import streamlit as st
st.title("New code")
question=st.text_input("Enter your question")

result=graph.invoke({"question":question,"category":"","answer":""})

if question:
    ans=graph.invoke(result)
    print(ans['category'])
    st.write(ans['answer'])
                  




'''while True:

    question = input(
        "\nEnter your question "
        "(type 'exit' to stop): "
    )

    if question.lower() == "exit":
        print("Goodbye!")
        break

    result = graph.invoke({
        "question": question,
        "category": "",
        "answer": ""
    })

    print("\nCategory:", result["category"])

    print("\nAnswer:")
    print(result["answer"])'''