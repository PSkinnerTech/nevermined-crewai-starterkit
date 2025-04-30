import os
from dotenv import load_dotenv
from crewai_tools import BaseTool
from payments_py import Payments, Environment

load_dotenv()

class NeverminedPaymentTool(BaseTool):
    name = "Nevermined Service Payment Tool"
    description = "Handles payments via Nevermined protocol"

    def __init__(self):
        super().__init__()
        nvm_api_key = os.getenv("NEVERMINED_API_KEY")
        env_name = os.getenv("NEVERMINED_ENVIRONMENT", "testing")
        self.payments = Payments(nvm_api_key, environment=Environment.get_environment(env_name))

    def _run(self, service_did, payment_amount):
        """
        Execute payment for a service through Nevermined
        
        Args:
            service_did (str): The DID of the service to pay for
            payment_amount (str): The amount to pay (in wei)
            
        Returns:
            str: Confirmation message with agreement ID
        """
        try:
            # Note: This is a placeholder implementation as the actual method would depend
            # on the payments-py API which might differ from the old SDK
            response = self.payments.pay_for_service(
                service_did=service_did,
                amount=int(payment_amount)
            )
            
            # Extract agreement ID from response (implementation details may vary)
            agreement_id = response.get('agreement_id', 'unknown')
            return f"Payment successful, Agreement ID: {agreement_id}"
        except Exception as e:
            return f"Payment failed: {str(e)}" 