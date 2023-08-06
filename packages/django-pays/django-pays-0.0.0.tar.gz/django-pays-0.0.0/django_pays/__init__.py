try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode


def payment_url(gateway, order_id, amount, currency=None, email='', lang=None):
    from .models import Gateway

    if not isinstance(gateway, Gateway):
        gateway = Gateway.objects.get(slug=gateway)

    return 'https://www.pays.cz/paymentorder?' + urlencode({
        'Merchant': gateway.merchant_id,
        'Shop': gateway.shop_id,
        'MerchantOrderNumber': order_id,
        'Amount': amount,
        'Currency': currency or gateway.default_currency,
        'Lang': lang or gateway.default_lang,
        'Email': email,
    })
