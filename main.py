from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas as pd
from collections import defaultdict
from pprint import pprint


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


def calculate_company_age(year_of_foundation: int) -> int:
    """Подсчитать возраст фирмы"""

    return datetime.now().year - year_of_foundation


year_of_foundation = 1920
path_to_current_stock = './wine3.xlsx'
company_age = calculate_company_age(year_of_foundation)
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