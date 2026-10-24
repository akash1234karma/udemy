from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mcp_mathserver.py"],
                "transport":'stdio'
            },
            "weather":{
                "url":"https//localhost:8000/mcp",
                "transport":"streamable_http"
            }
        }
    )

    tools=await client.get_tools()
    model=ChatOpenAI(model='gpt-3.5-turbo')
    agent=create_agent(tools,model)

    math_response=await agent.ainvoke({'messages':[{"role":"user","content":"what is (3+5)x 12?"}]})
    weather_resposne=await agent.ainvoke({'messages':[{'role':'user',"content":"what is weather in california?"}]})   

    print("Math response", math_response['messages'][-1].content)
    print("Weather response", weather_resposne['message'[-1].content])

asyncio.run(main())                   