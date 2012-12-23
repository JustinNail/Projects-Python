import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
print ("Root = ",root)
print ("Root Tag = ", root.tag)
print ("Root Attribute = ", root.attrib)
print ("Children:")
for child in root:
    print("\tTag: ",child.tag," Attributes: ",child.attrib)
