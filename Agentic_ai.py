import os
import socket
import psutil
from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

@tool
def check_cpu() ->str:
    """Check the current CPU usage of the system"""
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage > 80:
        status = "CRITICAL"
    elif cpu_usage > 60:
        status = 'WARNING'
    else:
        status = 'HEALTHY'
    return f'Cpu usage: {cpu_usage}% | Status:{status}'

@tool
def check_memory() ->str:
    """Check the current memory usage of the system"""

    memory=psutil.virtual_memory()
    memory_usage=memory.percent

    if memory_usage > 85:
        status = 'CRIRICAL'
    elif memory_usage > 70:
        status = 'WARNING'
    else:
        status = 'HEALTHY'

    return f'Memory usage: {memory_usage}% | Status:{status}'

@tool
def check_disk() -> str:
    """Check DISK usage of the system"""
    disk=psutil.disk_usage("/")
    disk_usage=disk.percent

    if disk_usage > 90:
        status = "CRITICAL"
    elif disk_usage > 80:
        status = "WARNING"
    else:
        status = "HEALTHY"

    return f'Disk usage {disk_usage}% | Status: {status}'

@tool
def check_network() -> str:
    """Check whether network connectivity is available."""

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Network Status: HEALTHY - Internet connection is available."

    except OSError:
        return "Network Status: CRITICAL - Internet connection is unavailable."


llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.4)
tools = [check_cpu,check_memory,check_disk,check_network]

agent = create_agent(model=llm,tools=tools,
                     system_prompt="""You are a System Health Monitoring AI Agent.

    Your job is to monitor the health of the computer.

    Available tools:
    - CPU health check
    - Memory health check
    - Disk health check
    - Network connectivity check

    When the user asks for a complete system health check,
    execute all relevant tools and provide a simple summary.

    Clearly mention:
    HEALTHY
    WARNING
    CRITICAL
    
    also if user is looking for specific parameter provide that only like if check CPU then respond with only CPU value

    """)

import streamlit as st
st.title("SYSTEM HEALTH")
question=st.text_input("Enter what would you like to check")

if question:
    result=agent.invoke({"message":[{'role':'user',"content":question}]})
    st.write(result['messages'][-1].content)