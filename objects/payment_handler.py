import stripe


class PaymentHandler:
    def process_payment(self, payment_token, amount):
        try:
            payment_details = stripe.Charge.create(
                amount=int(amount * 100),  # converted to pennies because Stripe likes it that way
                currency="usd",
                source=payment_token,
                description="Tickets",
            )
            return payment_details
        except:
            return {}

    def process_refund(self, payment_id, amount):
        try:
            refund_details = stripe.Refund.create(
                charge=payment_id,
                amount=int(amount * 100)  # converted to pennies again (see above for reason)
            )
            return refund_details
        except:
            return {}
