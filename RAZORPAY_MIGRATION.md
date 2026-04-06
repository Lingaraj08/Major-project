# HealthStack: SSLCommerz to Razorpay Migration Guide

## ✅ Migration Complete

Your HealthStack application has been successfully migrated from SSLCommerz payment gateway to Razorpay. Here's what was changed:

---

## 📋 Files Updated

### Core Configuration
- ✅ `setup.py` - Updated package to Razorpay
- ✅ `requirements.txt` - Razorpay SDK added (`razorpay==1.4.1`)
- ✅ `healthstack/settings.py` - Updated Django settings and env variables
- ✅ `healthstack/urls.py` - URL routing updated to use `/razorpay/` path
- ✅ `test.py` - Updated test file with Razorpay examples

### Payment Processing
- ✅ `sslcommerz/apps.py` - Updated app configuration
- ✅ `sslcommerz/urls.py` - All payment endpoints renamed
- ✅ `sslcommerz/views.py` - Complete rewrite with Razorpay SDK integration

### Frontend
- ✅ `templates/razorpay-checkout.html` - New checkout page with Razorpay Checkout JS
- ✅ `templates/test-cart.html` - Updated payment button URLs
- ✅ `templates/patient-dashboard.html` - Updated appointment payment URLs

### Documentation
- ✅ `README.md` - API references updated
- ✅ Migration notes created

---

## 🔧 Next Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Add these to your `.env` file:
```
RAZORPAY_KEY_ID=rzp_live_your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here
```

### 3. Get Razorpay Credentials
1. Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. For testing: Use sandbox credentials (rzp_test_*)
3. For production: Generate live credentials

### 4. Database Considerations
- Existing Payment model remains unchanged and compatible
- No migrations needed for the Payment model
- Old transaction data remains preserved

---

## 🔄 API Endpoint Changes

| Payment Type | Old URL | New URL |
|---|---|---|
| **Appointment** | `/sslcommerz/ssl-payment-request/<pk>/<id>/` | `/razorpay/razorpay-payment-request/<pk>/<id>/` |
| **Medicine** | `/sslcommerz/ssl-payment-request-medicine/<pk>/<id>/` | `/razorpay/razorpay-payment-request-medicine/<pk>/<id>/` |
| **Test** | `/sslcommerz/ssl-payment-request-test/<pk>/<id>/<pk2>/` | `/razorpay/razorpay-payment-request-test/<pk>/<id>/<pk2>/` |
| **Verification** | N/A | `/razorpay/verify-payment/` |

---

## 💳 Payment Flow

### Before (SSLCommerz)
1. User initiates payment
2. Session created with SSLCommerz
3. Redirect to SSLCommerz payment page
4. IPN validation
5. Success/Failure redirect

### After (Razorpay)
1. User initiates payment
2. Razorpay order created with amount in paise
3. Razorpay Checkout modal opens
4. User completes payment
5. Signature verification via `/razorpay/verify-payment/`
6. Django backend processes payment
7. Email notification sent

---

## ✨ Features

### Razorpay Benefits
- ✅ Global payment support (100+ payment methods)
- ✅ Multiple payment options: Cards, UPI, Wallets, Netbanking
- ✅ Better security with signature verification
- ✅ Simplified payment flow with Checkout JS
- ✅ Comprehensive dashboard and reporting

### Maintained Features
- ✅ Email notifications for payments
- ✅ Payment tracking in database
- ✅ Support for appointment, medicine, and test payments
- ✅ Patient invoice generation

---

## 🧪 Testing

### Sandbox Testing
1. Use test credentials: `rzp_test_*`
2. Test payment details (from Razorpay docs):
   - Card: 4111 1111 1111 1111
   - CVV: Any 3 digits
   - Expiry: Any future date

### URLs for Testing
- Appointment Payment: `/razorpay/razorpay-payment-request/<patient_id>/<appointment_id>/`
- Medicine Payment: `/razorpay/razorpay-payment-request-medicine/<patient_id>/<order_id>/`
- Test Payment: `/razorpay/razorpay-payment-request-test/<patient_id>/<test_order_id>/<prescription_id>/`

---

## 📞 Support

### Razorpay Documentation
- [Razorpay Dashboard](https://dashboard.razorpay.com/)
- [Payment Gateway Docs](https://razorpay.com/docs/)
- [API Reference](https://razorpay.com/docs/api/)

### Common Issues

**Issue**: Payment fails immediately
- **Solution**: Verify RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in settings

**Issue**: Signature verification fails
- **Solution**: Ensure keys are correct and payment data matches exactly

**Issue**: Amount discrepancies
- **Solution**: Remember amounts in Razorpay are in paise (multiply by 100)

---

## 📊 Payment Model Fields

The existing Payment model includes:
- `transaction_id` (Razorpay Order ID)
- `val_transaction_id` (Razorpay Payment ID)
- `status` (Payment status: 'captured', 'failed', etc.)
- `currency_amount` (Amount in original currency)
- `card_type` (Payment method)
- `payment_type` ('appointment', 'pharmacy', 'test')
- Email and customer details
- Appointment/Order/Test relationships

---

## 🎯 Migration Summary

| Item | Status | Details |
|---|---|---|
| Payment Gateway | ✅ | SSLCommerz → Razorpay |
| Dependencies | ✅ | Updated to razorpay==1.4.1 |
| Settings | ✅ | RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET |
| Views | ✅ | Complete rewrite for Razorpay SDK |
| URLs | ✅ | All endpoints updated |
| Templates | ✅ | Checkout page + URL updates |
| Models | ✅ | Compatible (no changes needed) |
| Database | ✅ | No migrations needed |

---

**Status**: ✅ **Complete - Ready for Testing**

Last Updated: April 6, 2026
