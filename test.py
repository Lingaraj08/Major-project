import razorpay

# Initialize Razorpay client with test credentials
client = razorpay.Client(auth=('rzp_test_YOUR_KEY_ID', 'YOUR_KEY_SECRET'))

# Create a test order
order = client.order.create({
    'amount': 1000,  # Amount in paise
    'currency': 'INR',
    'receipt': 'test_receipt_001',
    'payment_capture': 1
})

print("Order created:")
print(order)

# Sample payment details structure (from webhook or API response)
payment_response = {
    'razorpay_payment_id': 'pay_29QQoUBi66xm2f',
    'razorpay_order_id': 'order_9A33XWu170gUtm',
    'razorpay_signature': 'test_signature'
}

print("\nPayment response:")
print(payment_response)
