import stripe
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_price(course):
    """Создает продукт и цену в Stripe"""
    try:
        product = stripe.Product.create(name=course.name)
        price = stripe.Price.create(
            currency="usd",
            unit_amount=int(course.price * 100),
            product=product.id,
        )
        return price
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe"""
    try:
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/success/",
            cancel_url="http://127.0.0.1:8000/cancel/",
            line_items=[{
                "price": price.id,
                "quantity": 1,
            }],
            mode="payment",
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe session error: {e}")
