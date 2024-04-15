import calendar
import locale
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd

# month setteings(language and previous month)
previous_month = date.today() + relativedelta(months=-1)
locale.setlocale(locale.LC_TIME, 'ru_RU')

# lists of data for comparing and namespaces
types_of_data = ['Энергии на конец месяца', 'Месячные накопления энергии']
ns = {'_': 'urn:schemas-microsoft-com:office:spreadsheet',
      "ss": "urn:schemas-microsoft-com:office:spreadsheet",
      "o": "urn:schemas-microsoft-com:office:office",
      "x": "urn:schemas-microsoft-com:office:excel",
      "html": "http://www.w3.org/TR/REC-html40",
      "at": "urn:admintools:storage:exportinspreedsheet"}


# tree = ET.parse('март 2024.xml')
# root = tree.getroot()
def pars_of_xml(name_of_file):
    tree = ET.parse(name_of_file)
    root = tree.getroot()
    return root


def get_list_of_data(root):
    elements = root.findall('ss:Worksheet', ns)
    list_of_counters = []
    summarize_of_profiles = {}
    summary_of_KW = []
    kilowatt_values = []
    data = []
    for el in elements:
        counter_number = el.find(
        './/ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data', ns).text
        type_of_datasheet = el.find(
        './/ss:Cell[@ss:DataType="DHeader_DataTypeVal"]/ss:Data', ns).text
        data_rows = el.findall(
        './/ss:Row[@ss:TableType="DataMeasTable"][@ss:Session="0"]', ns)
        if type_of_datasheet in types_of_data:
            print(el.attrib[
                '{urn:schemas-microsoft-com:office:spreadsheet}Name'],
              counter_number, type_of_datasheet)
            for row in data_rows[1:]:
                kilowatt_value = row.find(
                    './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
                kilowatt_values.append(kilowatt_value)
                print(kilowatt_value)
        else:
            list_of_counters.append(counter_number)
            kw_list = []
            kw_int_list = []
            for row in data_rows[1:]:
                kilowatt_value_2 = row.find(
                    './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
                kw_list.append(kilowatt_value_2)
            for kw in kw_list[1:]:
                kw.replace(',', '.')
                kw_int_list.append(round(float(kw.replace(',', '.')), 4))
                summary_of_KW.append(round(sum(kw_int_list), 4))
            # print(round(sum(kw_int_list), 4))
            # print(list_of_counters)      
        # print(summary_of_KW)
        for i in range(len(list_of_counters)):
            summarize_of_profiles[list_of_counters[i]] = summary_of_KW[i],
            kilowatt_values[i]

    for key, value in summarize_of_profiles.items():
        data.append({'Счетчик': key,
                     'Сумма кВт профиля': value[0],
                     'показания': value[1]})
    return data


def collect_to_excel(data):
    get_to_excel = pd.DataFrame(data)
    get_to_excel.to_excel(f"Показания Энергомера "
                          f"{calendar.month_name[previous_month.month]} "
                          f"{datetime.now().year}.xlsx", index=False
                          )


if __name__ == '__main__':
    root = pars_of_xml('март 2024.xml')
    data = get_list_of_data(root)
    collect_to_excel(data)
