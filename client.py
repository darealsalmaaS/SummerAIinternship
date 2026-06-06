import asyncio
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from disk and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file to read.",
                    }
                },
                "required": ["path"],
            },
        },
    }
]

QUESTION = (
    "Read the file test_data/config.yaml "
    "and summarize the important parameters in 3 bullet points."
)

MODEL = "qwen2.5:3b"


async def main():
    server_params = StdioServerParameters(
        command="python", args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            print("✅ MCP server connected.\n")

            messages = [{"role": "user", "content": QUESTION}]

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
            )

            reply = response.message

            if reply.tool_calls:
                for tool_call in reply.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = tool_call.function.arguments
                    path = tool_args.get("path", "")

                    print(f"🔧 AI wants to use tool: {tool_name}(path='{path}')")

                    result = await session.call_tool(tool_name, {"path": path})
                    file_content = result.content[0].text

                    print(f"📄 File read successfully ({len(file_content)} chars)\n")

                    messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
                    messages.append({"role": "tool", "content": file_content})

                final_response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                )
                print("🤖 Agent:", final_response.message.content)

            else:
                print("🤖 Agent:", reply.content)


if __name__ == "__main__":
    asyncio.run(main())
