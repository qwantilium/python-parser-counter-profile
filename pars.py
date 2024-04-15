import xml.etree.ElementTree as ET
from lxml import etree

counters_list_inside = ['011793167151409',
                        '012643177507068']

forplast_counters = ['011793166143436',
                     '011793167151580',
                     '011793167151600',
                     '011793167151589',
                     '012289174709791',
                     ]
plastmassaperm = '012289174709928'
soloviev_counter = '009112172244601'

all_lists = {'counters_list_inside': ['011793167151409',
                                      '012643177507068'],
             'forplast': ['011793166143436',
                          '011793167151580',
                          '011793167151600',
                          '011793167151589',
                          '012289174709791',
                          ],
             'plastmassaperm': ['012289174709928'],
             'soloviev': ['009112172244601']}


types_of_data = ['Энергии на конец месяца', 'Профили нагрузки']
ns = {'_': 'urn:schemas-microsoft-com:office:spreadsheet',
      "ss": "urn:schemas-microsoft-com:office:spreadsheet",
      "o": "urn:schemas-microsoft-com:office:office",
      "x": "urn:schemas-microsoft-com:office:excel",
      "html": "http://www.w3.org/TR/REC-html40",
      "at": "urn:admintools:storage:exportinspreedsheet"}


tree = etree.parse('март 2024.xml')
root = tree.getroot()

elements = root.findall('ss:Worksheet', ns)
list_of_counters = []
for el in elements:
    counter_number = el.find(
        './/ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data', ns).text
    type_of_datasheet = el.find(
        './/ss:Cell[@ss:DataType="DHeader_DataTypeVal"]/ss:Data', ns).text
    data_rows = el.findall(
        './/ss:Row[@ss:TableType="DataMeasTable"][@ss:Session="0"]', ns)
    if type_of_datasheet == 'Энергии на конец месяца':
        print(el.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'],
              counter_number,
              type_of_datasheet)
        for row in data_rows:
            kilowatt_value_2 = row.find(
                './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
            print(kilowatt_value_2)
    elif type_of_datasheet == 'Месячные накопления энергии':
        print(el.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'],
              counter_number,
              type_of_datasheet)
        for row in data_rows:
            kilowatt_value_2 = row.find(
                './/ss:Cell[@ss:DataType="DMValue"]/ss:Data', ns).text
            print(kilowatt_value_2)
    else:
        list_of_counters.append(counter_number)

print([k for i, k in all_lists.items()])


def create_xml_with_worksheet(worksheet_node, output_file, new_tree):
    # Create a new XML tree with the worksheet node
    new_root = new_tree.getroot()
    new_root.append(worksheet_node)

    # Write the new ElementTree to a new XML file
    new_tree.write(output_file, xml_declaration=True, encoding="utf-8",
                   pretty_print=True)

    print(f"Файл с данными сохранен в {output_file}")


def parse_and_copy_xml(xml_file):
    #parse of xml file
    tree = etree.parse(xml_file)
    root = tree.getroot()
    # find all worksheets
    # elements=root.findall('ss:Worksheet', ns)
    # # create new empty xml file and stay just styles(delete all worksheets) 
    # empty_tree = etree.ElementTree(root)
    # empty_root=empty_tree.getroot()
    # delete_worksheets=empty_root.findall('ss:Worksheet', ns)
    # for delete in delete_worksheets:
    #     empty_root.remove(delete)


    for company in all_lists.keys():
        new_root = tree.getroot()
        elements=new_root.findall('ss:Worksheet', ns)
        for el in elements:
            counter_number=el.find('.//ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data', ns).text
            
            for counter in all_lists.values():
                if counter_number not in counter:       
                    new_root.remove(el)
                    print(f'удалили cчетчик {counter_number}')
                else:
                    pass
                    
        new_tree = etree.ElementTree(new_root)            
        new_tree.write(f'{company}.xml', xml_declaration=True, encoding="utf-8", pretty_print=True)
        print(f'сохранили элемент в файл {company}')

    #     print(f'сохранили элемент в файл {company}'
    # for company, counter_numbers in all_lists.items():
    #     new_tree = etree.ElementTree(empty_root)
    #     new_root=new_tree.getroot()
    #     for el in elements:
    #         counter_number=el.find('.//ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data', ns).text
            
    #         for counter in counter_numbers:
    #             if counter in counter_number:       
    #                 new_root.append(el)
    #                 print(f'Сохранили элемент счетчика {counter_number}')
    #                 break            
    #     new_tree.write(f'{company}.xml', xml_declaration=True, encoding="utf-8", pretty_print=True)
    #     print(f'сохранили элемент в файл {company}')

# if __name__ == '__main__':
#     parse_and_copy_xml('март 2024.xml')