import os, glob
from lxml import etree
import re
import pandas as pd
import calendar
import locale
from datetime import date
from dateutil.relativedelta import relativedelta 
from datetime import datetime

# date settings
previous_month = date.today() + relativedelta(months=-1)
locale.setlocale(locale.LC_TIME, 'ru_RU')

# some trainee code
# with open("форпласт 2.html", "r") as file:
#     html_content = file.read()
#     tree = etree.HTML(html_content)


def get_sum_of_kw(tree):
    second_tds = tree.xpath("//tr/td[position()=2]")
    kw_int_list = []
    for el in second_tds:
        text = el.text
        kw_int_list.append(round(float(text.replace(',', '.')), 4))
    sum_of_kw = round(sum(kw_int_list), 4)
    return sum_of_kw
    # print(round(sum(kw_int_list), 4))


def number_of_counter(tree):
    string_counter_number = (tree.xpath("//h2")[0]).text
    for s in re.findall(r'\b(?!m\d+)\d{4,}\b', string_counter_number):
        numbers_list = int(s)
    return numbers_list
    # print (numbers_list)


def get_excel_file(data, counter, summ_kw):
    get_to_excel = pd.DataFrame(data)
    get_to_excel.to_excel(
        f"Показания Меркурий "
        f"{calendar.month_name[previous_month.month]} "
        f"{datetime.now().year}.xlsx", index=False)
    print(f'cчётчик {counter} записан в excel c суммой Квт {summ_kw}')


if __name__ == '__main__':
    data = []
    # Folder where collection of html files with profiles of counters
    folder_name = 'mercury'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Get a list of all HTML files in the folder
    folder_path = os.path.join(current_directory, folder_name)
    html_files = glob.glob(os.path.join(folder_path, '*.html'))
    # Loop through each HTML file and open it
    for file_path in html_files:
        with open(file_path, 'r') as file:
            html_content = file.read()
            # print(html_content)
            tree = etree.HTML(html_content)
            counter = number_of_counter(tree)
            summ_kw = get_sum_of_kw(tree)
            data.append({'Счетчик': counter, 'Сумма кВт профиля': summ_kw})
            get_excel_file(data, counter, summ_kw)
