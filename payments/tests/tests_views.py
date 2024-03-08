from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch


class TestPaymentView(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        
    def test_successful_payment(self):
        url = reverse('payment')
        data = {'amount':1000,'token':'valid_token'}
        
        response = self.client.post(url,data,format='json')
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['message'],'Payment successfull')
        
    def test_card_error(self):
        url = reverse('payment')
        data = {'amount':1000,'token':'invalid_token'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 402)
        self.assertIn('error',response.data)
        
    @patch('stripe.Charge.create')
    def test_server_error(self,mock_charge_create):
        url = reverse('payment')
        data = {'amount':1000,'token':'valid_token'}
        
        
        mock_charge_create.side_effect = Exception('Stripe API error')
        
        response = self.client.post(url,data,format='json')
        
        self.assertEqual(response.status_code,500)
        self.assertIn('error',response.data)