import xml.etree.ElementTree as ET

def xmlreader(filename):
    labels = []
    startframes = []
    endframes = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        labels.append(child.attrib["name"])
        for c in child:
            if c.tag == 'Start_frame':
                startframes.append(c.text)
            else:
                endframes.append(c.text)
    return labels, startframes, endframes