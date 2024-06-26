import xml.etree.ElementTree as ET
import copy
import calendar
import locale
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime


# month setteings(language and previous month)
previous_month = date.today() + relativedelta(months=-1)
locale.setlocale(locale.LC_TIME, 'ru_RU')


# Dict of counters for different companies
all_lists = {'ТП 70': ['011793167151409',
                       '012643177507068'],
             'Форпласт': ['011793166143436',
                          '011793167151580',
                          '011793167151600',
                          '011793167151589',
                          '012289174709791',
                          ],
             'Пластмасса Пермь': ['012289174709928'],
             'Соловьев': ['009112172244601'],
             'Храмушина': ['012289198809411'],
             'Туева': ['012643188307856']}

# Namespaces lists
ns = {'_': 'urn:schemas-microsoft-com:office:spreadsheet',
      "ss": "urn:schemas-microsoft-com:office:spreadsheet",
      "o": "urn:schemas-microsoft-com:office:office",
      "x": "urn:schemas-microsoft-com:office:excel",
      "html": "http://www.w3.org/TR/REC-html40",
      "at": "urn:admintools:storage:exportinspreedsheet"}


def pars_of_xml(name_of_file):
    tree = ET.parse(name_of_file)
    root = tree.getroot()
    return root


def delete_worksheets(root):
    for el in root.findall('ss:Worksheet', ns):
        root.remove(el)


def separate_for_companies(root, copy_root):
    for company, counter_numbers in all_lists.items():
        empty_root = copy.deepcopy(root)
        for el in copy_root.findall('ss:Worksheet', ns):
            counter_number = el.find(
                './/ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data',
                ns).text
            print(counter_number)
            for number in counter_numbers:
                if number == counter_number:
                    empty_root.append(el)
                    new_tree = ET.ElementTree(empty_root)
                    new_tree.write(
                        f'{company} '
                        f'{calendar.month_name[previous_month.month]} '
                        f'{datetime.now().year}.xml',
                        xml_declaration=True, encoding="utf-8")
                    # new_tree.write(
                    #     f'{company} '
                    #     f'24.04 и 05.05 '
                    #     f'{datetime.now().year}.xml',
                    #     xml_declaration=True, encoding="utf-8")
                    # print(f'{counter_number} записан в {company}')
                else:
                    print('счетчик не в спике')


if __name__ == '__main__':
    root = pars_of_xml('май 2024(no doubles).xml')
    copy_root = copy.deepcopy(root)
    delete_worksheets(root)
    separate_for_companies(root, copy_root)
