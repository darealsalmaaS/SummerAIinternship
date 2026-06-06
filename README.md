# my-agent 🤖

A local AI agent that reads files using the MCP protocol. No cloud services, no API keys, no internet — everything runs on your machine.

## What it does

When you run `python client.py`, the agent:
1. Starts a local MCP server (`server.py`) as a subprocess
2. Sends this question to the LLM: "Read the file test_data/config.yaml and summarize the important parameters in 3 bullet points"
3. The LLM decides on its own to call the read_file tool via MCP
4. The file content travels through the MCP connection back to the LLM
5. The LLM generates and prints a 3-point summary

## Prerequisites

- Python 3.10+ — check with `python --version`
- Ollama installed and running — download at https://ollama.com

## Setup

### 1. Clone the repository
git clone https://github.com/darealsalmaaS/SummerAIinternship.git
cd SummerAIinternship

### 2. Pull the AI model
ollama pull qwen2.5:3b

### 3. Install Python dependencies
pip install -r requirements.txt

### 4. Run the agent
python client.py

## Expected output

MCP server connected.
AI wants to use tool: read_file(path='test_data/config.yaml')
File read successfully (286 chars)
Agent: Here are the important parameters from config.yaml:
- Network: CAN-FD protocol at 500 kbps, node ID 0x1A, 150ms timeout
- Logging: WARNING level, logs rotate every 50MB
- Safety: watchdog enabled, max 3 retries, fail-safe mode set to SHUTDOWN

## Project structure

my-agent/
├── server.py          # MCP server exposing the read_file tool
├── client.py          # Connects the LLM to the MCP server
├── test_data/
│   └── config.yaml    # Test file
├── requirements.txt
└── README.md

## Troubleshooting

ollama: command not found → Ollama is not installed. Download at https://ollama.com
ModuleNotFoundError → Run pip install -r requirements.txt again
Error: model not found → Run ollama pull qwen2.5:3b first
Agent replies without tool → Run python client.py again
