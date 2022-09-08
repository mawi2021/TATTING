# Run: C:\Users\D026557\AppData\Local\Programs\Python\Python39\python.exe main.py
import re  # regular expressions)"/> 
import math
import ctypes # for messages

# TODO:
#   Koordinaten für Picot-Ansatzpunkte in config/basic_elements.svg in Kommentare auslagern und entsprechend einlesen
#   Schmalere Ringe >> Picot-Positionen Koordinatenliste erstellen
#   Picots auf Bögen
#   Abfrage nach Dateiname statt statisch im Programm
#   Parameter zum Aussehen, bspw. 
#   - bei Ausgaben Farbe mitgeben
#   - bei Ausgaben Strichstärke mitgeben
#   - Grid anzeigen/unterdrücken
#   - "Name" oder "Nummer" einer Figur mitgeben, die bei der Ausgabe in/nahe der Figur ausgegeben wird
#   - Anzahl Knoten in Figur-Abschnitte als Zahl eintragen
#   Grid mit Millimerachse passend machen
#   Anpassung Bildgröße (xmax, ymax) entsprechend der ausgegebenen Objekte oder Eingabe der Länge/Breite durch den User
#   Kommentare im Code in Englisch
#   "Zahlen" h´für Berechnungen als Konstanten und ggf. Auslagern in Konfigurationsdatei
#   Grafische Oberfläche
#   Deploy to new GIT Project

class Main():
    def __init__(self):
        self.elems = []
        self.filename = "samples/t_001."
        self.scale_b = 0.69
        self.scale_c = 0.49
        # Bezieht sich auf einen Ring der Form a mit Spitze bei (0,0), x in {-40,40} und y in {0,100}
        # Angabe Tripel [x, y, winkel (in Grad)], wie das Picot am Ring (außen) klebt
        # Erstellung per Augenmaß. Im besseren Fall sollte dies an jeweils gleichgroßen Bogensegmenten passieren oder gar 
        # allgemeingültig berechnet werden, was ggf. bei zusammengesetzten Grundfiguren problematisch wäre
        self.picotA = []
        self.picotA.append([0,0,135])
        self.picotA.append([-6,5,135])
        self.picotA.append([-12,10,135])
        self.picotA.append([-18,15,135])
        self.picotA.append([-23,20,130])
        self.picotA.append([-27,25,125])
        self.picotA.append([-31,30,125,])
        self.picotA.append([-34,35,120,])
        self.picotA.append([-36,40,115])
        self.picotA.append([-38,45,110])  
        self.picotA.append([-39,50,105])
        self.picotA.append([-40,55,98])
        self.picotA.append([-40,60,90])
        self.picotA.append([-40,65,85])
        self.picotA.append([-39,70,78])
        self.picotA.append([-37,75,72])        
        self.picotA.append([-35,80,64])
        self.picotA.append([-32,85,55])
        self.picotA.append([-27,90,45])
        self.picotA.append([-22,93,35])
        self.picotA.append([-17,96,25])
        self.picotA.append([-12,98,15])   
        self.picotA.append([-6,99,10])        
        self.picotA.append([0,100,0])        
        self.picotA.append([6,99,350])    
        self.picotA.append([12,98,345])
        self.picotA.append([17,96,335])
        self.picotA.append([22,93,325])
        self.picotA.append([27,90,315])
        self.picotA.append([32,85,305])
        self.picotA.append([35,80,296])
        self.picotA.append([37,75,288])
        self.picotA.append([39,70,282])
        self.picotA.append([40,65,275])
        self.picotA.append([40,60,270])
        self.picotA.append([40,55,262])
        self.picotA.append([39,50,255])
        self.picotA.append([38,45,250])
        self.picotA.append([36,40,245])
        self.picotA.append([34,35,240])
        self.picotA.append([31,30,235])
        self.picotA.append([27,25,235])
        self.picotA.append([23,20,230])
        self.picotA.append([18,15,225])
        self.picotA.append([12,10,225])
        self.picotA.append([6,5,225])
        self.picotA.append([0,0,225])

        self.create_meta()
        
        with open(self.filename+'txt', encoding="utf-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                self.add(line)
        f.close()

        self.add_closure()
    def create_meta(self):
        with open(self.filename+'svg', 'w', encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<svg xmlns="http://www.w3.org/2000/svg"\n')
            f.write('    xmlns:xlink="http://www.w3.org/1999/xlink"\n')
            f.write('    version="1.1" baseProfile="full"\n')
            f.write('    width="500mm" height="500mm"\n')
            f.write('    viewBox="-20 -20 700 700">\n')
            f.write('    <title>Titel der Datei</title>\n')
            f.write('    <desc>Beschreibung/Textalternative zum Inhalt.</desc>\n')
            f.write('\n<!--Inhalt der Datei -->\n')
            f.write('\n<!-- Koordinatensystem -->\n')
            f.write('<!-- Senkrechte -->\n')

            for i in range(100):
                f.write('<line x1="' + str(i*20) + '"   y1="0" x2="' + str(i*20) + '"   y2="2000" stroke="lightgrey" stroke-width="1px" />\n')

            f.write('<!-- Waagerechte -->\n')
            for i in range(100):
                f.write('<line y1="' + str(i*20) + '"   x1="0" y2="' + str(i*20) + '"   x2="2000" stroke="lightgrey" stroke-width="1px" />\n')

            # Read basic elements from /config/basic_elements.svg file and replace it here
            found = False
            f.write('<!-- Grundelemente -->\n')
            with open('config/basic_elements.svg', 'r', encoding="utf-8") as fr:
                for line in fr.readlines():
                    if line.startswith('<!-- ### START PART TO BE COPIED ### -->'):
                        found = True
                        continue
                    if line.startswith('<!-- ### END PART TO BE COPIED ### -->'):
                        found = False
                        continue
                    if not found: continue
                    f.write(line)
            fr.close()

            f.write('\n<!-- Individueller Teil -->\n')
        f.close()
    def add_closure(self):
        with open(self.filename+'svg', 'a', encoding="utf-8") as f:
            f.write('</svg>')
        f.close()            


    def add(self,line):
        if len(line) == 0: return
        if line[0] == '#': return

        # Parse line
        element = {}
        regexp = '\{[-]*[0-9]+\}'
        coord_x = coord_y = -1

        # Search for id, figure variant, definition, output coordinates
        pos = line.find(':')
        element["id"] = line[:pos].strip()
        # Variant of ring or chain (a, b, c, ...)
        pos1 = element["id"].find('[')
        pos2 = element["id"].find(']')
        if pos1 >= 0 and pos2 >= 0:
            element["variant"] = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
        else:
            if element["id"][0] in ('R', 'C', 'c'):
                element["variant"] = 'a'
        element["def"] = line[pos+1:].strip()
        # Output coordinates if available
        pos1 = element["id"].find('(')
        pos2 = element["id"].find(')')
        if pos1 >= 0 and pos2 >= 0:
            coords = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
            pos = coords.find(',')
            coord_x = int(coords[:pos])
            coord_y = int(coords[pos+1:])
        
        # How many nodes (including picots)?
        seq = element["def"]
        seq = seq.replace("p","1")
        seq = seq.replace("P","1")
        seq = seq.replace(" ","+")
        for e in self.elems:
            seq = seq.replace(e["id"],str(e["nodes"]))
        seq = re.sub(regexp, '', seq, 0, 0)
        try:
            element["nodes"] = eval(seq)
        except NameError:
            ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                '\nAn expression in this line is not yet defined', 'Error', 0)
            exit()
        except SyntaxError:
            ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                '\nSyntax error, e.g. check space, colons and brackets', 'Error', 0)
            exit()
       
        # Ring (start + end on top) #
        if element["id"][0] == 'R': 
            scale = element["nodes"] / 100
            element["dx"] = 0
            element["dy"] = 0
            if element["variant"] == 'a':
                figure = 'ring1'
            elif element["variant"] == 'b':
                figure = 'ring2'
            elif element["variant"] == 'c':
                figure = 'ring3'
            else:
                ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                  '\nExpected one of the variants "a", "b" or "c" as second character instead of ' + element["id"][1], 'Error', 0)
                exit()

            line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round">\n' + \
                    '   <use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#' + figure + '"/>\n'
            # Picots?
            seq = element["def"].split(' ')
            pos = 0
            for el in seq:
                try:
                    pos = pos + int(el)
                except:
                    # calculate coords, where to add
                    pos = pos + 1
                    idx = int(round(46 * pos / element["nodes"])) - 1 # 46 = number of entries in self.picotA
                    place = self.picotA[idx]
                    if el == 'P':
                        scale_picot = scale
                    elif el == 'p':
                        scale_picot = scale / 2
                    line = line + '   <use transform="translate(' + str(scale*place[0]) + ' ' + str(scale*place[1]) + \
                        ') rotate(' + str(place[2]) + ') scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')" xlink:href="#picot"/>\n'

            line = line + '</g>\n'

        # Chain with mid on top (start left) #
        elif element["id"][0] == 'C':
            scale = element["nodes"] / 50
            element["dx"] = 120 * scale
            element["dy"] = 0
            if element["variant"] == 'a':
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain1"/></g>\n'
            elif element["variant"] == 'b':
                element["dx"] = element["dx"] * self.scale_b
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain3"/></g>\n'
            elif element["variant"] == 'c':
                element["dx"] = element["dx"] * self.scale_c
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain5"/></g>\n'
        # Chain with mid at the bottom (start left) #
        elif element["id"][0] == 'c':
            scale = element["nodes"] / 50
            element["dx"] = 120 * scale
            element["dy"] = 0
            if element["variant"] == 'a':
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain2"/></g>\n'
            elif element["variant"] == 'b':
                element["dx"] = element["dx"] * self.scale_b
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain4"/></g>\n'
            elif element["variant"] == 'c':
                element["dx"] = element["dx"] * self.scale_c
                line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round"><use transform="scale(' + str(scale) + ' ' + str(scale) + ')" xlink:href="#chain6"/></g>\n'
        # (Teil-) Figuren #
        else:
            dx = 0
            dy = 0
            line = '<g id="' + element["id"] + '" fill="none" stroke-linecap="round">'
            lst = element["def"].split(" ")
            for le in lst:
                regex = re.search(regexp, le)
                if regex:
                    grad = float(regex.group(0)[1:-1])
                    rad = math.radians(grad)
                else: 
                    grad = 0
                    rad = 0
                le = re.sub(regexp, '', le, 0, 0)
                line = line + '<use xlink:href="#' + le + '" transform="translate(' + str(dx) + ' ' + str(dy) + ')  rotate(' + str(grad) + ')"/>'

                # Get le-Element for dx and dy calculation #
                for el in self.elems:
                    if el["id"] == le:
                        dx = dx + el["dx"] * math.cos(rad) - el["dy"] * math.sin(rad)
                        dy = dy + el["dx"] * math.sin(rad) + el["dy"] * math.cos(rad)

            line = line + '</g>\n'
            element["dx"] = dx
            element["dy"] = dy

        with open(self.filename+'svg', 'a', encoding="utf-8") as f:
            f.write(line)
            # Final auszugebende Figur #
            if coord_x >= 0 and coord_y >= 0: #element["id"][0] == 'Z':
                f.write('<!-- Ausgabe -->\n')
                f.write('<g stroke="black" fill="none" stroke-width="1" stroke-linecap="round">')
                f.write('<use transform="translate(' + str(coord_x) + ' ' + str(coord_y) + ')" xlink:href="#' + element["id"] + '"/>')
                f.write('</g>\n')
        f.close() 

        self.elems.append(element)


if __name__ == "__main__":
    Main()