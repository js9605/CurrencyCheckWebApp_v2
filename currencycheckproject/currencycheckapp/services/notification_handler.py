from currencycheckapp.tasks.celery_tasks import check_currency_threshold
from currencycheckproject.currencycheckapp.models import Currency, UserCurrencies


# Using this in celery.py for scheduling
def fetch_currency_values_and_notify():

    user_currencies_list = UserCurrencies.objects.all()

    for user_currency in user_currencies_list:
        user = user_currency.user
        currency_shortcut = user_currency.currency_shortcut
        user_email = user_currency.user_email

        currency_rates = get_currency_value(user, currency_shortcut)
        threshold = get_threshold(user, currency_shortcut)

        check_currency_threshold.delay(user_email, currency_shortcut, currency_rates, threshold)

def get_currency_value(user, currency_shortcut):
    try:
        currency = Currency.objects.get(user=user, currency_shortcut=currency_shortcut)
        currency_rates = {'purchase_rate': currency.purchase_rate, 'selling_rate': currency.selling_rate}
        return currency_rates
    
    except Currency.DoesNotExist:
        print("log: Currency.DoesNotExist in notification_handler.get_currency_value")
        return None

def get_threshold(user, currency_shortcut):
    try:
        user_currency = UserCurrencies.objects.get(user=user, currency_shortcut=currency_shortcut)
        threshold = {'upper_limit': user_currency.upper_limit, 'lower_limit': user_currency.lower_limit}
        return threshold
    
    except UserCurrencies.DoesNotExist:
        print("log: UserCurrencies.DoesNotExist in notification_handler.get_threshold")
        return None


#TODO Example usage

# # Assuming you have a logged-in user (replace 'logged_user' with your actual user variable)
# logged_user = request.user  # or however you retrieve the logged-in user in your view/controller

# # Get the purchase rate for the currency with shortcut 'USD' for the logged-in user
# purchase_rate_usd = get_currency_value(logged_user, 'USD', criterion='purchase_rate')
