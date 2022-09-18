from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QHBoxLayout, QFileDialog, QScrollArea
from PyQt5 import QtWidgets
from PyQt5 import QtSvg
from PyQt5.QtCore import Qt
#from os.path import exists
import re  # regular expressions)"/> 
import math
import ctypes # for messages
import json

# TODO:
# - Text in formatted HTML instead of plain text
# - HTML formatting in config file (font size, font color, font family)
# - Numbers and names of figures written
# - Graphical elements created by drag&drop via icons in toolbox-bar

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # ----- Constants ----------------------------------------------------------------------- #
        # TODO: read values from config file
        self.elems = []
        self.picot = {}
        self.scale = 20    # realistic view with A4 paper in background an 5mm grid lines
        self.grid  = 'yes' # String!
        self.svg   = ''    # Content of SVG data
        self.paperwidthMM = 3000
        self.paperheightMM = 3000
        self.pix_x = self.paperwidthMM * 10
        self.pix_y = self.paperheightMM * 10
        self.kast = 50 # => 5mm = 1 Kästchen (when ViewBox has 10 times pixel as mm of "paper" size)
        self.defaultColor = 'black'

        # Instruction as Text #
        self.textWidget = QTextEdit()
        self.txtFilename = ''

        # Instruction as SVG Image #
        self.svgWidget = QtSvg.QSvgWidget() #"samples/t_001.svg")
        self.svgWidget.setGeometry(50,50,759,668)
        self.svgWidget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.svgWidget.setSizePolicy(QtWidgets.QSizePolicy(0,0))
        self.svgFilename = ''

        self.scrollArea = QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.svgWidget)

        # Combine Instructions with Splitter
        designSplitter = QSplitter(Qt.Horizontal)
        designSplitter.addWidget(self.textWidget)
        designSplitter.addWidget(self.scrollArea)
        designSplitter.setSizes([50,150])

        hbox = QHBoxLayout()
        hbox.addWidget(designSplitter)
        self.layout = hbox
        self.setLayout(self.layout)

    # ===== PUBLIC METHODS ====================================================================== #
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

        self.open()
    def onRedraw(self):
        # Read plain text instructions #
        content = self.textWidget.toPlainText()
        lines = content.split('\n')
        self.svg = ''
        self.elems = []
        self.picot = {}

        # Recalculate svg string #
        self._create_meta(lines)
        for line in lines:
            self._add(line)
        self.svg = self.svg + '</svg>'

        # Show SVG string #
        self.svgWidget.load(bytearray(self.svg, encoding='utf-8'))
        self.svgWidget.resize(round(self.paperwidthMM * 10), round(self.paperheightMM * 10))
    def onSave(self):
        content = self.textWidget.toPlainText()
        
        with open(self.txtFilename, 'w', encoding="utf-8") as f:
            f.write(content)
        f.close() 

        with open(self.svgFilename, 'w', encoding="utf-8") as f:
            f.write(self.svg)
        f.close() 
    def onZoomIn(self):
        #self.paperwidthMM  = self.paperwidthMM * 1.1
        #self.paperheightMM = self.paperheightMM * 1.1
        self.kast          = self.kast * 1.1
        self.scale         = self.scale / 1.1
        self.onRedraw()
    def onZoomOut(self):
        #self.paperwidthMM  = self.paperwidthMM / 1.1
        #self.paperheightMM = self.paperheightMM / 1.1
        self.kast          = self.kast / 1.1
        self.scale         = self.scale * 1.1
        self.onRedraw()

    def open(self):
        # Read text file and assign content #
        with open(self.txtFilename, encoding="utf-8") as f:
            instr = ''
            for line in f.readlines():
                instr = instr + line
            self.textWidget.setPlainText(instr)
        f.close()

        # Show SVG file #
        self.onRedraw()

    # ===== PRIVATE PART OF CLASS =============================================================== #
    def _create_meta(self, lines):
        self.svg = self.svg + '<?xml version="1.0" encoding="UTF-8"?>\n' \
                + '<svg xmlns="http://www.w3.org/2000/svg"\n' \
                + '    xmlns:xlink="http://www.w3.org/1999/xlink"\n' \
                + '    version="1.1" baseProfile="full"\n' \
                + '    width="%dmm" height="%dmm"\n' % (self.paperwidthMM,self.paperheightMM) \
                + '    viewBox="0 0 ' + str(self.pix_x) + ' ' + str(self.pix_y) + '">\n' \
                + '    <rect width="' + str(self.pix_x) + '" height="' + str(self.pix_y) \
                + '" style="fill:white;stroke-width:1;stroke:rgb(0,0,0)"/>\n' \
                + '\n<!-- File Content -->\n'

        # Draw Grid in whole "paper area" #
        if self.grid == 'yes':
            self.svg = self.svg + '\n<!-- Grid -->\n'
            i = 0
            while i <= self.pix_x:
                self.svg = self.svg + '<line x1="' + str(i) + '" y1="0" x2="' + str(i) + '" y2="' \
                    + str(self.pix_y) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + self.kast
            i = 0
            while i <= self.pix_y:
                self.svg = self.svg + '<line y1="' + str(i) + '" x1="0" y2="' + str(i) + '" x2="' \
                    + str(self.pix_x) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + self.kast

        # Read basic elements from /config/basic_elements.svg file and replace it here
        found = False
        next_is_coord = False
        fig_id = ''
        self.svg = self.svg + '<!-- Basic Elements -->\n'
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
                self.svg = self.svg + line
                reg = re.search('id=\"[^\"]*\"', line)
                if reg == None: continue
                fig_id = reg.group(0)
                fig_id = fig_id[4:-1]
                next_is_coord = True

            self.svg = self.svg + '\n<!-- Individueller Teil -->\n'
    def _add(self,line):
        if len(line) == 0: return
        if line[0] == '#': return

        # Parse line
        element = {}
        regexp = '\{[-]*[0-9]+\}'
        coord_x = coord_y = -1

        # Initial values
        element["color"] = ''

        # Search for id, figure variant, definition, output coordinates
        pos = line.find(':')

        if pos == -1:
            return

        element["id"] = line[:pos].strip()
        # Variant of ring or chain (a, b, c, ...) in [..]
        pos1 = element["id"].find('[')
        pos2 = element["id"].find(']')
        if pos1 >= 0 and pos2 >= 0:
            element["variant"] = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
        else:
            if element["id"][0] in ('R', 'C', 'c'):
                element["variant"] = 'a'
        element["def"] = line[pos+1:].strip()

        # Additional Instructions such as coloring in {..}
        pos1 = element["id"].find('{')
        pos2 = element["id"].find('}')
        if pos1 >= 0 and pos2 >= 0:
            instr = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
            instrList = instr.split(',')
            for instrTxt in instrList:
                pos3 = instrTxt.find('=')
                if pos3 >= 0:
                    key = instrTxt[:pos3]
                    val = instrTxt[pos3+1:]
                    if key == 'color':
                        element["color"] = val          

        # Output coordinates if available in (..)
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
        # Size of Rings and Chains must be scaled according to the number of nodes; elements 
        # consisting of such scaled rings and chains do not need to be scaled
        if element["id"][0] in ('R', 'c', 'C'):
            scale  = element["nodes"] / self.scale          # figure scale factor
            figure = element["id"][0] + element["variant"]  # figure name
            for el in self.elems:
                if el["id"] == figure:
                    element["dx"] = scale * int(el["dx"])   # figure width
                    element["dy"] = scale * int(el["dy"])   # figure height
                    exit

            self.svg = self.svg + '<g id="' + element["id"] + '" fill="none" stroke-linecap="round">\n' \
                                + '   <use xlink:href="#' + figure + '" ' \
                                + 'transform="scale(' + str(scale) + ' ' + str(scale) + ')"/>\n'
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
                    self.svg = self.svg + '   <use  xlink:href="#picot" ' \
                                + 'transform="translate(' + str(x) + ' ' + str(y) + ') '\
                                + 'rotate(' + str(place[2]) + ') ' \
                                + 'scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')"/>\n'

            self.svg = self.svg + '</g>\n'

        # (Teil-) Figuren #
        else:
            # Starting point for next element of the figure; in the end this is the end coordinate
            dx = 0
            dy = 0

            # Start of figure
            self.svg = self.svg + '<g id="' + element["id"] + '" fill="none" stroke-linecap="round">\n'

            lst = element["def"].split(" ")
            for figure in lst:
                # Angle in form: {..} as degree-value >> if available, recalculate to radiant #
                grad = 0
                rad = 0
                regex = re.search(regexp, figure)
                if regex:
                    grad = float(regex.group(0)[1:-1])
                    rad = math.radians(grad)

                # Get figure = Name of element without angle in form: {..} #
                figure = re.sub(regexp, '', figure, 0, 0)

                # Draw element #
                self.svg = self.svg + '   <use xlink:href="#' + figure + '" ' \
                            + 'transform="translate(' + str(dx) + ' ' + str(dy) + ') '\
                            + 'rotate(' + str(grad) + ')"/>\n'

                # Calculate dx and dy for figure #
                for el in self.elems:
                    if el["id"] == figure:
                        dx = dx + el["dx"] * math.cos(rad) - el["dy"] * math.sin(rad)
                        dy = dy + el["dx"] * math.sin(rad) + el["dy"] * math.cos(rad)

            # End of figure and end coordinate
            self.svg = self.svg + '</g>\n'
            element["dx"] = dx
            element["dy"] = dy

        # Final auszugebende Figur #
        if coord_x >= 0 and coord_y >= 0: #element["id"][0] == 'Z':
            if element["color"] == '':
                element["color"] = self.defaultColor
            self.svg = self.svg + '<!-- Ausgabe -->\n'
            self.svg = self.svg + '<g stroke="' + element["color"] + '" fill="none" stroke-width="1" stroke-linecap="round">\n'
            self.svg = self.svg + '   <use xlink:href="#' + element["id"] \
                                + '" transform="translate(' + str(coord_x*20/self.scale) + ' ' + str(coord_y*20/self.scale) + ')"/>\n'
            self.svg = self.svg + '</g>\n'
            self.svg = self.svg + '<circle cx="' + str(coord_x*20/self.scale) + '" cy="' + str(coord_y*20/self.scale) + '"  r="10" style="fill:red" />\n'

        self.elems.append(element)