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
git clone https://github.com/nevermined-io/nevermined-crewai-starterkit.git
cd nevermined-crewai-starterkit
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

## Technical Details of the Integration

This starter kit demonstrates several key technical concepts:

### 1. AI Agent Monetization

The core concept demonstrated is how AI agent capabilities can be monetized through a decentralized payment system. In this model:

- Each AI agent (like our Analyzer and Summarizer) represents a specialized service with unique capabilities
- Access to these agent services requires payment through the Nevermined protocol
- Payments are handled securely and transparently, with agreement IDs providing verification of transactions

### 2. Tokenized Service Access

The integration shows how service access can be tokenized and managed through:

- Service DIDs (Decentralized Identifiers) that uniquely identify each agent service
- Payment amounts that represent the cost to access each service
- Access tokens and credentials that authorize usage after payment

### 3. Orchestration with Payment Dependencies

A critical aspect demonstrated is the orchestration of agents with payment-dependent tasks:

- The Orchestrator agent manages the workflow and handles payments
- Each agent's work is contingent on successful payment
- The CrewAI task system enforces these dependencies through contextual relationships
- Payments serve as "gates" that must be cleared before specialized agent work can proceed

### 4. Fallback and Error Handling

The implementation demonstrates robust error handling:

- Attempts to use the real Nevermined payment system when credentials are available
- Gracefully falls back to a mock implementation when there are issues
- Logs detailed error information to help with debugging
- Ensures the demo can continue running even when there are infrastructure or credential issues

## Implementation Details

The payment tool is implemented using CrewAI's `@tool` decorator:

```python
@tool("Nevermined Payment Tool")
def nevermined_payment_tool(service_did: str, payment_amount: str) -> str:
    """Handles payments via Nevermined protocol
    
    Args:
        service_did: The DID of the service to pay for
        payment_amount: The amount to pay (in wei)
        
    Returns:
        A confirmation message with the agreement ID
    """
    # Implementation that tries real payment processing first,
    # with fallback to mock implementation if needed
```

When executed, the tool:

1. Checks for valid Nevermined API credentials
2. If credentials are available, attempts to:
   - Initialize the Payments client
   - Get access to the specified service
   - Create an agreement for the payment
3. If any step fails, falls back to a mock implementation that simulates successful payment
4. Returns a confirmation message with an agreement ID (real or mock)

This approach enables both educational demonstrations and real-world usage with minimal code changes, making it ideal for anyone exploring AI monetization concepts through Nevermined.

## Support & Issues

Encountered an issue or have a question? Open an issue on the GitHub repository. Contributions and suggestions for improvements are welcome!

Happy Building! 🎉
