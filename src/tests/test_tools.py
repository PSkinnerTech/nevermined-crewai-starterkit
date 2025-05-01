import os
import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import nevermined_payment_tool

class TestNeverminedPaymentTool(unittest.TestCase):
    
    @patch('tools.Payments')
    @patch('tools.Environment')
    def test_payment_success(self, mock_environment, mock_payments):
        """Test successful payment processing."""
        # Setup mocks
        mock_payments_instance = MagicMock()
        mock_payments_instance.pay_for_service.return_value = {'agreement_id': 'test_agreement_id'}
        mock_payments.return_value = mock_payments_instance
        
        mock_env = MagicMock()
        mock_environment.get_environment.return_value = mock_env
        
        # Setup environment variables
        with patch.dict('os.environ', {
            'NEVERMINED_API_KEY': 'test_api_key',
            'NEVERMINED_ENVIRONMENT': 'testing'
        }):
            # Access and call the _run method directly
            result = nevermined_payment_tool.func('test_did', '1000')
        
        # Assertions
        mock_environment.get_environment.assert_called_once_with('testing')
        mock_payments.assert_called_once_with('test_api_key', environment=mock_env)
        mock_payments_instance.pay_for_service.assert_called_once_with(
            service_did='test_did', amount=1000
        )
        self.assertEqual(result, 'Payment successful, Agreement ID: test_agreement_id')
    
    @patch('tools.Payments')
    @patch('tools.Environment')
    def test_payment_failure(self, mock_environment, mock_payments):
        """Test error handling during payment."""
        # Setup mocks
        mock_payments_instance = MagicMock()
        mock_payments_instance.pay_for_service.side_effect = Exception('Payment failed')
        mock_payments.return_value = mock_payments_instance
        
        # Setup environment variables
        with patch.dict('os.environ', {
            'NEVERMINED_API_KEY': 'test_api_key',
            'NEVERMINED_ENVIRONMENT': 'testing'
        }):
            # Access and call the func method directly 
            result = nevermined_payment_tool.func('test_did', '1000')
        
        # Assertions
        self.assertEqual(result, 'Payment failed: Payment failed')

if __name__ == '__main__':
    unittest.main() 