import codecs
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.dom import pulldom
DOMTree = xml.dom.minidom.parse("data.xml")
collection = DOMTree.documentElement
