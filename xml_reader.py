import xml.etree.ElementTree as ET

def xmlreader(filename):
    labels = []
    startframes = []
    endframes = []
    startpoints = []
    endpoints = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        labels.append(child.attrib["name"])
        for c in child:
            if c.tag == 'Start_frame':
                startframes.append(c.text)
            elif c.tag == 'End_frame':
                endframes.append(c.text)
            elif c.tag == 'Start_point':
                startpoints.append(c.text)
            elif c.tag == 'End_point':
                endpoints.append(c.text)
    return labels, startframes, endframes