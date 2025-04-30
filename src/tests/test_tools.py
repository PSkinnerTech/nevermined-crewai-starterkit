import os
import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import NeverminedPaymentTool

class TestNeverminedPaymentTool(unittest.TestCase):
    
    @patch('tools.Payments')
    @patch('tools.Environment')
    def test_initialization(self, mock_environment, mock_payments):
        """Test that the NeverminedPaymentTool initializes correctly."""
        # Setup mocks
        mock_payments_instance = MagicMock()
        mock_payments.return_value = mock_payments_instance
        
        mock_env = MagicMock()
        mock_environment.get_environment.return_value = mock_env
        
        # Create tool with mocked dependencies
        with patch.dict('os.environ', {
            'NEVERMINED_API_KEY': 'test_api_key',
            'NEVERMINED_ENVIRONMENT': 'testing'
        }):
            tool = NeverminedPaymentTool()
        
        # Assertions
        mock_environment.get_environment.assert_called_once_with('testing')
        mock_payments.assert_called_once_with('test_api_key', environment=mock_env)
        self.assertEqual(tool.payments, mock_payments_instance)
    
    @patch('tools.Payments')
    @patch('tools.Environment')
    def test_payment_success(self, mock_environment, mock_payments):
        """Test successful payment processing."""
        # Setup mocks
        mock_payments_instance = MagicMock()
        mock_payments_instance.pay_for_service.return_value = {'agreement_id': 'test_agreement_id'}
        mock_payments.return_value = mock_payments_instance
        
        # Create tool with mocked dependencies
        with patch.dict('os.environ', {
            'NEVERMINED_API_KEY': 'test_api_key',
            'NEVERMINED_ENVIRONMENT': 'testing'
        }):
            tool = NeverminedPaymentTool()
        
        # Test payment
        result = tool._run('test_did', '1000')
        
        # Assertions
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
        
        # Create tool with mocked dependencies
        with patch.dict('os.environ', {
            'NEVERMINED_API_KEY': 'test_api_key',
            'NEVERMINED_ENVIRONMENT': 'testing'
        }):
            tool = NeverminedPaymentTool()
        
        # Test payment with exception
        result = tool._run('test_did', '1000')
        
        # Assertions
        self.assertEqual(result, 'Payment failed: Payment failed')

if __name__ == '__main__':
    unittest.main() 