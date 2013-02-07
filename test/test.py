import os
import xml.dom.minidom
import xml.etree.ElementTree as ET

def main():
        pliki = os.listdir('xmle')
        d = {}
        lista = []
        print (pliki)
        for plik in  pliki:
            parsed = xml.dom.minidom.parse('xmle/'+plik)
            for child in parsed.getElementsByTagName("uptime"):
                uptime = child.childNodes[0].nodeValue
                intuptime = int(uptime)
                d[intuptime] = plik
                lista.append(intuptime)
                lista.sort()
                lista.reverse()
        print (lista)
        for i in range(0, len(lista)):
            parsed = xml.dom.minidom.parse('xmle/'+d[lista[i]])
            tree = ET.parse('xmle/'+d[lista[i]])
            root = tree.getroot()
            for child in root:
                for child in parsed.getElementsByTagName(child.tag):
                    dane = child.childNodes[0].nodeValue
                    print (dane)
            
                
if __name__ == '__main__':
    main()
