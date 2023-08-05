import json
from xml.etree.ElementTree import iterparse


def relations(json_file_path):
    "reads a sped specification file and return a children-to-parent mapping"
    with open(json_file_path) as f:
        data = json.load(f)
    return dict((i['name'], i['parent_record']) for i in data)


def build_relations_from_xml(filepath):
    "reads a xml specification (PVA) and return a child-to-parent mapping"
    hierarchy = {}
    records = []
    for (event, node) in iterparse(filepath, events=['start', 'end']):
        if event == 'start' and node.tag == 'registro':
            records.append(node.attrib['id'])
        if event == 'end' and node.tag == 'registro':
            child = records.pop()
            try:
                parent = records[-1]
            except IndexError:
                parent = None
            hierarchy[child] = parent
    return hierarchy
