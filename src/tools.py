import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from payments_py import Payments, Environment

load_dotenv()

@tool("Nevermined Payment Tool")
def nevermined_payment_tool(service_did: str, payment_amount: str) -> str:
    """Handles payments via Nevermined protocol
    
    Args:
        service_did: The DID of the service to pay for
        payment_amount: The amount to pay (in wei)
        
    Returns:
        A confirmation message with the agreement ID
    """
    try:
        nvm_api_key = os.getenv("NEVERMINED_API_KEY")
        env_name = os.getenv("NEVERMINED_ENVIRONMENT", "testing")
        
        payments = Payments(nvm_api_key, environment=Environment.get_environment(env_name))
        
        # Note: This is a placeholder implementation as the actual method would depend
        # on the payments-py API which might differ from the old SDK
        response = payments.pay_for_service(
            service_did=service_did,
            amount=int(payment_amount)
        )
        
        # Extract agreement ID from response (implementation details may vary)
        agreement_id = response.get('agreement_id', 'unknown')
        return f"Payment successful, Agreement ID: {agreement_id}"
    except Exception as e:
        return f"Payment failed: {str(e)}" 