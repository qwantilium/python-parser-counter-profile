import xml.etree.ElementTree as ET
from inspect import isclass, getmembers


tree = ET.parse('профиль декабрь1.xml')
root = tree.getroot()

parser = ET.XMLPullParser(['start', 'end'])
parser.feed('<Element>{urn:schemas-microsoft-com:office:spreadsheet}Worksheet')

print(list(parser.read_events()))


a=root.findall("{*}ss:DataType")
print(a)

# for list in root.findall('Worksheet'):
#     print(list.text)





    # name = list.find('Лист:DHeader_FactoryNumber', ns)
    # number = list.find('Лист:DHeader_FactoryNumberVal', ns)
    # print(name.text, number.text)
    # for char in list.findall('role:character', ns):
    #     print(' |-->', char.text)
# for book in root:
#     print(book.get('ss:Name'))
# print(ET.tostring(root))
# for child in root:
#     print(ET.tostring(child.tag), child.attrib)
# book = root.find('Лист 1')


# for (name, members) in getmembers(ET, isclass):
#     print(name, members)

# print(book)