import os
import xml.dom.minidom
import xml.etree.ElementTree as ET

def main():
    f = open('tabele.html','w+')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<title>Tabelki Serwerow</title>\n')
    f.write('</head>\n')
    f.write('<body>\n')

    pliki = os.listdir('xmle')
    d = {}
    lista = []
    print(pliki)
    for plik in pliki:
        parsed = xml.dom.minidom.parse('xmle/'+plik)
        for child in parsed.getElementsByTagName("uptime"):
            uptime = child.childNodes[0].nodeValue
            intUptime = int(uptime)
            d[intUptime] = plik
            lista.append(intUptime)
            lista.sort()
            lista.reverse()

    for i in range(0, len(lista)):
        f.write('<table border="1" align="left" style="margin-left:50">\n')
        parsed = xml.dom.minidom.parse('xmle/'+d[lista[i]])
        tree = ET.parse('xmle/'+d[lista[i]])
        root = tree.getroot()
        for child in root:
                 f.write('<tr><td>' + child.tag + '</td>')
                 for child in parsed.getElementsByTagName(child.tag):
                      dane = child.childNodes[0].nodeValue
                      f.write('<td>' + dane + '</td></tr>\n')
        f.write('</table>\n')
    
    f.write('</body>\n')
    f.write('</html>\n')

if __name__ == "__main__":
    main()
