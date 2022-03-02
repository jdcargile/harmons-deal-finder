import datetime
from email.utils import format_datetime
from pydoc import cli
import click
import requests
import os
import locale

@click.group()
def main():
    """ Simple CLI that will get you the best deals at Harmons Grocery"""
    pass


@main.command()
@click.argument('search_term')
@click.option('--discount-only', is_flag=True, help='Only show deals with a discount')
@click.option('--vegan', is_flag=True, help='Only show deals that are vegan')
@click.option('--discount-percentage-highlight', default=0, help='Show all deals with a discount, but highlight deals with a discount greater than this percentage')
# TODO: Add a flag to show deals with a discount greater than this percentage
# @click.option('--discount-percentage', default=0, help='Only show deals with a discount greater than this percentage')

def search(search_term, discount_only, vegan, discount_percentage_highlight):
    """Get deals on a search term"""

    locale.setlocale( locale.LC_ALL, '' )

    url = f'https://shop.harmonsgrocery.com/api/v2/store_products?limit=1000&search_provider=buffet&search_term={search_term}&secondary_results=false&sort=popular'

    if discount_only:
        url = f'{url}&tags=on_sale'

    if vegan:
        url = f'{url}&tags=vegan_friendly'

    resp = callApi(url)

    deals = resp.json()['items']

    for deal in deals:
        sale_price = 0
        sale_percentage = 0

        click.secho(f'{deal["name"]} ', fg="green", bold=True) 
        click.secho(f'  Price: ${deal["base_price"]}')

        if isinstance(deal['sale_price'], float):
            sale_price = locale.currency(deal['base_price'] - deal['sale_price'], grouping=True)
            sale_percentage = round((deal["base_price"] - deal["sale_price"]) / deal["base_price"] * 100)
            if sale_percentage > discount_percentage_highlight and discount_percentage_highlight != 0:
                click.secho(f'  Sale Price: ${deal["sale_price"]} ({sale_price} {sale_percentage}%)', fg="red", bold=True)
                click.secho(f'  Sale End: {deal["sale_end_date"]} ')
            else:
                click.secho(f'  Sale Price: ${deal["sale_price"]} ({sale_price} {sale_percentage}%)')
                click.secho(f'  Sale End: {deal["sale_end_date"]} ')

        click.secho(f'  Aisle: {deal["aisle"]} ')
    
    click.secho(f"\n{resp.json()['item_count']} deals for search term {search_term}", fg="cyan")

def callApi(url):
    token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2Vyc2Vzc2lvbl9pZCI6MTg3MjIxNzYsInVzZXJfaWQiOjIyNjM3NTcsImFkbWludXNlcl9pZCI6bnVsbCwiYW5vbnltb3VzIjp0cnVlLCJpYXQiOjE2MDY3NDc0NjF9.nDhi_bDVIVNY_ac9nh3FpVQc1Jxl7D-J_iKSsPalocc"
    bearerToken = f'Bearer {token}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken 
        }

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        resp.raise_for_status()
    return resp

if __name__ == "__main__":
    main()