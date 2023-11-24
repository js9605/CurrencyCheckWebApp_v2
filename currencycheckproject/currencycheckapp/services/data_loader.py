from .webscraper import scrape_website
from currencycheckapp.models import Currency


def save_currency_data(currencies):
    print("SAVING CURRENCIES: ", currencies)
    for currency in currencies:
        scraped_data = scrape_website(currency)

        Currency.objects.create(
            currency_shortcut=scraped_data.get('currency_shortcut'),
            country=scraped_data.get('country'),
            ref_number=scraped_data.get('ref_number'),
            purchase_rate=scraped_data.get('purchase_rate'),
            selling_rate=scraped_data.get('selling_rate'),
            average_exchange_rate=scraped_data.get('average_exchange_rate'),
            owner=scraped_data.get('owner')
        )

        print(Currency.objects.all)