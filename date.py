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
def pars_of_xml_get_elements(name_of_file):
    tree = ET.parse(name_of_file)
    root = tree.getroot()
    return root


# def get_kilowatt_value(el, data_rows, counter_number, type_of_datasheet,
#                        kilowatt_values):
#     print(el.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'],
#           counter_number, type_of_datasheet)
#     for row in data_rows[1:]:
#         kilowatt_value = row.find(
#             './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
#         kilowatt_values.append(kilowatt_value)
#     print(kilowatt_values, 'список кВт')
#     return kilowatt_values


def get_list_of_counters(root):
    counters = {}
    list_counters = []
    elements = root.findall('ss:Worksheet', ns)
    kilowatt_values = []
    dates = []
    for el in elements:
        # print(el)    
        type_of_datasheet = el.find(
         './/ss:Cell[@ss:DataType="DHeader_DataTypeVal"]/ss:Data',
         ns).text
        # print(type_of_datasheet)
        if type_of_datasheet in types_of_data:
            values = {}
            counter_number = el.find(
             './/ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data',
             ns).text
            data_rows = el.findall(
             './/ss:Row[@ss:TableType="DataMeasTable"][@ss:Session="0"]',
             ns)
            # print(counter_number)
            # append counter number to the list
            list_counters.append(counter_number)
            # parse date and kilowatt value
            for row in data_rows[1:]:
                kilowatt_value = row.find(
                                          './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
                date = row.find('.//ss:Cell[@ss:DataType="DMDate"]/ss:Data', ns).text
                dates.append(date)
                kilowatt_values.append(round(float(kilowatt_value.replace(',', '.')), 4))
                kilowatt_value = round(float(kilowatt_value.replace(',', '.')), 4)
                values[date] = kilowatt_value
                counters[counter_number] = values
    # print(counters)
    # print(len(list_counters), len(dates), len(kilowatt_values))
    # print(dates)
    # print(kilowatt_values)
    return counters
    # print(counters)
    # return counters


def collect_to_excel(counters):
    name_file = (f"Показания Энергомера "
                 f"{calendar.month_name[previous_month.month]} "
                 f"{datetime.now().year}.xlsx")
    # sorting dates
    all_dates = set()
    for dates_values in counters.values():
        all_dates.update(dates_values.keys())
    all_dates = sorted(all_dates)
    print(all_dates)
    # create a data frame
    df = pd.DataFrame(index=counters.keys(), columns=all_dates)
    for counter, dates_values in counters.items():
        for date_of_value, kilowatt_value in dates_values.items():
            df.at[counter, date_of_value] = kilowatt_value
    df.index.name = 'Счетчики'
    writer = pd.ExcelWriter(name_file, engine='xlsxwriter')
    # write the data frame to Excel
    df.to_excel(writer, sheet_name='Лист1')
    # get the XlsxWriter workbook and worksheet objects
    # workbook = writer.book
    worksheet = writer.sheets['Лист1']
    worksheet.autofit()
    # save the Excel file
    writer.close()

    print(f'Файл {name_file} записан"')
    print(df)


if __name__ == '__main__':
    root = pars_of_xml_get_elements('май 2024.xml')
    data2 = get_list_of_counters(root)
    collect_to_excel(data2)
