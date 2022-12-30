from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas as pd
from collections import defaultdict
import argparse


def parse_args():
    """Спарсить аргументы с командной строки"""

    parser = argparse.ArgumentParser(description='Конструируем сайт по продаже алкоголя')
    parser.add_argument('data_path', default='./drinks_info.xlsx', help='Путь к файлу с данными')
    parser.add_argument('--foundation_year', default=1920, type=int, help='Год основания компании')
    args = parser.parse_args()
    return args


def generate_correct_age_form(age: int) -> str:
    """Скорректировать форму слова ГОД для указания возраста фирмы"""

    if age % 100 in (11, 12, 13, 14):
        return 'лет'
    elif age % 10 == 1:
        return 'год'
    elif age % 10 in (2, 3, 4):
        return 'года'
    else:
        return 'лет'


def main():

    args = parse_args()
    foundation_year = args.foundation_year
    path_to_current_stock = args.data_path
    company_age = datetime.now().year - foundation_year
    age_form = generate_correct_age_form(company_age)

    wines = pd.read_excel(path_to_current_stock, keep_default_na=False)
    wines['Цена'] = wines['Цена'].astype(int)
    wines = wines.to_dict(orient='records')

    drinks = defaultdict(list)
    for wine in wines:
        drinks[wine['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        company_age=company_age,
        age_form=age_form,
        drinks=drinks.items()
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()