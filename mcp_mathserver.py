from mcp.server.fastmcp import FastMCP
mcp=FastMCP("MCP")

@mcp.tool()
def add(a:int, b:int)->int:
    """_summary_
    Add to number
    """
    return a+b

@mcp.tool()
def multiple(a:int,b:int) ->int:
    """Multiple two number"""
    return a*b
if __name__=="__main__":
    mcp.run(transport="stdio")