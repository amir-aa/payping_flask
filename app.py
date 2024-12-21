from flask import Flask, render_template, request, redirect, url_for, flash, session
from dataclasses import dataclass
import requests
from typing import Optional
import os
from urllib.parse import urljoin

# PayPing implementation from previous artifact
@dataclass
class PaymentRequest:
    amount: int
    return_url: str
    payer_identity: Optional[str] = None
    payer_name: Optional[str] = None
    description: Optional[str] = None
    client_ref_id: Optional[str] = None

class PayPingGateway:
    BASE_URL = "https://api.payping.ir/v2"
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
    
    def create_payment(self, payment: PaymentRequest) -> dict:
        endpoint = f"{self.BASE_URL}/pay"
        
        payload = {
            "amount": payment.amount,
            "returnUrl": payment.return_url,
            "payerIdentity": payment.payer_identity,
            "payerName": payment.payer_name,
            "description": payment.description,
            "clientRefId": payment.client_ref_id
        }
        
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def verify_payment(self, amount: int, ref_id: str) -> bool:
        endpoint = f"{self.BASE_URL}/pay/verify"
        
        payload = {
            "amount": amount,
            "refId": ref_id
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return True

    def get_payment_gateway_url(self, code: str) -> str:
        return f"https://api.payping.ir/v1/pay/gotoipg/{code}"


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key


PAYPING_API_TOKEN = 'your-api-token-here'  # Replace with your actual API token
gateway = PayPingGateway(PAYPING_API_TOKEN)

# Sample product database
products = {
    '1': {'name': 'Product 1', 'price': 10000},  # Price in Tomans
    '2': {'name': 'Product 2', 'price': 20000},
    '3': {'name': 'Product 3', 'price': 30000},
}

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/initiate-payment/<product_id>')
def initiate_payment(product_id):
    if product_id not in products:
        flash('Invalid product selected.')
        return redirect(url_for('index'))
    
    product = products[product_id]
    session['product_id'] = product_id  # Store product_id for verification
    
    # Create payment request
    payment = PaymentRequest(
        amount=int(product['price']),
        return_url=url_for('verify_payment', _external=True),#must include registered domain
        description=f"Payment for {product['name']}",
        client_ref_id=f"order_{product_id}"
    )
    
    try:
        # Create payment and get the code
        result = gateway.create_payment(payment)
        payment_code = result['code']
        
        # Store payment amount in session for verification
        session['payment_amount'] = product['price']
        
        # Redirect to payment gateway
        return redirect(gateway.get_payment_gateway_url(payment_code))
        
    except requests.exceptions.RequestException as e:
        flash(f'Payment initiation failed: {str(e)}')
        return redirect(url_for('index'))

@app.route('/verify-payment')
def verify_payment():
    ref_id = request.args.get('refId')
    if not ref_id:
        flash('Payment verification failed: No reference ID provided.')
        return redirect(url_for('index'))
    
    # Get stored payment amount from session
    payment_amount = session.get('payment_amount')
    if not payment_amount:
        flash('Payment verification failed: Invalid session.')
        return redirect(url_for('index'))
    
    try:
        # Verify the payment
        if gateway.verify_payment(payment_amount, ref_id):
            product_id = session.get('product_id')
            product = products.get(product_id, {'name': 'Unknown Product'})
            flash(f'Payment successful for {product["name"]}!')
            
            # Clear session data
            session.pop('payment_amount', None)
            session.pop('product_id', None)
            
            return redirect(url_for('success'))
        else:
            flash('Payment verification failed.')
            return redirect(url_for('index'))
            
    except requests.exceptions.RequestException as e:
        flash(f'Payment verification failed: {str(e)}')
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)