import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from tools import nevermined_payment_tool

# Load environment variables
load_dotenv()

def main():
    # Initialize LLM
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define agents
    orchestrator = Agent(
        role='Orchestrator',
        goal='Manage agent payments and coordinate tasks between agents',
        llm=llm,
        tools=[nevermined_payment_tool],
        verbose=True
    )
    
    analyzer_agent = Agent(
        role='Analyzer',
        goal='Analyze data and extract meaningful insights',
        llm=llm,
        verbose=True
    )
    
    summarizer_agent = Agent(
        role='Summarizer',
        goal='Summarize complex data into concise, actionable insights',
        llm=llm,
        verbose=True
    )
    
    # Define tasks with payment dependencies
    task_pay_analyzer = Task(
        description=f"Pay for the Analyzer service using DID {os.getenv('ANALYZER_SERVICE_DID')} with payment amount {os.getenv('ANALYZER_PAYMENT_AMOUNT')}",
        agent=orchestrator,
        tools=[nevermined_payment_tool]
    )
    
    task_analyze = Task(
        description="Analyze the provided text and extract key insights, trends, and patterns.",
        agent=analyzer_agent,
        context=[task_pay_analyzer]
    )
    
    task_pay_summarizer = Task(
        description=f"Pay for the Summarizer service using DID {os.getenv('SUMMARIZER_SERVICE_DID')} with payment amount {os.getenv('SUMMARIZER_PAYMENT_AMOUNT')}",
        agent=orchestrator,
        tools=[nevermined_payment_tool],
        context=[task_analyze]
    )
    
    task_summarize = Task(
        description="Create a concise summary of the analysis results highlighting the most important points.",
        agent=summarizer_agent,
        context=[task_pay_summarizer]
    )
    
    # Create and run the crew
    crew = Crew(
        agents=[orchestrator, analyzer_agent, summarizer_agent],
        tasks=[task_pay_analyzer, task_analyze, task_pay_summarizer, task_summarize],
        verbose=True
    )
    
    print("\n=== 🚀 Starting Crew AI + Nevermined Integration Demo ===\n")
    print("This demo shows how to use Nevermined's payment system to monetize AI agent interactions.")
    print("The Orchestrator will pay for services from the Analyzer and Summarizer agents via Nevermined.\n")
    
    # Run the workflow
    result = crew.kickoff(inputs={"initial_text": "Climate change is accelerating with global temperatures rising faster than predicted. Recent studies show the Arctic ice melting at unprecedented rates, contributing to sea level rise. Meanwhile, extreme weather events including floods, wildfires, and hurricanes have increased in frequency and intensity worldwide."})
    
    print("\n\n=== 🎉 FINAL RESULT ===")
    print(result)
    print("\n=== 💡 Demo Complete ===")
    print("All payments were handled through the Nevermined payment protocol.")
    print("See the documentation at https://docs.nevermined.app for more details on how to use Nevermined.")

if __name__ == "__main__":
    main() 