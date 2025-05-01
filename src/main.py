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
        backstory='I am an orchestration agent specialized in managing workflows and handling payments. I ensure that all services are properly compensated for their work using decentralized payment protocols.',
        llm=llm,
        tools=[nevermined_payment_tool],
        verbose=True
    )
    
    analyzer_agent = Agent(
        role='Analyzer',
        goal='Analyze data and extract meaningful insights',
        backstory='I am an expert in data analysis with the ability to identify patterns, trends, and insights from complex information. I provide detailed analytical reports based on raw data.',
        llm=llm,
        verbose=True
    )
    
    summarizer_agent = Agent(
        role='Summarizer',
        goal='Summarize complex data into concise, actionable insights',
        backstory='I specialize in condensing large volumes of information into clear, concise summaries. I focus on extracting the most important points and presenting them in an easily digestible format.',
        llm=llm,
        verbose=True
    )
    
    # Define tasks with payment dependencies
    task_pay_analyzer = Task(
        description=f"Pay for the Analyzer service using DID {os.getenv('ANALYZER_SERVICE_DID')} with payment amount {os.getenv('ANALYZER_PAYMENT_AMOUNT')}",
        expected_output="Confirmation of successful payment to the Analyzer service with agreement ID",
        agent=orchestrator,
        tools=[nevermined_payment_tool]
    )
    
    task_analyze = Task(
        description="Analyze the provided text and extract key insights, trends, and patterns.",
        expected_output="A detailed analysis of the text with identified patterns, trends, and insights",
        agent=analyzer_agent,
        context=[task_pay_analyzer]
    )
    
    task_pay_summarizer = Task(
        description=f"Pay for the Summarizer service using DID {os.getenv('SUMMARIZER_SERVICE_DID')} with payment amount {os.getenv('SUMMARIZER_PAYMENT_AMOUNT')}",
        expected_output="Confirmation of successful payment to the Summarizer service with agreement ID",
        agent=orchestrator,
        tools=[nevermined_payment_tool],
        context=[task_analyze]
    )
    
    task_summarize = Task(
        description="Create a concise summary of the analysis results highlighting the most important points.",
        expected_output="A concise summary of the key points from the analysis",
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