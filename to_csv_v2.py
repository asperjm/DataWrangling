import csv
import codecs
import pprint
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as soup 
import cerberus
from collections import defaultdict

data = []
# Read the XML file
with open("sample2.osm", "r", encoding="utf8") as file:
    # Read each line in the file, readlines() returns a list of lines
    data = file.readlines()
    # Combine the lines in the list into a string
    data = "".join(data)
    soup = soup(data, "lxml")



OSM_PATH = "sample2.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }   
    },
    'way_tags': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
   }
    


# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
# ['id', 'lat', 'lon', 'version', 'timestamp', 'changeset', 'uid', 'user']

#WAY_NODES_FIELDS = ['id', 'node_id', 'position']

#way_tags={}
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    # for n in element:
    #    print(n.items())
    node_attribs = {}
    node_tags ={}
    way_attribs = {}
    way_nodes = []
    n_tags = []
    way_t = {}
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    if element.tag =='node':
        #for x not in node_attr_fileds:
        for x in NODE_TAGS_FIELDS:
            #soup.find_all("tag", {'id'})
            node_tags[x] = element.attrib[x] if hasattr(element.attrib, x) else ''
    
        for f in node_attr_fields:
            node_attribs[f] = element.attrib[f]
            
        for node in element:
            if node.tag =='tag':
                node_tags={
                'id':element.attrib['id'],
                'key': node.attrib['k'], 
                'value':node.attrib['v'],
                'type':'regular'      
                }
           
            n_tags.append(node_tags)
            
    elif element.tag =='way':
        for a in WAY_TAGS_FIELDS:
            way_t[a] = element.attrib[a] if hasattr(element.attrib, a) else ''
            
        for w in way_attr_fields:
            way_attribs[w] = element.attrib[w]
   
        for node in element:
            if node.tag == 'tag':
                way_tags = {
                    'id': element.attrib['id'],
                    'key': node.attrib['k'],
                    'value': node.attrib['v'],
                    'type': 'regular'
                }
           
                tags.append(way_tags)
    
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': n_tags}
    elif element.tag == 'way':
        #print(way_tags)
        return{'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
#if element.tag == 'way':
                   
#         print(way_tags['id'])
        #new_way_tags = dict()
        #print(way_tags.items())
#         for x in way_tags:
#             new_way_tags[x.pop('id')] = x
#         print(new_way_tags)
        #print([[k, way_tags[k]] for k in way_tags.keys()])
        #print(way_tags)
        
    
   # print(way_attribs[w])
# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerows(self, row):
            #print("ROW:", row)
            super(UnicodeDictWriter, self).writerow({
           # k: (v.encode('utf-8') if not isinstance(v, bytes) else v) for k, v in row.items()})  
            k: v for k, v in row.items()})

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w',"utf-8") as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w', "utf-8") as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w', "utf-8") as ways_file, \
         codecs.open(WAY_TAGS_PATH, 'w', "utf-8") as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
       # way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    
                    for n_tag in el['node_tags']:
                        node_tags_writer.writerow(n_tag)
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                  
                    for tag in el['way_tags']:   
                        way_tags_writer.writerow(tag)
                  
if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)

