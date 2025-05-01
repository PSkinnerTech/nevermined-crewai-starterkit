# Crew AI + Nevermined Integration Starter Kit

This starter kit simplifies the process of integrating Crew AI's multi-agent orchestration capabilities with Nevermined's decentralized payment and access control protocol. It enables developers to quickly prototype and demonstrate monetized AI agent interactions, establishing secure and verifiable workflows between collaborating AI agents.

## Prerequisites

Before you start, ensure you have the following:
- Python 3.10 or newer (CrewAI requires Python >=3.10 and <3.13)
- An OpenAI API Key
- A Nevermined account (testnet recommended: Nevermined Sepolia)

## Quick Start Guide

1. Clone the repository:
```bash
git clone https://github.com/nevermined-io/crew-ai-starter-kit.git
cd crew-ai-starter-kit
```

2. Set up a Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure the environment:
   - Copy `src/example_env` to `.env` in the project root
   - Update the values with your OpenAI API key and Nevermined API key
   - You can get a Nevermined API key by following the instructions at https://docs.nevermined.app/docs/tutorials/integration/nvm-api-keys

4. Run the starter kit:
```bash
python src/main.py
```

## What's Included

- `src/tools.py`: Implementation of the Nevermined payment tool using CrewAI's `@tool` decorator
- `src/main.py`: Example workflow with orchestrator, analyzer, and summarizer agents
- `src/tests/`: Unit tests for validating tool functionality
- `docs/`: Architecture documentation and project roadmap

## How It Works

The integration follows this flow:
1. User triggers the orchestrator agent
2. Orchestrator pays for the Analyzer via Nevermined's payment system
3. Analyzer agent processes the provided input
4. Orchestrator pays for the Summarizer via Nevermined's payment system
5. Summarizer agent produces a summary
6. Final result is displayed in the terminal

All payments are securely managed using Nevermined API key authentication and payment protocol, ensuring transparent, verifiable interactions between agents.

## Implementation Details

The payment tool is implemented using CrewAI's `@tool` decorator:

```python
@tool("Nevermined Payment Tool")
def nevermined_payment_tool(service_did: str, payment_amount: str) -> str:
    """Handles payments via Nevermined protocol"""
    # Tool implementation...
```

This approach allows for easy integration with CrewAI agents and tasks, providing a clean interface for handling payments through the Nevermined protocol.

## Support & Issues

Encountered an issue or have a question? Open an issue on the GitHub repository. Contributions and suggestions for improvements are welcome!

Happy Building! 🎉