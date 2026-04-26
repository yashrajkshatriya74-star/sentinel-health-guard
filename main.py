from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test")

@mcp.tool()
def hello():
    return "hello world"

if __name__ == "__main__":
    # MCP khud server handle karta hai
    mcp.run()
