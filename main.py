
from lxml import etree

def parseWorkSheet(element):
    device_identifier = element.xpath('.//ss:Cell[@ss:DataType="DHeader_FactoryNumberVal"]/ss:Data/text()', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"})[0]
    device_type = element.xpath('.//ss:Cell[@ss:DataType="DHeader_DataTypeVal"]/ss:Data/text()', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"})[0]
    print(device_identifier, device_type)

    data_rows = element.xpath('.//ss:Row[@ss:TableType="DataMeasTable"]', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"})
    for row in data_rows:
        date = row.xpath('.//ss:Cell[@ss:DataType="DMDate"]/ss:Data/text()', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"})
        value = row.xpath('.//ss:Cell[@ss:DataType="DMValue"]/ss:Data/text()', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"})
        if len(date) == 0 or len(value) == 0:
            continue
        print(date[0], value[0])
    # print( element.xpath('//ss:Cell', namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}) )


def extract_data_from_xml(xml_file_path, xpath_query):
    tree = etree.parse(xml_file_path)
    for element in tree.xpath('//_:Worksheet', namespaces = {"_":"urn:schemas-microsoft-com:office:spreadsheet", "ss": "urn:schemas-microsoft-com:office:spreadsheet"}):
        parseWorkSheet(element)

if __name__ == '__main__':
    print (extract_data_from_xml('профиль декабрь1.xml', '//Workbook'))
