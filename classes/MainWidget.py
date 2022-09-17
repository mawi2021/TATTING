from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QHBoxLayout, QFileDialog
from PyQt5 import QtSvg
from PyQt5.QtCore import Qt
from os.path import exists
import re  # regular expressions)"/> 
import math
import ctypes # for messages
import json

# TODO:
# - Text in formatted HTML instead of plain text
# - HTML formatting in config file (font size, font color, font family)

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # ----- Constants ----------------------------------------------------------------------- #
        # TODO: read values from config file
        self.top = 50
        self.left = 50
        self.width = 1400
        self.height = 1000

        # Instruction as Text #
        self.textWidget = QTextEdit()
        self.txtFilename = ''

        # Instruction as SVG Image #
        self.svgWidget = QtSvg.QSvgWidget() #"samples/t_001.svg")
        self.svgWidget.setGeometry(50,50,759,668)
        self.svgFilename = ''

        # Combine Instructions with Splitter
        designSplitter = QSplitter(Qt.Horizontal)
        designSplitter.addWidget(self.textWidget)
        designSplitter.addWidget(self.svgWidget)
        designSplitter.setSizes([50,150])

        hbox = QHBoxLayout()
        hbox.addWidget(designSplitter)
        self.layout = hbox
        self.setLayout(self.layout)

    def onOpen(self):
        # Reguest filename #
        fileDlg = QFileDialog()
        fileStruc = fileDlg.getOpenFileName( 
                        self.parent, 'Choose a file with instructions (text)', "samples/"
                    )

        # Stop if nothing chosen #
        if fileStruc[0] == "":
            return

        # Set filenames #
        self.txtFilename = fileStruc[0]
        pos = self.txtFilename.rfind('.')
        if pos >= 0:
            self.svgFilename = self.txtFilename[:pos+1] + 'svg'
        else:
            self.svgFilename = self.txtFilename + '.svg'

        # Read text file and assign content #
        with open(self.txtFilename, encoding="utf-8") as f:
            instr = ''
            for line in f.readlines():
                instr = instr + line
            self.textWidget.setPlainText(instr)
        f.close()

        # Show SVG file #
        if exists(self.svgFilename):
            self.svgWidget.load(self.svgFilename)

    def onRedraw(self):
        # ----- Constants ----------------------------------------------------------------------- #
        self.elems = []
        self.picot = {}
        self.scale = 25
        self.grid = 'yes' # String!

        # ----- Read and Write SVG File --------------------------------------------------------- #
        content = self.textWidget.toPlainText()
        lines = content.split('\n')
        
        self._create_meta(lines)
        for line in lines:
            self._add(line)
        self._add_closure()

        # Show SVG file #
        if exists(self.svgFilename):
            self.svgWidget.load(self.svgFilename)

    def onSave(self):
        content = self.textWidget.toPlainText()
        
        with open(self.txtFilename, 'w', encoding="utf-8") as f:
            f.write(content)
        f.close() 


    # ===== PRIVATE PART OF CLASS =============================================================== #
    def _create_meta(self, lines):
        # Search for Meta-Information
        for line in lines:
            if len(line) == 0 or line[0] == '#': continue
            pos = line.find(':')
            if pos == -1:
                if line[:5] == 'grid=':
                    self.grid = line[5:]

        with open(self.svgFilename, 'w', encoding="utf-8") as f:
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

            if self.grid == 'yes':
                for i in range(100):
                    f.write('<line x1="' + str(i*20) + '"   y1="0" x2="' + str(i*20) + '"   y2="2000" stroke="lightgrey" stroke-width="1px" />\n')

                f.write('<!-- Waagerechte -->\n')
                for i in range(100):
                    f.write('<line y1="' + str(i*20) + '"   x1="0" y2="' + str(i*20) + '"   x2="2000" stroke="lightgrey" stroke-width="1px" />\n')

            # Read basic elements from /config/basic_elements.svg file and replace it here
            found = False
            next_is_coord = False
            fig_id = ''
            f.write('<!-- Grundelemente -->\n')
            with open('config/basic_elements.svg', 'r', encoding="utf-8") as fr:                
                for line in fr.readlines():
                    if line == '' or line == '\n':
                        continue

                    if next_is_coord:
                        line = line[+4:-4]
                        coord_arr = line.split(' ')
                        self.picot[fig_id] = []
                        first = True
                        for coord in coord_arr:
                            coord = json.loads(coord)
                            if first:
                                dx = coord[0]
                                dy = coord[1]
                                element = {}
                                element["id"] = fig_id
                                element["dx"] = dx
                                element["dy"] = dy
                                element["nodes"] = 1
                                self.elems.append(element)
                                first = False
                                continue
                            self.picot[fig_id].append(coord)
                        next_is_coord = False
                        continue

                    if line.startswith('<!-- ### START PART TO BE COPIED ### -->'):
                        found = True
                        continue
                    if line.startswith('<!-- ### END PART TO BE COPIED ### -->'):
                        found = False
                        continue
                    if not found: continue
                    f.write(line)
                    reg = re.search('id=\"[^\"]*\"', line)
                    if reg == None: continue
                    fig_id = reg.group(0)
                    fig_id = fig_id[4:-1]
                    next_is_coord = True
            fr.close()

            f.write('\n<!-- Individueller Teil -->\n')
        f.close()
    def _add_closure(self):
        with open(self.svgFilename, 'a', encoding="utf-8") as f:
            f.write('</svg>')
        f.close()            
    def _add(self,line):
        if len(line) == 0: return
        if line[0] == '#': return

        # Parse line
        element = {}
        regexp = '\{[-]*[0-9]+\}'
        coord_x = coord_y = -1

        # Search for id, figure variant, definition, output coordinates
        pos = line.find(':')

        if pos == -1:
            return

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
       
        # Ring (start + end on top) or Chain with mid on top (start left) #
        if element["id"][0] in ('R', 'c', 'C'):
            scale = element["nodes"] / self.scale # size of figure
            figure = element["id"][0] + element["variant"]
            for el in self.elems:
                if el["id"] == figure:
                    element["dx"] = scale * int(el["dx"])
                    element["dy"] = scale * int(el["dy"])
                    exit

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
                    idx = int(round((len(self.picot[figure])-2) * pos / element["nodes"])) - 1
                    place = self.picot[figure][idx]
                    if el == 'P':
                        scale_picot = scale
                    elif el == 'p':
                        scale_picot = scale / 2
                    x = scale * float(place[0])
                    y = scale * float(place[1])
                    line = line + '   <use transform="translate(' + str(x) + ' ' + str(y) + \
                        ') rotate(' + str(place[2]) + ') scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')" xlink:href="#picot"/>\n'

            line = line + '</g>\n'

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

        with open(self.svgFilename, 'a', encoding="utf-8") as f:
            f.write(line)
            # Final auszugebende Figur #
            if coord_x >= 0 and coord_y >= 0: #element["id"][0] == 'Z':
                f.write('<!-- Ausgabe -->\n')
                f.write('<g stroke="black" fill="none" stroke-width="1" stroke-linecap="round">')
                f.write('<use transform="translate(' + str(coord_x) + ' ' + str(coord_y) + ')" xlink:href="#' + element["id"] + '"/>')
                f.write('</g>\n')
        f.close() 

        self.elems.append(element)