import datetime
import pandas as pd

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint
from collections import defaultdict

current_date = datetime.date.today()
event_date = datetime.date(year=1920, month=1, day=1)

delta_years = current_date.year - event_date.year

def get_year_phrase(n: int) -> str:
    n = abs(n)
    if 11 <= n % 100 <= 14:
        word = "лет"
    else:
        last_digit = n % 10
        if last_digit == 1:
            word = "год"
        elif 2 <= last_digit <= 4:
            word = "года"
        else:
            word = "лет"
    return f"Уже {n} {word} с вами!"


df = pd.read_excel('wine2.xlsx')
df = df.fillna('')
result = defaultdict(list)
for _, row in df.iterrows():
    wine = {
        'Картинка': row['Картинка'],
        'Название': row['Название'],
        'Сорт': row['Сорт'],
        'Цена': row['Цена']
    }
    result[row['Категория']].append(wine)

pprint(result, sort_dicts=False)

wines = df.to_dict(orient='records')


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')
rendered_page = template.render(
    years_text=get_year_phrase(delta_years),
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

