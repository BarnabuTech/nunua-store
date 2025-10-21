import requests
import base64
from datetime import datetime
from django.conf import settings
import json

class MpesaClient:
    def __init__(self):
        self.business_shortcode = settings.MPESA_SHORTCODE
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.api_url = settings.MPESA_API_URL

    def get_access_token(self):
        """Get access token from Safaricom"""
        url = f"{self.api_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        
        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Basic {auth}"}
            )
            response.raise_for_status()  # Raise exception for non-200 status codes
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def generate_password(self):
        """Generate password for STK push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_str.encode()).decode(), timestamp

    def initiate_stk_push(self, phone_number, amount, order_ref):
        """Initiate STK push"""
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        # Format phone number (remove + if present and ensure it starts with 254)
        phone_number = phone_number.replace("+", "")
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif not phone_number.startswith("254"):
            phone_number = "254" + phone_number

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{self.callback_url}?order_ref={order_ref}",
            "AccountReference": order_ref,
            "TransactionDesc": f"Payment for order {order_ref}"
        }

        try:
            response = requests.post(
                f"{self.api_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"STK push failed: {str(e)}")

    def verify_transaction(self, checkout_request_id):
        """Verify transaction status"""
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        try:
            response = requests.post(
                f"{self.api_url}/mpesa/stkpushquery/v1/query",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Transaction verification failed: {str(e)}") 