import stripe
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_price(course):
    product = stripe.Product.create(name=course.name)
    price = stripe.Price.create(
        currency="usd",
        unit_amount=100,
        product_data={"name": product.name},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.unit_amount, "quantity": 2}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
