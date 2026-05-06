import os

class StripeWrapper:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_API_KEY")

    def create_checkout_session(self, product_name: str, amount: int):
        # Mocking Stripe interaction
        return {
            "session_id": "cs_test_aether_123",
            "url": f"https://checkout.stripe.com/pay/cs_test_aether_123",
            "product": product_name,
            "amount": amount
        }

stripe = StripeWrapper()
