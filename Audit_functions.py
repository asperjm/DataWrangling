import os
from xml.etree import cElementTree as ET
from collections import defaultdict
import pprint
import re
# Import BeautifulSoup
from bs4 import BeautifulSoup as bs


data = []
# Read the XML file
with open("sample2.osm", "r", encoding="utf8") as file:
    # Read each line in the file, readlines() returns a list of lines
    data = file.readlines()
    # Combine the lines in the list into a string
    data = "".join(data)
    soup = bs(data, "lxml")


file_name = 'sample2.osm'
doc_path = os.path.join(file_name)
file_path = os.path.abspath(os.path.join(file_name))
osm_file = open("sample2.osm", encoding="utf8")
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_typesw = defaultdict(set)
street_types = defaultdict(int)




def basic_audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1


#def audit_street_type(street_types, street_name):
#    m = street_type_re.search(street_name)
#    if m:
#        street_type = m.group()
#        if street_type not in expected:
#            street_types[street_type].add(street_name)
# Looks at the expected list, and returns a dictionary of names that does not match the expected list appove. 

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print("%s: %d" % (k, v)) 
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def basic_audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1
# This function will show us what different names streets in Reno have been given.

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            basic_audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)



file_name = 'sample2.osm'
def find_pc_k(elem):
    return (elem.attrib['k'] =='addr:postcode')
       # will show all postal codes in the data set.

def find_tags():
    for event, elem in ET.iterparse(file_name, events =("start",)):
        if elem.tag =='node':
            for tag in elem.iter('tag'):
                  if find_pc_k(tag):
                    print(tag.attrib['k'], tag.attrib['v'])
                    #return tag.attrib['k'], tag.attrib['v']

                
if __name__ == '__main__':
    audit()   
    find_tags()
    
;
