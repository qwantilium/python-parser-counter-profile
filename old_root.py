from lxml import etree

old_root = '''<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook></Workbook>
'''

# parser = etree.XMLParser(ns_clean=True)
# xml_root = etree.fromstring(old_root, parser)
# new_tree = etree.ElementTree(xml_root)
# new_tree.write('new_new_xml.xml', encoding="utf-8", pretty_print=True)

ns = {'_':'urn:schemas-microsoft-com:office:spreadsheet', "ss": "urn:schemas-microsoft-com:office:spreadsheet", "o":"urn:schemas-microsoft-com:office:office",
 "x":"urn:schemas-microsoft-com:office:excel", "html":"http://www.w3.org/TR/REC-html40",
 "at":"urn:admintools:storage:exportinspreedsheet"}

tree = etree.parse('ПС Дальняя ноябрь.xml')
root = tree.getroot()
styles = root.find('.//Styles', ns)
