from mcp.server.fastmcp import FastMCP

# On crée le serveur MCP et on lui donne un nom
mcp = FastMCP("file-reader")


# On définit l'outil read_file
@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from disk and return its contents as a string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: file '{path}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"


# On lance le serveur en mode stdio
if __name__ == "__main__":
    mcp.run(transport="stdio")
